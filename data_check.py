import pandas as pd

df = pd.read_csv("data/loan.csv")

print("Total rows and columns:", df.shape)

print("\nColumn names:")
print(df.columns)gi