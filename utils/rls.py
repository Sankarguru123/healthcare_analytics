# utils/rls.py  ✅ FIXED
import pandas as pd
from sqlalchemy import text

def hc_apply_rls(df, engine, user):
    access = pd.read_sql(
        text("""
            SELECT department
            FROM user_department_access
            WHERE user_name = :user_name
        """),
        engine,
        params={
            "user_name": user
        }
    )

    if "ALL" in access["department"].values:
        return df

    return df[df["department"].isin(access["department"])]



def hc_get_users(engine):

    user_df = pd.read_sql(
        text("""
            select distinct user_name 
            from user_department_access
            order by user_name       
        """),
        engine,

    )
    return user_df["user_name"].tolist()

