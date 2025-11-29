from load_data import load_orders, load_customers, load_order_items, load_geolocation
from preprocess import clean_orders, add_time_features
from merge_tables import merge_orders_items_customers
from analysis_customers import customers_by_state
from visualization import plot_top_categories

# 1. Carregar dados
orders = load_orders()
customers = load_customers()
items = load_order_items()
geolocation = load_geolocation()

# 2. Pré-processar
orders = clean_orders(orders)
orders = add_time_features(orders)

# 3. Merge
df = merge_orders_items_customers(orders, items, customers)

# 4. Análises
cust_state = customers_by_state(df)
print(cust_state)

# 5. Visualização
plot_top_categories(df)
