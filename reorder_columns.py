import pandas as pd

# Load the existing cleaned file
file_path = r"C:\Users\LENOVO\Desktop\soil_project\Data science project\SoilHealthDataScraper\data\processed\final_cleaned_data.csv"
df = pd.read_csv(file_path)

# Reorder columns: bring important metadata to the front
meta_cols = ['Year','State', 'District','Village','Block']
other_cols = [col for col in df.columns if col not in meta_cols]
new_order = meta_cols + other_cols

# Reorder and save again
df = df[new_order]
df.to_csv(file_path, index=False)

print("✅ Columns reordered. Final file updated.")
