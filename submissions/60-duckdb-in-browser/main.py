"""
DuckDB In-Browser Analytics Demo
Showcases: SQL queries, file formats, analytics functions
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Initialize DuckDB
duckdb = None
try:
    import duckdb as ddb
    duckdb = ddb
    print("DuckDB initialized")
except ImportError:
    print("duckdb not installed. Running in demo mode.")

def basic_sql_demo():
    """Basic SQL operations"""
    print("\nBasic SQL Demo:")

    if duckdb:
        con = duckdb.connect()

        # Create sample data
        con.execute("""
            CREATE TABLE users AS
            SELECT * FROM (VALUES
                (1, 'Alice', 28, 'Engineering'),
                (2, 'Bob', 34, 'Marketing'),
                (3, 'Carol', 29, 'Engineering'),
                (4, 'Dave', 42, 'Sales'),
                (5, 'Eve', 31, 'Engineering')
            ) AS t(id, name, age, department)
        """)

        # Query
        result = con.execute("""
            SELECT department, COUNT(*) as count, AVG(age) as avg_age
            FROM users
            GROUP BY department
            ORDER BY count DESC
        """).fetchall()

        print("  Department stats:")
        for row in result:
            print(f"    {row[0]}: {row[1]} employees, avg age {row[2]:.1f}")

        con.close()
    else:
        print("  [Demo] Query results:")
        print("    Engineering: 3 employees, avg age 29.3")
        print("    Marketing: 1 employee, avg age 34.0")
        print("    Sales: 1 employee, avg age 42.0")

def parquet_demo():
    """Query Parquet files"""
    print("\nParquet File Demo:")

    if duckdb:
        con = duckdb.connect()

        # Create sample parquet file
        con.execute("""
            COPY (
                SELECT i as id,
                       'product_' || i as name,
                       RANDOM() * 100 as price
                FROM generate_series(1, 1000) t(i)
            ) TO 'sample.parquet' (FORMAT PARQUET)
        """)

        # Query parquet
        result = con.execute("""
            SELECT COUNT(*) as total,
                   AVG(price) as avg_price,
                   MIN(price) as min_price,
                   MAX(price) as max_price
            FROM 'sample.parquet'
        """).fetchone()

        print(f"  Total rows: {result[0]}")
        print(f"  Price range: ${result[2]:.2f} - ${result[3]:.2f}")
        print(f"  Average: ${result[1]:.2f}")

        # Clean up
        os.remove("sample.parquet")
        con.close()
    else:
        print("  [Demo] Parquet query results:")
        print("    Total rows: 1000")
        print("    Price range: $0.12 - $99.87")
        print("    Average: $49.52")

def json_demo():
    """Query JSON data"""
    print("\nJSON Data Demo:")

    if duckdb:
        con = duckdb.connect()

        # Query JSON directly
        result = con.execute("""
            SELECT *
            FROM (
                SELECT unnest([
                    {'name': 'Alice', 'score': 95},
                    {'name': 'Bob', 'score': 87},
                    {'name': 'Carol', 'score': 92}
                ]) as data
            )
        """).fetchall()

        print("  JSON records:")
        for row in result:
            print(f"    {row}")

        con.close()
    else:
        print("  [Demo] JSON processing supported")
        print("    - read_json_auto('file.json')")
        print("    - JSON path expressions")
        print("    - Nested struct handling")

def window_functions_demo():
    """Advanced analytics with window functions"""
    print("\nWindow Functions Demo:")

    if duckdb:
        con = duckdb.connect()

        result = con.execute("""
            WITH sales AS (
                SELECT * FROM (VALUES
                    ('2024-01', 'A', 100),
                    ('2024-02', 'A', 150),
                    ('2024-03', 'A', 120),
                    ('2024-01', 'B', 200),
                    ('2024-02', 'B', 180),
                    ('2024-03', 'B', 220)
                ) AS t(month, product, revenue)
            )
            SELECT
                month,
                product,
                revenue,
                SUM(revenue) OVER (PARTITION BY product ORDER BY month) as cumulative,
                LAG(revenue) OVER (PARTITION BY product ORDER BY month) as prev_month
            FROM sales
            ORDER BY product, month
        """).fetchall()

        print("  Sales with running totals:")
        print("  Month    | Product | Revenue | Cumulative | Prev")
        for row in result:
            prev = row[4] if row[4] else '-'
            print(f"  {row[0]} | {row[1]}       | ${row[2]:>3}    | ${row[3]:>3}       | {prev}")

        con.close()
    else:
        print("  [Demo] Window functions: ROW_NUMBER, RANK, LAG, LEAD, SUM OVER, etc.")

def remote_file_demo():
    """Query remote files with httpfs"""
    print("\nRemote File Demo (httpfs):")

    if duckdb:
        con = duckdb.connect()

        # Install and load httpfs
        con.execute("INSTALL httpfs")
        con.execute("LOAD httpfs")

        print("  httpfs extension loaded!")
        print("  Can now query remote files:")
        print("    SELECT * FROM 'https://example.com/data.parquet'")
        print("    SELECT * FROM 's3://bucket/data.csv'")

        con.close()
    else:
        print("  [Demo] httpfs enables remote queries:")
        print("    - HTTP/HTTPS files")
        print("    - S3 buckets")
        print("    - GCS storage")

def wasm_example():
    """Show WASM usage for browser"""
    print("\nWASM Browser Example:")
    print("-" * 40)

    code = '''
<!-- In HTML -->
<script src="https://cdn.jsdelivr.net/npm/@duckdb/duckdb-wasm/dist/duckdb-browser.js"></script>

<script type="module">
import * as duckdb from '@duckdb/duckdb-wasm';

// Initialize
const db = await duckdb.createInstance();

// Run queries
const result = await db.query(`
    SELECT * FROM read_csv_auto('data.csv')
    WHERE value > 100
`);

console.log(result.toArray());
</script>
'''
    print(code)

def main():
    print("=" * 50)
    print("DuckDB In-Browser Analytics Demo")
    print("=" * 50)

    if duckdb:
        print(f"DuckDB version: {duckdb.__version__}")
    else:
        print("Running in demo mode")

    print("\nAvailable demos:")
    print("  1. Basic SQL Operations")
    print("  2. Parquet File Queries")
    print("  3. JSON Data Processing")
    print("  4. Window Functions")
    print("  5. Remote Files (httpfs)")
    print("  6. WASM Browser Example")
    print("  7. Run all demos")

    choice = input("\nSelect demo (1-7): ").strip()

    if choice == "1":
        basic_sql_demo()
    elif choice == "2":
        parquet_demo()
    elif choice == "3":
        json_demo()
    elif choice == "4":
        window_functions_demo()
    elif choice == "5":
        remote_file_demo()
    elif choice == "6":
        wasm_example()
    elif choice == "7":
        basic_sql_demo()
        parquet_demo()
        json_demo()
        window_functions_demo()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
