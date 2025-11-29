import pandas as pd

def clean_orders(df):
    # Exemplo: filtrar apenas pedidos entregues
    return df[df['order_status'] == 'delivered'].copy()

def add_time_features(df):
    df['order_year_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
    return df

def add_time_features(df, col="order_purchase_timestamp"):
    """
    Adiciona colunas derivadas de tempo a partir de um timestamp.
    """
    # Converter para datetime
    df[col] = pd.to_datetime(df[col], errors="coerce")

    # Criar features temporais
    df['order_year'] = df[col].dt.year
    df['order_month'] = df[col].dt.month
    df['order_weekday'] = df[col].dt.day_name()
    df['order_hour'] = df[col].dt.hour
    df['order_year_month'] = df[col].dt.to_period('M').astype(str)

    return df