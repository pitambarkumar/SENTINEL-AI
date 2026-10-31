import pandas as pd

# Load the real fraud detection dataset
df = pd.read_csv("creditcard.csv")

print("\n===== SENTINEL AI DATASET =====")

print("\nTotal Rows and Columns:")
print(df.shape)

print("\nFirst 5 Transactions:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum().sum())

print("\nFraud vs Genuine Transactions:")
print(df["Class"].value_counts())

print("\nFraud Percentage:")
print(round(df["Class"].mean() * 100, 4), "%")

print("\nDataset Exploration Complete!")