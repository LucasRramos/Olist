def freight_share(df):
    df["freight_share"] = df["freight_value"] / (df["price"] + df["freight_value"])
    return df
