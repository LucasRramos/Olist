
# %% Imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid", palette="deep")
plt.rcParams['figure.figsize'] = (10, 6)

# %% Carregamento
customers = pd.read_csv("customers(Clientes)_dataset.csv")
geos      = pd.read_csv("geolocation(GeoLocalizacao)_dataset.csv")
items     = pd.read_csv("order_items(itens_pedido)_dataset.csv")
payments  = pd.read_csv("order_payments(pagamento_pedido)_dataset.csv")
reviews   = pd.read_csv("order_reviews(avaliacao_pedido)_dataset.csv")
orders    = pd.read_csv("orders(Pedidos)_dataset.csv")
products  = pd.read_csv("products(Produtos)_dataset.csv")
sellers   = pd.read_csv("sellers(Vendedores)_dataset.csv")

# %% Conversão de datas
date_cols = [
    "order_purchase_timestamp","order_approved_at",
    "order_delivered_carrier_date","order_delivered_customer_date",
    "order_estimated_delivery_date","review_creation_date","review_answer_timestamp",
    "shipping_limit_date"
]
for c in date_cols:
    if c in orders.columns:
        orders[c] = pd.to_datetime(orders[c], errors="coerce")
    if c in reviews.columns:
        reviews[c] = pd.to_datetime(reviews[c], errors="coerce")
    if c in items.columns:
        items[c] = pd.to_datetime(items[c], errors="coerce")

# %% Derivações úteis
# Valor total do pedido (produto + frete)
order_price = items.groupby("order_id", as_index=False).agg(
    valor_produto=("price","sum"),
    valor_frete=("freight_value","sum"),
    qtd_itens=("order_item_id","count")
)
order_price["valor_total"] = order_price["valor_produto"] + order_price["valor_frete"]

# Junta preço/frete com pedidos e clientes
orders_full = (orders
    .merge(order_price, on="order_id", how="left")
    .merge(customers[["customer_id","customer_unique_id","customer_city","customer_state","customer_zip_code_prefix"]],
           on="customer_id", how="left")
)

# Tempo de entrega (dias)
orders_full["tempo_entrega_dias"] = (
    orders_full["order_delivered_customer_date"] - orders_full["order_purchase_timestamp"]
).dt.days

# Filtrar apenas pedidos entregues
delivered = orders_full[orders_full["order_status"] == "delivered"].copy()

# %% Recompra por cliente
recompra = (delivered.groupby("customer_unique_id")
            .agg(pedidos=("order_id","nunique"),
                 valor_total=("valor_total","sum"))
            .reset_index())
recompra["eh_recompra"] = (recompra["pedidos"] > 1).astype(int)

# %% Preferência de pagamento
pay_sum = payments.groupby(["order_id","payment_type"], as_index=False).agg(
    valor_pagamento=("payment_value","sum"),
    parcelas=("payment_installments","max") # aproximação
)
pay_dist = pay_sum.groupby("payment_type")["valor_pagamento"].sum().sort_values(ascending=False).reset_index()

# %% Top categorias
items_products = items.merge(products[["product_id","product_category_name",
                                       "product_weight_g","product_length_cm",
                                       "product_height_cm","product_width_cm"]],
                             on="product_id", how="left")
cat_sales = (items_products.groupby("product_category_name")
             .agg(valor_produto=("price","sum"),
                  valor_frete=("freight_value","sum"),
                  pedidos=("order_id","nunique"),
                  peso_medio=("product_weight_g","mean"))
             .sort_values("valor_produto", ascending=False)
             .reset_index())

# %% Vendedores: ranking por receita
seller_perf = (items_products.groupby("seller_id")
               .agg(valor_produto=("price","sum"),
                    valor_frete=("freight_value","sum"),
                    pedidos=("order_id","nunique"))
               .assign(receita_total=lambda df: df["valor_produto"] + df["valor_frete"])
               .sort_values("receita_total", ascending=False)
               .reset_index())

# %% Avaliações + atraso
reviews_full = reviews.merge(orders[["order_id","order_purchase_timestamp","order_delivered_customer_date"]],
                             on="order_id", how="left")
reviews_full["atraso_dias"] = (
    reviews_full["order_delivered_customer_date"] - reviews_full["order_purchase_timestamp"]
).dt.days
# Pode existir NaN; considere filtrar somente delivered:
reviews_full = reviews_full.dropna(subset=["review_score"])

# %% Visualizações

# 1) Distribuição de pedidos por estado (clientes)
plt.figure()
sns.countplot(data=delivered, x="customer_state", order=delivered["customer_state"].value_counts().index)
plt.title("Pedidos por Estado (Clientes)")
plt.xlabel("Estado")
plt.ylabel("Quantidade de pedidos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2) Ticket médio por estado
ticket_estado = delivered.groupby("customer_state")["valor_total"].mean().sort_values(ascending=False)
plt.figure()
sns.barplot(x=ticket_estado.index, y=ticket_estado.values)
plt.title("Ticket Médio por Estado")
plt.xlabel("Estado")
plt.ylabel("Ticket médio (R$)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3) Preferência de pagamento
plt.figure()
sns.barplot(data=pay_dist, x="payment_type", y="valor_pagamento")
plt.title("Distribuição de Valor por Tipo de Pagamento")
plt.xlabel("Tipo de pagamento")
plt.ylabel("Valor total (R$)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4) Top 10 categorias por valor vendido
top_cat = cat_sales.head(10)
plt.figure()
sns.barplot(data=top_cat, x="product_category_name", y="valor_produto")
plt.title("Top 10 Categorias por Valor Vendido")
plt.xlabel("Categoria")
plt.ylabel("Valor vendido (R$)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# 5) Relação entre peso e frete
plt.figure()
sns.scatterplot(data=items_products.sample(min(10000, len(items_products), 10000), random_state=42),
                x="product_weight_g", y="freight_value", alpha=0.5)
plt.title("Peso do Produto vs Valor do Frete")
plt.xlabel("Peso (g)")
plt.ylabel("Frete (R$)")
plt.tight_layout()
plt.show()

# 6) Avaliações: distribuição de notas
plt.figure()
sns.countplot(data=reviews_full, x="review_score")
plt.title("Distribuição das Avaliações (Notas 1–5)")
plt.xlabel("Nota")
plt.ylabel("Quantidade")
plt.tight_layout()
plt.show()

# 7) Nota vs Atraso na entrega
plt.figure()
sns.boxplot(data=reviews_full.dropna(subset=["atraso_dias"]), x="review_score", y="atraso_dias")
plt.title("Atraso na Entrega por Nota de Avaliação")
plt.xlabel("Nota")
plt.ylabel("Atraso (dias)")
plt.tight_layout()
plt.show()

# 8) Séries temporais de pedidos
orders["mes"] = orders["order_purchase_timestamp"].dt.to_period("M")
serie_pedidos = orders.groupby("mes")["order_id"].nunique()
plt.figure()
serie_pedidos.index = serie_pedidos.index.astype(str)
sns.lineplot(x=serie_pedidos.index, y=serie_pedidos.values, marker="o")
plt.title("Pedidos por Mês")
plt.xlabel("Mês")
plt.ylabel("Quantidade de pedidos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
