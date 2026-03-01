import uvicorn
from fastapi import HTTPException, Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import os
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row

app = FastAPI()

@app.middleware("http")
async def log_origin(request: Request, call_next):
    # This prints the origin header sent by the browser to your console
    origin = request.headers.get("origin")
    print(f"\n[CORS DEBUG] Incoming Request Origin: {origin}")
    response = await call_next(request)
    return response

# Equivalent to your CORSRequestHandler settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=["http://127.0.0.1:5173"], # NOTE: should do this soon
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["X-Requested-With", "Content-Type"],
)


# 1. Setup the Connection Pool
DATABASE_URL = "user=postgres host=localhost password=some_password port=8006"

# We initialize the pool outside the request cycle
pool = AsyncConnectionPool(conninfo=DATABASE_URL, open=False)


@app.on_event("startup")
async def open_pool():
    await pool.open()


@app.on_event("shutdown")
async def close_pool():
    await pool.close()


# 2. Dependency to get a connection from the pool
async def get_db():
    async with pool.connection() as conn:
        # dict_row allows accessing columns by name like a dictionary
        yield conn


# 3. Updated Logic
async def get_tutorial_url(conn, song_name: str) -> tuple[str, float, str]:
    # We use an async cursor to execute the query
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            """
                select
                    dance_descriptions.song_name as best_match,
                    dances.url,
                    dance_descriptions.song_name <-> %s as distance
                FROM
                    dances
                JOIN
                    dance_descriptions
                ON
                    dances.id = dance_descriptions.id
                order by
                    dance_descriptions.song_name <-> %s
                limit 1
                """,
            (song_name, song_name),
        )
        result = await cur.fetchone()

        if not result:
            return None
        return (result["url"], result["distance"], result["best_match"])


@app.get("/linedance_database/tutorial_url")
async def tutorial_url(song_name: str, db=Depends(get_db)):
    url, distance, best_match = await get_tutorial_url(db, song_name)

    if url is None:
        raise HTTPException(status_code=404, detail="Dance tutorial not found")

    return {"tutorial_url": url, "distance": distance, "best_match": best_match}


if __name__ == "__main__":
    port = 8005
    print(f"Serving on port {port} with CORS enabled...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload="DEBUG" in os.environ,
    )
