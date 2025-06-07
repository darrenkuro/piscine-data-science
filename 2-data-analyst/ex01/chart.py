from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

def style_axis(ax, index):
    ax.xaxis.set_major_locator(mdates.MonthLocator()) # Limit label counts
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b')) # X axis label
    ax.set_xlim(index.min(), index.max()) # Close gaps

# Main
try:
    QUERY = """
    SELECT event_time, price::numeric AS price, event_type, user_id
    FROM customers
    WHERE event_type = 'purchase'
    """
    df = get_data(QUERY)
    df['event_time'] = pd.to_datetime(df['event_time'])
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['date'] = df['event_time'].dt.date
    sns.set_theme(style="darkgrid")

    # Chart 1: Customers per day
    daily_customers = df.groupby('date')['user_id'].nunique() # Only count unique customers
    ax1 = daily_customers.plot(figsize=(10, 6), kind='line')
    style_axis(ax1, daily_customers.index)
    save_plot(ax1, y="Number of customers", filename="chart1.png")

    # Chart 2: Total sales per month
    df['month'] = df['event_time'].dt.to_period('M')
    monthly_sales = df.groupby('month')['price'].sum() / 1_000_000  # Convert to millions
    monthly_sales.index = monthly_sales.index.strftime('%b')  # Group index name
    ax2 = monthly_sales.plot(figsize=(10, 6), kind='bar', color='lightsteelblue', width=0.8)
    ax2.set_xticklabels(monthly_sales.index, rotation=0)  # Set x labels horizontal
    save_plot(ax2, x="month", y="total sales in million of ₳", filename="chart2.png")

    # Chart 3: Average spending per customer
    daily_sales = df.groupby('date')['price'].sum()
    daily_avg = daily_sales / daily_customers
    ax3 = daily_avg.plot(figsize=(10, 6), kind='area', color='lightsteelblue')
    style_axis(ax3, daily_avg.index)
    save_plot(ax3, y="average spend/customers in ₳", filename="chart3.png")

except Exception as e:
    print(f"Error: {e}")
