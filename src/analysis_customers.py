def customers_by_state(df):
    return df.groupby("customer_state")["order_id"].nunique().reset_index()
