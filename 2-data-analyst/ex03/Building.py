from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

    # Histo 1
    freq = df.groupby('user_id').size()  # Purchase per user
    ax1 = sns.histplot(freq, bins=np.arange(1, 40, 7.5), kde=False, color='lightsteelblue')
    ax1.set_xlim(-1, 40)
    ax1.set_xticks(range(0, 40, 10))
    save_plot(ax1, x="frequency", y="customers", filename="histo1.png")

    # Histo 2
    spent = df.groupby('user_id')['price'].sum()  # Total spent per user
    ax2 = sns.histplot(spent, bins=range(-26, 225, 50), kde=False, color='lightsteelblue')
    ax2.set_xlim(-50, 250)
    ax2.set_xticks(range(0, 250, 50))
    save_plot(ax2, x="monetary value in ₳", y="customers", filename="histo2.png")

except Exception as e:
    print(f"Error: {e}")
