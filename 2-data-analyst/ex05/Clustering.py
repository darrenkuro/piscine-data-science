from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
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

def label_segment(row):
    if row['recency'] < 0.5 and row['frequency'] <= 5:
        return "new customers"
    elif row['recency'] < 1 and row['frequency'] > 20:
        return "loyal customers: gold"
    elif row['recency'] >= 2 and row['frequency'] <= 10:
        return "inactive"
    else:
        return "loyal customers: silver"

# Main
try:
    QUERY = """
    SELECT event_time, price::numeric AS price, user_id, event_type
    FROM customers
    WHERE event_type = 'purchase'
    """
    df = get_data(QUERY)
    df['event_time'] = pd.to_datetime(df['event_time'])
    latest_date = df['event_time'].max() # Reference date

    # RFM
    rfm = df.groupby('user_id').agg(
        recency=('event_time', lambda x: (latest_date - x.max()).days / 30),  # Months
        frequency=('price', 'count'),
        monetary=('price', 'sum')
    )

    X = rfm[['recency', 'frequency', 'monetary']]
    kmeans = KMeans(n_clusters=4, random_state=42, n_init='auto')
    rfm['cluster'] = kmeans.fit_predict(X)
    cluster_stats = rfm.groupby('cluster').agg(
        median_recency=('recency', 'median'),
        median_frequency=('frequency', 'median'),
        avg_monetary=('monetary', 'mean'),
    )

    rfm['segment'] = rfm.apply(label_segment, axis=1)
    cluster_stats = rfm.groupby('segment').agg(
        median_recency=('recency', 'median'),
        median_frequency=('frequency', 'median'),
        avg_monetary=('monetary', 'mean')
    ).reset_index()

    plt.figure(figsize=(8, 6))
    ax1 = sns.scatterplot(
        data=cluster_stats,
        x='median_recency',
        y='median_frequency',
        size='avg_monetary',
        sizes=(200, 2000),
        hue='segment',
        legend=False,
        alpha=0.6
    )

    # Annotation
    for i, row in cluster_stats.iterrows():
        label = row['segment']
        value = round(row['avg_monetary'], 2)
        ax1.text(row['median_recency'] + 0.1, row['median_frequency'], f'Average "{label}": {value} ₳', fontsize=10)

    save_plot(ax1, x="Median Recency (month)", y="Median Frequency", filename="bubble.png")

    # Plot 2
    segment_counts = rfm['segment'].value_counts().reset_index()
    segment_counts.columns = ['segment', 'count']
    segment_counts = segment_counts.sort_values(by='count', ascending=False)

    plt.figure(figsize=(12, 6))
    ax2 = sns.barplot(
        data=segment_counts,
        y='segment',
        x='count',
        hue='segment',
        palette='pastel',
        legend=False
    )

    # Annotation
    for i, row in segment_counts.iterrows():
        ax2.text(row['count'] + 200, i, str(row['count']), va='center')
    save_plot(ax2, x="number of customers", filename="bar.png")

except Exception as e:
    print(f"Error: {e}")