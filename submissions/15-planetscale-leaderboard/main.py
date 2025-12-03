"""
PlanetScale Leaderboard
Showcases: Boost Query Caching
"""
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def main():
    print("=" * 50)
    print("PlanetScale Leaderboard")
    print("=" * 50)

    conn = mysql.connector.connect(
        host=os.getenv("PLANETSCALE_HOST"),
        user=os.getenv("PLANETSCALE_USER"),
        password=os.getenv("PLANETSCALE_PASSWORD"),
        database=os.getenv("PLANETSCALE_DATABASE"),
        ssl_ca="/etc/ssl/certs/ca-certificates.crt"
    )
    cursor = conn.cursor()

    # Create leaderboard table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INT AUTO_INCREMENT PRIMARY KEY,
            player_name VARCHAR(100),
            score INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Add sample scores
    players = [("Alice", 1500), ("Bob", 1200), ("Charlie", 1800)]
    cursor.executemany(
        "INSERT INTO leaderboard (player_name, score) VALUES (%s, %s)",
        players
    )
    conn.commit()

    # Query top scores (Boost caches this automatically)
    cursor.execute("""
        SELECT player_name, score FROM leaderboard
        ORDER BY score DESC LIMIT 10
    """)

    print("\n🏆 Leaderboard:")
    for i, (name, score) in enumerate(cursor.fetchall(), 1):
        print(f"  {i}. {name}: {score}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
