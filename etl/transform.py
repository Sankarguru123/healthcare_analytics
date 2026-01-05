import pandas as pd


def hc_transform(df):

    df['visit_date'] = pd.to_datetime(df['visit_date'],errors='coerce')

    df["department"] = (
        df["department"]
        .str.strip()
        .str.title()
    )
    df['collections'] = df['collections'].fillna(0)
    df['ar_amount'] = df['charges'] - df['collections']
    df['payment_status'] = df['ar_amount'].apply(
        lambda x: 'Paid' if x ==0 else 'Pending'
    )
    return df