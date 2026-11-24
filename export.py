import os
from pathlib import Path

import snowflake.connector

TABLES = ["mart_form", "mart_home_away", "mart_attack_defense"]
OUT_DIR = Path("app/data")

if __name__ == "__main__":
    conn = snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        warehouse="PL_WH",
        database="PL_DB",
        schema="ANALYTICS",
        role="ACCOUNTADMIN",
    )
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for table in TABLES:
        df = conn.cursor().execute(f"select * from {table}").fetch_pandas_all()
        df.columns = [c.lower() for c in df.columns]
        df.to_parquet(OUT_DIR / f"{table}.parquet", index=False)
        print(table, len(df))

    conn.close()