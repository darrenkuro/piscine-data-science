from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Config
DB_NAME = "piscineds"
DB_USER = "dlu"
DB_PASS = "mysecretpassword"
DB_HOST = "localhost"
QUERY = """
SELECT event_time, price::numeric AS price, event_type, user_id
FROM customers
WHERE event_type = 'purchase'
"""

# Helpers
def style_axis(ax, index):
    ax.xaxis.set_major_locator(mdates.MonthLocator()) # Limit label counts
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b')) # X axis label
    ax.set_xlim(index.min(), index.max()) # Close gaps

def save_chart(ax, xlabel, ylabel, filename):
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plt.tight_layout()
    plt.savefig(filename)
    plt.clf()

# Main
try:
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
    df = pd.read_sql(QUERY, engine)
    df['event_time'] = pd.to_datetime(df['event_time'])
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['date'] = df['event_time'].dt.date

    # Chart 1: Customers per day
    daily_customers = df.groupby('date')['user_id'].nunique() # Only count unique customers
    ax1 = daily_customers.plot(figsize=(10, 6), kind='line')
    style_axis(ax1, daily_customers.index)
    save_chart(ax1, "", "Number of customers", "chart1.png")

    # Chart 2: Total sales per month
    df['month'] = df['event_time'].dt.to_period('M')
    monthly_sales = df.groupby('month')['price'].sum() / 1_000_000  # Convert to millions
    monthly_sales.index = monthly_sales.index.strftime('%b')  # Group index name
    ax2 = monthly_sales.plot(figsize=(6, 6), kind='bar')
    save_chart(ax2, "month", "total sales in million of ₳", "chart2.png")

    # Chart 3: Average spending per customer
    daily_sales = df.groupby('date')['price'].sum()
    daily_avg = daily_sales / daily_customers
    ax3 = daily_avg.plot(kind='area', figsize=(10, 6), color='lightsteelblue')
    style_axis(ax3, daily_avg.index)
    save_chart(ax3, "", "average spend/customers in ₳", "chart3.png")

except Exception as e:
    print(f"Error: {e}")
