import pandas as pd


df = pd.read_csv('shopping_trends_updated.csv')

# Define the age ranges
bins = [18, 28, 38, 48, 58, 68, 78]
labels = ['18-27', '28-37', '38-47', '48-57', '58-67', '68-77']

# Create the "Age Range" column
df['Age Range'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

df.to_csv('shopping_trends_updated_copy.csv', index=False)