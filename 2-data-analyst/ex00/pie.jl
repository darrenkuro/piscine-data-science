import Pkg
Pkg.add(["LibPQ", "DataFrames", "Plots"])

using LibPQ
using DataFrames
using Plots

conn = LibPQ.Connection("host=localhost user=dlu dbname=piscineds password=mysecretpassword")

df = DataFrame(LibPQ.execute(conn, """
    SELECT event_type, COUNT(*) AS count
    FROM customers
    GROUP BY event_type
    ORDER BY count DESC;
"""))

LibPQ.close(conn)

pie(df.event_type, df.count, title="Event Distribution")
savefig("pie_chart.png")