#impoort dataset
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

#load the dataset
data=pd.read_csv("Online Sales Data.csv")

#create sqlite database and insert data
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

#create the sales table(drop if already exists)
cursor.execute("DROP table if EXISTS sales")

#create sales table
cursor.execute("""
   CREATE TABLE sales (
    "Transaction ID" INTEGER PRIMARY KEY,
    "Date" TEXT,
    "Product Category" TEXT,
    "Product Name" TEXT,
    "Units Sold" INTEGER,
    "Unit Price" REAL,
    "Total Revenue" REAL,
    "Region" TEXT,
    "Payment Method" TEXT
);
""")

#Insert all data into sales table
data.to_sql("sales", conn, if_exists="replace", index=False)

# Commit changes
conn.commit()

#Run SQL queries
'''
SELECT 
      "Product Name" AS Product,
      SUM("Units Sold") AS Total_Quantity,
      SUM("Total Revenue") AS Revenue
FROM sales
GROUP BY "Product Name"
ORDER BY Revenue DESC
'''

summary_df = pd.read_sql_query('''
SELECT 
      "Product Name" AS Product,
      SUM("Units Sold") AS Total_Quantity,
      SUM("Total Revenue") AS Revenue
FROM sales
GROUP BY "Product Name"
ORDER BY Revenue DESC
''', conn)

# Display the summary DataFrame
print(summary_df)

#plot sales revenue by product
plt.figure(figsize=(12, 6))
plt.bar(summary_df['Product'], summary_df['Revenue'], color='blue')
plt .xticks(rotation=45, ha='right')
plt.xlabel('Product')
plt.ylabel('Revenue')
plt.title('Sales Revenue by Product')
plt.tight_layout()
plt.show()

#save the figure
plt.savefig("sales_revenue_by_product.png")

#close the database connection
conn.close()


