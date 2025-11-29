def merge_orders_items_customers(orders, items, customers):
    merged = orders.merge(items, on="order_id", how="left")
    merged = merged.merge(customers, on="customer_id", how="left")
    return merged
