from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

# Config
DB_NAME = "piscineds"
DB_USER = "dlu"
DB_PASS = "mysecretpassword"
DB_HOST = "localhost"

# Helpers
def get_data(query: str = "SELECT * FROM customers"):
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
    return pd.read_sql(query, engine)

def save_plot(ax, x: str = "", y: str = "", filename: str = "plot.png") -> None:
    ax.set_xlabel(x)
    ax.set_ylabel(y)

    fig = ax.get_figure()  # Get the parent figure from ax
    fig.tight_layout()
    fig.savefig(filename)
    plt.clf()

# Main
try:
    df = get_data(query="SELECT event_type FROM customers")

    counts = df['event_type'].value_counts()
    ax = counts.plot.pie(autopct='%1.1f%%')
    save_plot(ax, filename="pie.png")
except Exception as e:
    print(f"Error: {e}")