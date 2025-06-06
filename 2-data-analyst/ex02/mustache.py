from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Config
DB_NAME = "piscineds"
DB_USER = "dlu"
DB_PASS = "mysecretpassword"
DB_HOST = "localhost"

# Helpers
def get_data(query="SELECT * FROM customers"):
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
    return pd.read_sql(query, engine)

def save_plot(ax, x="", y="", filename="plot.png"):
    ax.set_xlabel(x)
    ax.set_ylabel(y)

    fig = ax.get_figure()  # Get the parent figure from ax
    fig.tight_layout()
    fig.savefig(filename)
    plt.clf()

# Main
try:
    QUERY = """
    SELECT event_time, price::numeric AS price, event_type, user_id
    FROM customers
    WHERE event_type = 'purchase'
    """
    df = get_data(QUERY)
    plt.figure(figsize=(8, 6))
    sns.set_theme(style="darkgrid")

    # Print stats
    for k, v in df['price'].describe().items():
        print(f"{k}: {v:>15.6f}")

    # Box plot 1
    marker = dict(marker='D', markerfacecolor='dimgray', markersize=6, linestyle='none')
    ax1 = sns.boxplot(x=df['price'], flierprops=marker)
    save_plot(ax1, x="price", filename="box1.png")

    # Box plot 2
    ax2 = sns.boxplot(
        x=df['price'],
        color="mediumseagreen",
        boxprops=dict(facecolor="mediumseagreen", edgecolor="black"),
        flierprops=dict(marker=''), # Hide outliers
    )
    ax2.set_xlim(-1, 13)
    save_plot(ax2, x="price", filename="box2.png")

    # Box plot 3...?
    avg_basket = df.groupby(['user_id', 'event_time'])['price'].mean()
    ax3 = sns.boxplot(x=avg_basket)
    save_plot(ax3, filename="box3.png")

except Exception as e:
    print(f"Error: {e}")
