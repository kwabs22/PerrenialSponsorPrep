"""
Snowflake Cortex AI Demo
Showcases: LLM functions, embeddings, ML in SQL
"""

import os
from dotenv import load_dotenv

load_dotenv()

SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")

# Initialize Snowflake
snowflake = None
try:
    import snowflake.connector
    if SNOWFLAKE_ACCOUNT and SNOWFLAKE_USER:
        snowflake = snowflake.connector
        print("Snowflake connector initialized")
    else:
        print("Warning: Snowflake credentials not set. Running in demo mode.")
except ImportError:
    print("snowflake-connector-python not installed. Running in demo mode.")

def get_connection():
    """Create Snowflake connection"""
    if snowflake and SNOWFLAKE_ACCOUNT:
        return snowflake.connect(
            account=SNOWFLAKE_ACCOUNT,
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD
        )
    return None

def cortex_complete_demo():
    """Use Cortex COMPLETE for text generation"""
    print("\nCortex COMPLETE Demo (LLM):")

    sql = """
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'llama3.1-70b',
        'Explain data warehousing in one paragraph'
    ) as response
    """

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        print(f"  Response: {result[0][:300]}...")
        cursor.close()
        conn.close()
    else:
        print(f"  [Demo] SQL: {sql}")
        print("  Would return LLM-generated explanation of data warehousing")

def cortex_sentiment_demo():
    """Sentiment analysis with Cortex"""
    print("\nCortex Sentiment Demo:")

    sql = """
    SELECT
        review_text,
        SNOWFLAKE.CORTEX.SENTIMENT(review_text) as sentiment
    FROM (
        SELECT 'This product is amazing!' as review_text
        UNION ALL SELECT 'Terrible experience, never again'
        UNION ALL SELECT 'It was okay, nothing special'
    )
    """

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        print("  Review Analysis:")
        for row in results:
            print(f"    '{row[0][:30]}...' -> {row[1]}")
        cursor.close()
        conn.close()
    else:
        print("  [Demo] Sentiment scores:")
        print("    'This product is amazing!' -> 0.95 (positive)")
        print("    'Terrible experience...' -> -0.87 (negative)")
        print("    'It was okay...' -> 0.12 (neutral)")

def cortex_embed_demo():
    """Generate embeddings with Cortex"""
    print("\nCortex Embeddings Demo:")

    sql = """
    SELECT
        text,
        SNOWFLAKE.CORTEX.EMBED_TEXT_768('e5-base-v2', text) as embedding
    FROM (
        SELECT 'Machine learning transforms data into insights' as text
    )
    """

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        embedding = result[1]
        print(f"  Text: {result[0]}")
        print(f"  Embedding dimension: {len(embedding)}")
        print(f"  First 5 values: {embedding[:5]}")
        cursor.close()
        conn.close()
    else:
        print("  [Demo] EMBED_TEXT_768 returns 768-dim vector")
        print("    Dimension: 768")
        print("    Values: [-0.023, 0.156, -0.089, ...]")

def cortex_summarize_demo():
    """Summarize text with Cortex"""
    print("\nCortex Summarize Demo:")

    sql = """
    SELECT SNOWFLAKE.CORTEX.SUMMARIZE(
        'Snowflake is a cloud data platform that provides data warehousing,
        data lakes, data engineering, data science, and data application
        development. It was founded in 2012 and went public in 2020 with
        the largest software IPO in history. The platform runs on AWS,
        Azure, and Google Cloud.'
    ) as summary
    """

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        print(f"  Summary: {result[0]}")
        cursor.close()
        conn.close()
    else:
        print("  [Demo] Would summarize long text into key points")
        print("    'Snowflake is a cloud data platform for warehousing and analytics...'")

def cortex_translate_demo():
    """Translate text with Cortex"""
    print("\nCortex Translate Demo:")

    sql = """
    SELECT
        SNOWFLAKE.CORTEX.TRANSLATE(
            'Hello, how are you today?',
            'en', 'es'
        ) as spanish,
        SNOWFLAKE.CORTEX.TRANSLATE(
            'Hello, how are you today?',
            'en', 'fr'
        ) as french
    """

    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        print(f"  English: 'Hello, how are you today?'")
        print(f"  Spanish: {result[0]}")
        print(f"  French: {result[1]}")
        cursor.close()
        conn.close()
    else:
        print("  [Demo] Translation:")
        print("    English: 'Hello, how are you today?'")
        print("    Spanish: 'Hola, como estas hoy?'")
        print("    French: 'Bonjour, comment allez-vous?'")

def ml_forecast_demo():
    """Time series forecasting"""
    print("\nML Forecasting Demo:")

    example = """
    -- Create forecasting model
    CREATE OR REPLACE SNOWFLAKE.ML.FORECAST model_sales_forecast(
        INPUT_DATA => TABLE(sales_data),
        TIMESTAMP_COLNAME => 'date',
        TARGET_COLNAME => 'revenue'
    );

    -- Generate forecast
    SELECT * FROM TABLE(
        model_sales_forecast!FORECAST(
            FORECASTING_PERIODS => 30
        )
    );
    """

    print("  SQL Example:")
    print(example)

def main():
    print("=" * 50)
    print("Snowflake Cortex AI Demo")
    print("=" * 50)

    if SNOWFLAKE_ACCOUNT:
        print(f"Account: {SNOWFLAKE_ACCOUNT}")
    else:
        print("Running in demo mode (no credentials)")

    print("\nAvailable demos:")
    print("  1. Cortex COMPLETE (LLM)")
    print("  2. Sentiment Analysis")
    print("  3. Text Embeddings")
    print("  4. Summarization")
    print("  5. Translation")
    print("  6. ML Forecasting")
    print("  7. Run all demos")

    choice = input("\nSelect demo (1-7): ").strip()

    if choice == "1":
        cortex_complete_demo()
    elif choice == "2":
        cortex_sentiment_demo()
    elif choice == "3":
        cortex_embed_demo()
    elif choice == "4":
        cortex_summarize_demo()
    elif choice == "5":
        cortex_translate_demo()
    elif choice == "6":
        ml_forecast_demo()
    elif choice == "7":
        cortex_complete_demo()
        cortex_sentiment_demo()
        cortex_embed_demo()
        cortex_summarize_demo()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
