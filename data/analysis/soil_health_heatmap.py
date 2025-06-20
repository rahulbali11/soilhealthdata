import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load the final cleaned data
file_path = r"C:\Users\LENOVO\Desktop\soil_project\Data science project\SoilHealthDataScraper\data\processed\final_cleaned_data.csv"
df = pd.read_csv(file_path)

# Create folder to save output if not exists
output_dir = os.path.join(os.path.dirname(file_path), "..", "analysis")
os.makedirs(output_dir, exist_ok=True)

# Filter nutrient columns (excluding meta columns)
meta_cols = ['Year', 'State', 'District', 'Village', 'Block']
nutrient_cols = [col for col in df.columns if col not in meta_cols]

# Group by State and sum nutrient counts
state_summary = df.groupby("State")[nutrient_cols].sum()

# Normalize values (optional)
normalized = state_summary.div(state_summary.max(axis=0), axis=1)

# Plot heatmap
plt.figure(figsize=(18, 12))
sns.heatmap(normalized, cmap="YlGnBu", annot=False, linewidths=0.5)

plt.title("Soil Nutrient Status by State (Normalized Heatmap)", fontsize=16)
plt.xlabel("Nutrients")
plt.ylabel("State")

# Save the figure
plot_path = os.path.join(output_dir, "soil_health_heatmap.png")
plt.tight_layout()
plt.savefig(plot_path)
plt.show()

print(f"✅ Heatmap saved at: {plot_path}")
