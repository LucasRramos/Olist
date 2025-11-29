import seaborn as sns
import matplotlib.pyplot as plt

def plot_top_categories(df):
    sns.barplot(data=df, x="total_revenue", y="product_category_name")
    plt.title("Top categorias por receita")
    plt.show()
