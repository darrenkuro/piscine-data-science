from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

# Config
DB_NAME = "piscineds"
DB_USER = "dlu"
DB_PASS = "mysecretpassword"
DB_HOST = "localhost"
QUERY = "SELECT event_type FROM customers"
OUTPUT_FILE = "pie.png"


# Main
try:
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
    df = pd.read_sql(QUERY, engine)

    counts = df['event_type'].value_counts()
    counts.plot.pie(autopct='%1.1f%%', title='User Activity Chart')
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE)
except Exception as e:
    print(f"Error: {e}")