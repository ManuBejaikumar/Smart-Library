import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="smart library",
            user="postgres",
            password="Miyamura18",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to DB: {e}")
        return None