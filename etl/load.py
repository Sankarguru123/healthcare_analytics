import pandas as pd

def hc_incremental_load(df, engine, start, end):
    # 🔧 Convert sidebar dates to pandas datetime
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)

    # 🔧 Ensure visit_date is datetime
    df["visit_date"] = pd.to_datetime(df["visit_date"], errors="coerce")

    # ✅ Safe datetime comparison
    df_filtered = df[
        (df["visit_date"] >= start_dt) &
        (df["visit_date"] < end_dt)
    ]

    if not df_filtered.empty:
        df_filtered.to_sql(
            "fact_billing",
            engine,
            if_exists="append",
            index=False
        )
