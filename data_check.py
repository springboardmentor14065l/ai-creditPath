import pandas as pd


df = pd.read_csv("data/final_features.csv")

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns)

print("\nData types:")
print(df.dtypes)

print("\nSample data:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())