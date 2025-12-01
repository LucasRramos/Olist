
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar a tabela de itens do pedido
items = pd.read_csv("order_items(itens_pedido)_dataset.csv")

# Contar número de vendas por vendedor (quantidade de itens vendidos)
vendas_por_vendedor = items.groupby("seller_id").size().reset_index(name="quantidade_vendas")

# Ordenar do maior para o menor
vendas_por_vendedor = vendas_por_vendedor.sort_values(by="quantidade_vendas", ascending=False)

# Selecionar os 10 vendedores com maior número de vendas
top10_vendedores = vendas_por_vendedor.head(10)

# Exibir os dados
print("Top 10 vendedores com maior número de vendas:")
print(top10_vendedores)

# Criar gráfico de barras
plt.figure(figsize=(10,6))
sns.barplot(data=top10_vendedores, x="seller_id", y="quantidade_vendas", palette="Blues_d")
plt.title("Top 10 Vendedores com Maior Número de Vendas")
plt.xlabel("ID do Vendedor")
plt.ylabel("Quantidade de Vendas")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
