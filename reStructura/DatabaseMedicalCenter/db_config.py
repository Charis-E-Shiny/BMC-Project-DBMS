import os
import sys

def get_db_connection():
    """
    Create and return a database connection using environment variables
    with fallback to default values for development.
    Attempts to use MySQL first, falls back to PostgreSQL if MySQL fails.
    """
    # Check if we need to use PostgreSQL (when DATABASE_URL is set)
    if os.environ.get('DATABASE_URL'):
        import psycopg2
        return psycopg2.connect(
            host=os.environ.get('PGHOST', 'localhost'),
            user=os.environ.get('PGUSER', 'postgres'),
            password=os.environ.get('PGPASSWORD', 'charis123'),
            dbname=os.environ.get('PGDATABASE', 'BMCbase'),
            port=os.environ.get('PGPORT', '5432')
        )
    else:
        # Try to use MySQL
        try:
            import MySQLdb
            return MySQLdb.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                user=os.environ.get('DB_USER', 'root'),
                passwd=os.environ.get('DB_PASS', 'charis123'),
                db=os.environ.get('DB_NAME', 'BMCbase')
            )
        except (ImportError, Exception) as e:
            # If MySQL fails, fall back to PostgreSQL
            print(f"MySQL connection failed: {e}. Falling back to PostgreSQL", file=sys.stderr)
            import psycopg2
            return psycopg2.connect(
                host=os.environ.get('PGHOST', 'localhost'),
                user=os.environ.get('PGUSER', 'postgres'),
                password=os.environ.get('PGPASSWORD', 'postgres'),
                dbname=os.environ.get('PGDATABASE', 'structura_db'),
                port=os.environ.get('PGPORT', '5432')
            )
