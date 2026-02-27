import pandas as pd
import psycopg
import matplotlib.pyplot as plt

# 1. Database connection parameters
DB_PARAMS = "user=postgres host=localhost password=some_password port=8006"


def process_song_matches(csv_path):
    # Load the CSV
    df_input = pd.read_csv(csv_path)
    results = []

    # Connect to the database
    with psycopg.connect(DB_PARAMS) as conn:
        with conn.cursor() as cur:
            for song_name in df_input["Track Name"]:
                # The <-> operator returns the distance between the query and the closest match
                cur.execute(
                    """
                    SELECT 
                        song_name, 
                        song_name <-> %s AS distance
                    FROM 
                        dance_descriptions
                    ORDER BY 
                        distance
                    LIMIT 1
                """,
                    (song_name,),
                )

                row = cur.fetchone()
                if row:
                    results.append(
                        {
                            "song_name": song_name,
                            "closest_match": row[0],
                            "distance_to_closest_match": row[1],
                        }
                    )

    # 2. Create the pandas DataFrame
    df_results = pd.DataFrame(results)

    # 3. Use matplotlib to plot a histogram
    plt.figure(figsize=(10, 6))
    plt.hist(
        df_results["distance_to_closest_match"],
        bins=20,
        color="skyblue",
        edgecolor="black",
    )
    plt.title("Distribution of Distances to Closest Song Matches")
    plt.xlabel("Distance (Lower is closer)")
    plt.ylabel("Frequency")
    plt.grid(axis="y", alpha=0.75)
    plt.savefig("closest_matches.png", dpi=200)

    return df_results


res_df = process_song_matches("ww_master_wed.csv")
res_df.to_csv("df_results.csv", index=False)
