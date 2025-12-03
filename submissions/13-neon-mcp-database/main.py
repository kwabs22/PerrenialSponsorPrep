"""
Neon MCP Database Manager
Showcases: MCP Server for AI Agents
This is a client demo - the MCP server runs separately
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def main():
    print("=" * 50)
    print("Neon MCP Database Demo")
    print("=" * 50)

    # Direct connection demo (MCP server handles this via natural language)
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    # Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    print("✅ Created tasks table")

    # Insert sample data
    cur.execute("INSERT INTO tasks (title) VALUES ('Learn Neon MCP') RETURNING id")
    task_id = cur.fetchone()[0]
    conn.commit()
    print(f"✅ Created task {task_id}")

    # Query
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    print(f"\n📋 Tasks: {tasks}")

    cur.close()
    conn.close()

    print("\n💡 MCP Setup:")
    print("1. Install: npm install @neondatabase/mcp-server-neon")
    print("2. Add to Claude Desktop config:")
    print('   "neon": {"command": "npx", "args": ["-y", "@neondatabase/mcp-server-neon"]}')
    print("3. Ask Claude: 'Show me all tables in my Neon database'")

if __name__ == "__main__":
    main()
