import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import urllib

load_dotenv()

def get_engine():
    server   = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    driver   = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
    user     = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if user:
        conn_str = (
            f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
            f"UID={user};PWD={password};TrustServerCertificate=yes"
        )
    else:
        conn_str = (
            f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
            f"Trusted_Connection=yes;TrustServerCertificate=yes"
        )

    params = urllib.parse.quote_plus(conn_str)
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}", fast_executemany=True)

engine = get_engine()

if __name__ == "__main__":
    with engine.connect() as conn:
        result = conn.execute(text("SELECT @@VERSION"))
        print(result.scalar())