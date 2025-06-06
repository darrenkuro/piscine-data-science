from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import pandas as pd
import seaborn as sns
import matplotlib.ticker as ticker

# Config
DB_NAME = "piscineds"
DB_USER = "dlu"
DB_PASS = "mysecretpassword"
DB_HOST = "localhost"

# Helpers
def get_data(query="SELECT * FROM customers"):
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
    return pd.read_sql(query, engine)

def save_plot(ax, x="", y="", filename="plot.png", title=""):
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title)

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

    spent = df.groupby('user_id')['price'].sum().to_frame()
    scaler = MinMaxScaler(feature_range=(0, 68))
    X = scaler.fit_transform(spent)
    wcss = [] # Within-cluster sum of squares (basically WCSS/n = variance)
    K_RANGE = range(1, 11)
    for k in K_RANGE:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)

    ax = sns.lineplot(x=list(K_RANGE), y=wcss)
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=False))
    ax.ticklabel_format(style='plain', axis='y')
    ax.set_xlim(0.5, 11)
    ax.set_xticks(range(2, 11, 2))
    save_plot(ax, x="number of clusters", filename="elbow.png", title="The Elbow Method")

except Exception as e:
    print(f"Error: {e}")