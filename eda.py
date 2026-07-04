from utils.data_loader import load_data

df = load_data()

print("=" * 60)
print("DATASET SHAPE")
print("=" * 60)
print(df.shape)

print("\n")

print("=" * 60)
print("COLUMN NAMES")
print("=" * 60)
print(df.columns.tolist())

print("\n")

print("=" * 60)
print("MISSING VALUES")
print("=" * 60)
print(df.isnull().sum())

print("\n")

print("=" * 60)
print("NUMERIC SUMMARY")
print("=" * 60)
print(df.describe())

print("\n")

print("=" * 60)
print("UNIQUE COUNTRIES")
print("=" * 60)
print(df["country_txt"].nunique())

print("\n")

print("=" * 60)
print("UNIQUE REGIONS")
print("=" * 60)
print(df["region_txt"].nunique())

print("\n")

print("=" * 60)
print("UNIQUE ATTACK TYPES")
print("=" * 60)
print(df["attacktype1_txt"].unique())

print("\n")

print("=" * 60)
print("TOP 10 COUNTRIES")
print("=" * 60)
print(df["country_txt"].value_counts().head(10))

print("\n")

print("=" * 60)
print("TOP 10 ATTACK TYPES")
print("=" * 60)
print(df["attacktype1_txt"].value_counts().head(10))

print("\n")

print("=" * 60)
print("TOP 10 TERRORIST GROUPS")
print("=" * 60)
print(df["gname"].value_counts().head(10))