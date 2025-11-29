def top_sellers(df, n=10):
    return df.groupby("seller_id")["price"].sum().nlargest(n)
