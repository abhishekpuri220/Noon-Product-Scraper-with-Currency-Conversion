import pandas as pd

# Loading the script into dataframe
df = pd.read_csv("scraped_noon_data.csv")

# 1. Most Expensive product
most_expensive = df.loc[df["Price"].idxmax()]
print(f"Most Expensive Product: {most_expensive['Name']} - ₹{most_expensive['Price']}")

# 2. Cheapest Product
cheapest = df.loc[df['Price'].idxmin()]
print(f"Cheapest Product: {cheapest['Name']} - ₹{cheapest['Price']}")

# 3. Number of Products from Each Brand
brand_counts = df['Brand'].value_counts()
print("\nNumber of Products from Each Brand:")
print(brand_counts)