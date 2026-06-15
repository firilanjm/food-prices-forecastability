import pandas as pd
import numpy as np

# =====================================
# FILES
# =====================================

files = [
    "data/2021.xlsx",
    "data/2022.xlsx",
    "data/2023.xlsx",
    "data/2024.xlsx",
    "data/2025.xlsx"
]

# =====================================
# READ FILES
# =====================================

dfs = []

for file in files:

    df = pd.read_excel(file)

    print(f"\n{file}")
    print(df.shape)

    dfs.append(df)

# =====================================
# CHECK COMMODITIES
# =====================================

print("\nCommodity Names:")
print(dfs[0]["Komoditas (Rp)"].tolist())

# =====================================
# KEEP MAIN COMMODITIES
# =====================================

main_commodities = [
    "Beras",
    "Daging Ayam",
    "Daging Sapi",
    "Telur Ayam",
    "Bawang Merah",
    "Bawang Putih",
    "Cabai Merah",
    "Cabai Rawit",
    "Gula Pasir",
    "Minyak Goreng"
]

processed = []

# =====================================
# CLEAN EACH FILE
# =====================================

for df in dfs:

    # remove numbering column
    if "No" in df.columns:
        df = df.drop(columns=["No"])

    # remove extra spaces
    df["Komoditas (Rp)"] = (
        df["Komoditas (Rp)"]
        .astype(str)
        .str.strip()
    )

    # KEEP ONLY MAIN COMMODITIES
    df = df[
        df["Komoditas (Rp)"]
        .isin(main_commodities)
    ]

    # use commodity as index
    df = df.set_index("Komoditas (Rp)")

    processed.append(df)

# =====================================
# COMBINE 2021-2025
# =====================================

master = pd.concat(
    processed,
    axis=1
)

# =====================================
# REMOVE DUPLICATE DATE COLUMNS
# =====================================

master = master.loc[
    :,
    ~master.columns.duplicated()
]

# =====================================
# TRANSPOSE
# =====================================

master = master.T

# =====================================
# DATE INDEX
# =====================================

master.index = pd.to_datetime(
    master.index,
    dayfirst=True,
    errors="coerce"
)

# remove invalid dates
master = master[master.index.notna()]

# =====================================
# SORT
# =====================================

master = master.sort_index()

# =====================================
# MOVE DATE TO COLUMN
# =====================================

master = master.reset_index()

master = master.rename(
    columns={"index": "Date"}
)

# =====================================
# CLEAN NUMBERS
# =====================================

for col in master.columns[1:]:

    master[col] = (
        master[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("-", "", regex=False)
        .str.strip()
    )

    master[col] = pd.to_numeric(
        master[col],
        errors="coerce"
    )

# =====================================
# MISSING VALUES
# =====================================

print("\nMissing Values:")
print(master.isna().sum())

# interpolate

price_cols = master.columns[1:]

master[price_cols] = (
    master[price_cols]
    .interpolate(method="linear")
)

master[price_cols] = (
    master[price_cols]
    .ffill()
    .bfill()
)

# =====================================
# FINAL CHECK
# =====================================

print("\nShape:")
print(master.shape)

print("\nHead:")
print(master.head())

print("\nInfo:")
print(master.info())

# =====================================
# SAVE CLEAN DATA
# =====================================

master.to_csv(
    "data/food_prices_2021_2025_clean.csv",
    index=False
)

print("\nSaved:")
print("data/food_prices_2021_2025_clean.csv")

# # =====================================
# # SUMMARY STATS
# # =====================================

# summary = pd.DataFrame()

# summary["Mean"] = (
#     master.drop("Date", axis=1)
#     .mean()
# )

# summary["SD"] = (
#     master.drop("Date", axis=1)
#     .std()
# )

# summary["CV"] = (
#     summary["SD"] /
#     summary["Mean"]
# )

# summary = summary.sort_values(
#     "CV",
#     ascending=False
# )

# print("\nVolatility Ranking")
# print(summary)

# summary.to_csv(
#     "commodity_summary.csv"
# )

# # =====================================
# # CORRELATION
# # =====================================

# corr = (
#     master
#     .drop("Date", axis=1)
#     .corr()
# )

# corr.to_csv(
#     "commodity_correlation.csv"
# )

# print("\nSaved:")
# print("commodity_summary.csv")
# print("commodity_correlation.csv")