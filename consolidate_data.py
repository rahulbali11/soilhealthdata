import pandas as pd
import os

# Define paths
base_dir = r"C:\Users\LENOVO\Desktop\soil_project\Data science project\SoilHealthDataScraper"
raw_data_dir = os.path.join(base_dir, "data", "raw")
processed_dir = os.path.join(base_dir, "data", "processed")
os.makedirs(processed_dir, exist_ok=True)

consolidated_csv = os.path.join(processed_dir, "consolidated_data.csv")
final_output_csv = os.path.join(processed_dir, "final_cleaned_data.csv")

# Collect all dataframes
all_data = []

# Step 1: Loop through raw data and collect valid CSVs
for year in os.listdir(raw_data_dir):
    year_path = os.path.join(raw_data_dir, year)
    if not os.path.isdir(year_path): continue

    for state in os.listdir(year_path):
        state_path = os.path.join(year_path, state)
        if not os.path.isdir(state_path): continue

        for district in os.listdir(state_path):
            district_path = os.path.join(state_path, district)
            if not os.path.isdir(district_path): continue

            for file in os.listdir(district_path):
                if file.endswith(".csv"):
                    file_path = os.path.join(district_path, file)
                    try:
                        df = pd.read_csv(file_path)
                        if df.empty or df.columns.size == 0:
                            continue
                        df["Year"] = year
                        df["State"] = state
                        df["District"] = district
                        df["Block_File"] = file
                        all_data.append(df)
                    except Exception as e:
                        print(f"❌ Failed to read {file_path}: {e}")

# Step 2: Combine & clean
if not all_data:
    print("⚠️ No valid data files found.")
    exit()

combined_df = pd.concat(all_data, ignore_index=True)
combined_df.columns = [col.strip().title().replace(" ", "_") for col in combined_df.columns]

nutrient_cols = ['N', 'P', 'K', 'Ph', 'Ec', 'Oc', 'Zn', 'Fe', 'Cu', 'Mn']
existing_cols = combined_df.columns
for col in nutrient_cols:
    if col in existing_cols:
        combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')

# Drop rows with missing all NPK
if all(col in existing_cols for col in ['N', 'P', 'K']):
    combined_df = combined_df.dropna(subset=['N', 'P', 'K'], how='all')

# Save consolidated file
combined_df.to_csv(consolidated_csv, index=False)
print(f"\n✅ Consolidated data saved to:\n{consolidated_csv}")

# Step 3: Merge Macro & Micro into final dataset
df = combined_df.copy()
df["Type"] = df["Block_File"].apply(lambda x: "Macro" if "_macro.csv" in str(x) else "Micro")
df["Block"] = df["Block_File"].str.extract(r"^(.*?)\s*-\s*")

macro_df = df[df["Type"] == "Macro"].copy()
micro_df = df[df["Type"] == "Micro"].copy()

merge_keys = ["Year", "State", "District", "Block", "Village"]

macro_df = macro_df.drop(columns=["Block_File", "Type"])
micro_df = micro_df.drop(columns=["Block_File", "Type"])

final_df = pd.merge(
    macro_df, micro_df,
    on=merge_keys,
    suffixes=("_Macro", "_Micro"),
    how="outer"
)

final_df.to_csv(final_output_csv, index=False)
print(f"\n✅ Final cleaned & merged data saved to:\n{final_output_csv}")
