import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set(style="whitegrid")

# Load the data
base_path = r"C:\Users\LENOVO\Desktop\soil_project\Data science project\SoilHealthDataScraper"
data_path = os.path.join(
    base_path, "data", "processed", "final_cleaned_data.csv")
df = pd.read_csv(data_path)

# Create plots folder
plots_dir = os.path.join(base_path, "analysis", "plots")
os.makedirs(plots_dir, exist_ok=True)

# List of key nutrients
macro_nutrients = ['Nitrogen_Low_Macro',
                   'Phosphorus_Low_Macro', 'Potassium_Low_Macro']
micro_nutrients = ['Zinc_Deficient_Macro',
                   'Iron_Deficient_Macro', 'Boron_Deficient_Macro']
all_deficiencies = macro_nutrients + micro_nutrients

### 1. Top 5 States with Highest Soil Deficiencies ###


def plot_top5_states(nutrient):
    top_states = df.groupby("State")[nutrient].sum(
    ).sort_values(ascending=False).head(5)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=top_states.values, y=top_states.index, palette="Reds_r")
    plt.title(f"Top 5 States with Highest {nutrient.replace('_', ' ')}")
    plt.xlabel("Total Deficiency Count")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, f"top5_states_{nutrient}.png"))
    plt.close()


for nutrient in all_deficiencies:
    plot_top5_states(nutrient)

### 2. Bottom 5 States with Least Soil Deficiencies ###


def plot_bottom5_states(nutrient):
    bottom_states = df.groupby("State")[nutrient].sum().sort_values().head(5)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=bottom_states.values,
                y=bottom_states.index, palette="Greens")
    plt.title(f"Bottom 5 States with Least {nutrient.replace('_', ' ')}")
    plt.xlabel("Total Deficiency Count")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, f"bottom5_states_{nutrient}.png"))
    plt.close()


for nutrient in all_deficiencies:
    plot_bottom5_states(nutrient)

### 3. Best Year for Each Nutrient (Lowest total deficiency) ###


def best_year_trend(nutrient):
    yearly = df.groupby("Year")[nutrient].sum().sort_values()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=yearly, marker="o")
    plt.title(f"Yearly Trend of {nutrient.replace('_', ' ')}")
    plt.ylabel("Total Deficiency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, f"yearly_trend_{nutrient}.png"))
    plt.close()


for nutrient in all_deficiencies:
    best_year_trend(nutrient)

### 4. Top & Bottom 5 Districts Based on Total Deficiency ###
df['Total_Deficiency'] = df[all_deficiencies].sum(axis=1)
top_districts = df.groupby(['State', 'District'])[
    'Total_Deficiency'].sum().sort_values(ascending=False).head(5)
bottom_districts = df.groupby(['State', 'District'])[
    'Total_Deficiency'].sum().sort_values().head(5)

# Plot top & bottom districts
plt.figure(figsize=(10, 6))
sns.barplot(x=top_districts.values, y=[
            f"{s}, {d}" for s, d in top_districts.index], palette="Reds_r")
plt.title("Top 5 Districts with Highest Soil Deficiency")
plt.xlabel("Total Deficiency")
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "top5_districts_deficiency.png"))
plt.close()

plt.figure(figsize=(10, 6))
sns.barplot(x=bottom_districts.values, y=[
            f"{s}, {d}" for s, d in bottom_districts.index], palette="Greens")
plt.title("Bottom 5 Districts with Least Soil Deficiency")
plt.xlabel("Total Deficiency")
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "bottom5_districts_deficiency.png"))
plt.close()

### 5. Suggestions: Areas for Improvement (Districts with High Deficiency) ###
suggestions = top_districts.reset_index()
suggestions.columns = ['State', 'District', 'Total_Deficiency']
suggestions.to_csv(os.path.join(base_path, "analysis",
                   "districts_to_improve.csv"), index=False)
print("✅ All visualizations saved in 'analysis/plots' and suggestions saved as 'districts_to_improve.csv'")
