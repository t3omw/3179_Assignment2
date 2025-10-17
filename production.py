import pandas as pd
from sklearn.preprocessing import MinMaxScaler

start_year = 2001
end_year = 2010

# --- 1. Load Herbs data and filter to 2001-2010 ---
df_herbs = pd.read_csv("planted-area-and-production-of-herbs-malaysia-2001-2019.csv")
df_herbs = df_herbs[(df_herbs['Year'] >= start_year) & (df_herbs['Year'] <= end_year)].copy()
df_herbs_final = df_herbs[['Year', 'Production (Tonnes)']].rename(columns={'Production (Tonnes)': 'Herbs Production (Tonnes)'})

# --- 2. Load Fruits data, filter, and aggregate production ---
df_fruits = pd.read_csv("planted-area-and-production-of-selected-fruits-malaysia-2000-20.csv")
df_fruits['Year'] = df_fruits['Year'].astype(int) # Ensure Year is integer for filtering
df_fruits = df_fruits[(df_fruits['Year'] >= start_year) & (df_fruits['Year'] <= end_year)].copy()

# Aggregate all fruit production by summing 'Production (Tonnes)'
df_fruits_agg = df_fruits.groupby('Year')['Production (Tonnes)'].sum().reset_index()
df_fruits_agg = df_fruits_agg.rename(columns={'Production (Tonnes)': 'Fruits Production (Tonnes)'})

# --- 3. Combine Data (Original Figures) ---
df_original = pd.merge(df_herbs_final, df_fruits_agg, on='Year')

# --- 4. Standardize (Min-Max Scaling) ---

# Prepare data for scaling (exclude 'Year' column)
df_data_to_scale = df_original[['Herbs Production (Tonnes)', 'Fruits Production (Tonnes)']].copy()

# Initialize the scaler
scaler = MinMaxScaler()

# Apply min-max scaling
df_standardized = pd.DataFrame(
    scaler.fit_transform(df_data_to_scale),
    columns=df_data_to_scale.columns,
)

# Insert the Year column back into the standardized dataframe
df_standardized.insert(0, 'Year', df_original['Year'])

# --- 5. Output to CSV Files ---

# 5a. Output Original Data
original_output_file = 'malaysia_agri_production_original_2001_2010.csv'
df_original.to_csv(original_output_file, index=False, float_format='%.0f')
print(f"Original production data saved to: {original_output_file}")

# 5b. Output Standardized Data
standardized_output_file = 'malaysia_agri_production_standardized_2001_2010.csv'
df_standardized.to_csv(standardized_output_file, index=False, float_format='%.4f')
print(f"Standardized production data saved to: {standardized_output_file}")