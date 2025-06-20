# Soil Health Data Analysis

This project involves scraping, consolidating, and analyzing soil health data from the Government of India Soil Health Dashboard. The goal is to extract meaningful insights and identify regional trends related to soil nutrients across Indian districts and states.

---

## 🌍 Project Overview

### ✍️ Objectives

- Scrape Macro and Micro nutrient soil data for all available years.
- Consolidate the scattered CSVs into a clean master dataset.
- Perform Exploratory Data Analysis (EDA).
- Generate visualizations showing soil health trends.
- Identify top/bottom performing states and districts for each nutrient.

---

## 📂 Folder Structure

```
soil_project/
├── data/
│   ├── raw/                  # Scraped CSVs (state/district/block/year-wise)
│   └── processed/
│       └── final_cleaned_data.csv    # Cleaned, merged dataset
├── consolidate_data.py       # Combines and cleans all nutrient data
├── soil_health_analysis.py   # Performs EDA and generates insights/visuals
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/rahulbali11/soilhealthdata.git
cd soilhealthdata
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Consolidation Script

```bash
python consolidate_data.py
```

This script:

- Reads all nutrient CSVs in `data/raw/`
- Merges and cleans them
- Outputs the file: `data/processed/final_cleaned_data.csv`

### 4. Run Analysis Script

```bash
python soil_health_analysis.py
```

This script:

- Performs exploratory analysis
- Generates nutrient trend plots by state/year/district
- Saves charts in `analysis/`

---

## 📊 Key Insights Generated

- Top 5 and bottom 5 states by Nitrogen/Phosphorus/Potassium levels
- District-level nutrient heatmaps
- Year-wise trend of deficiency/sufficiency levels
- Identification of regions needing intervention

---

## 🌐 Data Source

[Soil Health Dashboard - Government of India](https://soilhealth.dac.gov.in/piechart)

---

## 🧱 Authors

- **Rahul Bali**

Feel free to fork, star, and explore further!

---

## 🚫 Disclaimer

This project is for educational and analytical purposes only. It is based on public data provided by government portals.
