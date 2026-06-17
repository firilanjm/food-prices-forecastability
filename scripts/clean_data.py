# clean_data.py

import pandas as pd

# =====================================================
# Commodity Translation
# =====================================================

commodity_map = {
    "Beras": "Rice",
    "Daging Ayam": "Chicken",
    "Daging Sapi": "Beef",
    "Telur Ayam": "Eggs",
    "Bawang Merah": "Shallots",
    "Bawang Putih": "Garlic",
    "Cabai Merah": "Red Chili",
    "Cabai Rawit": "Bird's Eye Chili",
    "Minyak Goreng": "Cooking Oil",
    "Gula Pasir": "Sugar"
}

# =====================================================
# Files
# =====================================================

files = [
    "../data/raw/2021.xlsx",
    "../data/raw/2022.xlsx",
    "../data/raw/2023.xlsx",
    "../data/raw/2024.xlsx",
    "../data/raw/2025.xlsx"
]

# =====================================================
# Processing Function
# =====================================================

def process_file(file):

    print(f"Processing {file}")

    df = pd.read_excel(file)

    # Keep selected commodities
    df = df[
        df["Komoditas (Rp)"].isin(
            commodity_map.keys()
        )
    ]

    # Translate names
    df["Komoditas (Rp)"] = (
        df["Komoditas (Rp)"]
        .map(commodity_map)
    )

    # Drop unnecessary column
    df = df.drop(
        columns=["No"],
        errors="ignore"
    )

    # Commodity names become columns
    df = df.set_index(
        "Komoditas (Rp)"
    )

    # Transpose
    df = df.T

    # Date index
    df.index = pd.to_datetime(
        df.index,
        dayfirst=True,
        errors="coerce"
    )

    # Remove invalid dates
    df = df[
        ~df.index.isna()
    ]

    # Reset index
    df = df.reset_index()

    df = df.rename(
        columns={"index": "Date"}
    )

    return df


# =====================================================
# Combine All Years
# =====================================================

all_data = []

for file in files:

    temp = process_file(file)

    all_data.append(temp)

master = pd.concat(
    all_data,
    ignore_index=True
)

# =====================================================
# Cleaning
# =====================================================

master = master.sort_values(
    "Date"
)

master = master.drop_duplicates(
    subset="Date"
)

master = master.reset_index(
    drop=True
)

# Forward fill missing values
master = master.ffill()

# =====================================================
# Save
# =====================================================

master.to_csv(
    "../data/processed/food_prices_2021_2025_clean.csv",
    index=False
)

print("\nDataset Saved!")
print(master.shape)

print("\nColumns:")
print(master.columns.tolist())

print("\nFirst Rows:")
print(master.head())