import pandas as pd

# def load_orders(path="data/olist_orders_dataset.csv"):
#     return pd.read_csv(path, parse_dates=[
#         'order_purchase_timestamp','order_delivered_customer_date',
#         'order_estimated_delivery_date'
#     ])

def load_customers(path="data/customers(Clientes)_dataset.csv"):
    return pd.read_csv(path)

def load_geolocation(path="data/geolocation(GeoLocalizacao)_dataset.csv"):
    return pd.read_csv(path)

def load_order_items(path="data/order_items(itens_pedido)_dataset.csv"):
    return pd.read_csv(path)

def load_order_payments(path="data/order_payments(pagamento_pedido)_dataset.csv"):
    return pd.read_csv(path)

def load_order_reviews(path="data/order_reviews(avaliacao_pedido)_dataset.csv"):
    return pd.read_csv(path)

def load_orders(path="data/orders(Pedidos)_dataset.csv"):
    return pd.read_csv(path)

def load_products(path="data/products(Produtos)_dataset.csv"):
    return pd.read_csv(path)

def load_sellers(path="data/sellers(Vendedores)_dataset.csv"):
    return pd.read_csv(path)
