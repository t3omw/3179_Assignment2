import pandas as pd
import numpy as np

# --- 0. Define Consistent State Names and Mapping ---
# Your provided list of state names
all_states_list = [
    'Johor', 'Kedah', 'Kelantan', 'Kuala Lumpur', 'Labuan', 'Melaka',
    'Negeri Sembilan', 'Pahang', 'Perak', 'Perlis', 'Pulau Pinang',
    'Putrajaya', 'Sabah', 'Sarawak', 'Selangor', 'Terengganu'
]

# Mapping from Flood Data STATE ID to your consistent State Names
# Based on cross-referencing, some states from your list are not in the flood data snippet.
flood_state_id_to_name_map = {
    108: 'Johor',
    102: 'Kedah',
    109: 'Kelantan',
    106: 'Negeri Sembilan',
    101: 'Pahang',
    105: 'Perak',
    104: 'Perlis',
    103: 'Pulau Pinang',
    113: 'Sabah',
    111: 'Sarawak',
    112: 'Terengganu'
}

# --- 1. Preprocess _MalaysiaFloodDataset_MalaysiaFloodDataset.csv ---
# This file provides annual/monthly rainfall and flood indicators (2000-2010)

print("Preprocessing _MalaysiaFloodDataset_MalaysiaFloodDataset.csv...")
flood_raw_df = pd.read_csv('_MalaysiaFloodDataset_MalaysiaFloodDataset.csv')

# Rename '0V' to 'NOV' for consistency
flood_raw_df = flood_raw_df.rename(columns={'0V': 'NOV'})

# Apply state name mapping
flood_raw_df['State Name'] = flood_raw_df['STATE'].map(flood_state_id_to_name_map)

# Drop rows where State Name couldn't be mapped (i.e., states not in our flood_state_id_to_name_map)
flood_raw_df.dropna(subset=['State Name'], inplace=True)

# --- 1.1. Prepare data for "Rainfall & Risk: A Decade of Floods in Malaysia (2000-2010)" ---
# Aggregated annual flood count and average annual rainfall by State and Year
annual_flood_summary = flood_raw_df.groupby(['State Name', 'YEAR']).agg(
    Annual_Flood_Count=('FLOOD', 'sum'), # Sum of 'FLOOD' per state per year
    Average_Annual_Rainfall=('ANNUAL RAINFALL', 'mean') # Mean of annual rainfall per state per year
).reset_index()

output_filename_1_1 = 'processed_flood_summary_by_state_year.csv'
annual_flood_summary.to_csv(output_filename_1_1, index=False)
print(f"  - Data for Rainfall & Risk saved to '{output_filename_1_1}'")

# --- 1.2. Prepare data for "Monsoon's Fury: Monthly Rainfall Patterns in Flood vs. Non-Flood Years" ---
# Pivot monthly rainfall, then calculate average for flood vs. non-flood years for each state
monthly_rainfall_cols = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
monthly_rainfall_df = flood_raw_df[['State Name', 'YEAR', 'FLOOD'] + monthly_rainfall_cols].copy()

# Melt monthly rainfall columns into a 'Month' and 'Rainfall' column
monthly_rainfall_long = monthly_rainfall_df.melt(
    id_vars=['State Name', 'YEAR', 'FLOOD'],
    value_vars=monthly_rainfall_cols,
    var_name='Month',
    value_name='Rainfall'
)

# Convert month names to ordered categorical for proper sorting in visualization
month_order = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
monthly_rainfall_long['Month'] = pd.Categorical(monthly_rainfall_long['Month'], categories=month_order, ordered=True)

# Calculate average monthly rainfall for flood years (FLOOD=1) and non-flood years (FLOOD=0)
avg_monthly_rainfall_patterns = monthly_rainfall_long.groupby(['State Name', 'Month', 'FLOOD'])['Rainfall'].mean().reset_index()

# You might want to pivot 'FLOOD' status to have 'Rainfall_Flood' and 'Rainfall_NoFlood' columns
avg_monthly_rainfall_pivot = avg_monthly_rainfall_patterns.pivot_table(
    index=['State Name', 'Month'],
    columns='FLOOD',
    values='Rainfall',
    aggfunc='mean' # Use mean as values are already means
).reset_index()
avg_monthly_rainfall_pivot.columns.name = None # Remove columns name 'FLOOD'

# Rename columns for clarity: 0 for no flood, 1 for flood
avg_monthly_rainfall_pivot = avg_monthly_rainfall_pivot.rename(columns={0: 'Avg_Rainfall_NoFlood', 1: 'Avg_Rainfall_Flood'})

output_filename_1_2 = 'processed_monthly_rainfall_patterns.csv'
avg_monthly_rainfall_pivot.to_csv(output_filename_1_2, index=False)
print(f"  - Data for Monsoon's Fury saved to '{output_filename_1_2}'")

# --- 2. Preprocess crops_state.csv ---
# This file provides annual planted area and production by crop type and state (2017-2022)

print("\nPreprocessing crops_state.csv...")
crops_df = pd.read_csv('crops_state.csv')

# Ensure 'date' is datetime and extract 'YEAR'
crops_df['date'] = pd.to_datetime(crops_df['date'])
crops_df['YEAR'] = crops_df['date'].dt.year

# Filter for Malaysia and specific crops if desired, ensure consistent state names
crops_df.loc[crops_df['state'] == 'Malaysia', 'State Name'] = 'Malaysia'
for state_name in all_states_list:
    if state_name != 'Malaysia': # 'Malaysia' is a special entry, not a specific state
        crops_df.loc[crops_df['state'] == state_name, 'State Name'] = state_name

# Drop rows where 'State Name' is not in our consistent list (e.g., specific W.P.s if not mapped or 'All States')
crops_df.dropna(subset=['State Name'], inplace=True)


# For "Harvests Under Threat": Merge with annual flood summary (2000-2010 data, crops 2017-2022)
# Note: The time periods don't perfectly align (2000-2010 floods, 2017-2022 crops).
# For a direct correlation, you'd ideally need overlapping data.
# For this preprocessing, we'll prepare crops data. If you get overlapping flood data, you can merge then.

# Select relevant crop types for visualization (e.g., paddy, industrial_crops, fruits)
selected_crop_types = ['paddy', 'industrial_crops', 'fruits', 'vegetables', 'coconut']
crops_filtered_df = crops_df[crops_df['crop_type'].isin(selected_crop_types)].copy()

# Aggregate production by state, year, and crop type (if multiple entries per year/crop)
crops_aggregated = crops_filtered_df.groupby(['State Name', 'YEAR', 'crop_type']).agg(
    Total_Production=('production', 'sum')
).reset_index()

output_filename_2 = 'processed_crops_production.csv'
crops_aggregated.to_csv(output_filename_2, index=False)
print(f"  - Data for Harvests Under Threat saved to '{output_filename_2}'")

# --- 3. Preprocess timber_products.csv ---
# This file provides annual timber production by product and state (mostly Malaysia)

print("\nPreprocessing timber_products.csv...")
timber_df = pd.read_csv('timber_products.csv')

# Ensure 'date' is datetime and extract 'YEAR'
timber_df['date'] = pd.to_datetime(timber_df['date'])
timber_df['YEAR'] = timber_df['date'].dt.year

# Standardize state name, focusing on 'Malaysia' for national overview
timber_df.loc[timber_df['state'] == 'Malaysia', 'State Name'] = 'Malaysia'
# Handle other specific states if you have state-level timber analysis, using your all_states_list
# For now, we'll keep it simple for national view.

# Aggregate total production by product and year for national level
timber_aggregated = timber_df[timber_df['State Name'] == 'Malaysia'].groupby(['YEAR', 'product']).agg(
    Total_Production=('production', 'sum')
).reset_index()

output_filename_3 = 'processed_timber_production_national.csv'
timber_aggregated.to_csv(output_filename_3, index=False)
print(f"  - Data for Timber's Struggle saved to '{output_filename_3}'")


# --- 4. Preprocess fish_landings.csv ---
# This file provides monthly fish landings by coast/state (2018-2023)

print("\nPreprocessing fish_landings.csv...")
fish_df = pd.read_csv('fish_landings.csv')

# Ensure 'date' is datetime and extract 'YEAR' and 'Month'
fish_df['date'] = pd.to_datetime(fish_df['date'])
fish_df['YEAR'] = fish_df['date'].dt.year
fish_df['Month'] = fish_df['date'].dt.strftime('%b').str.upper() # e.g., JAN, FEB

# Standardize state names in fish_df to match all_states_list if possible
# The fish_landings.csv uses 'All States' for coast, and specific state names for west/east/borneo
# We'll prioritize 'Malaysia' and then individual states if available.
fish_df.loc[fish_df['state'] == 'Malaysia', 'State Name'] = 'Malaysia'
fish_df.loc[fish_df['state'] == 'All States', 'State Name'] = fish_df['coast'].apply(
    lambda x: 'Peninsular Malaysia' if x in ['east', 'west'] else 'Borneo Malaysia' if x == 'borneo' else 'Malaysia'
) # This might require careful handling if 'All States' is aggregated across all states

# Let's simplify and aggregate for 'Malaysia' level or directly use specific state names if present
# For direct mapping, identify if any 'fish_df.state' entries match 'all_states_list'
fish_df['State Name'] = fish_df['state'].apply(lambda x: x if x in all_states_list else ('Malaysia' if x == 'Malaysia' else np.nan))
fish_df.dropna(subset=['State Name'], inplace=True) # Drop entries not directly mappable to our list

# Aggregate to annual total landings for 'Malaysia'
fish_annual_landings_national = fish_df[fish_df['State Name'] == 'Malaysia'].groupby('YEAR').agg(
    Total_Landings=('landings', 'sum')
).reset_index()

output_filename_4_1 = 'processed_fish_annual_landings_national.csv'
fish_annual_landings_national.to_csv(output_filename_4_1, index=False)
print(f"  - Data for Fish's Challenge (Annual National) saved to '{output_filename_4_1}'")

# Aggregate to monthly average landings for 'Malaysia' (for seasonal patterns)
fish_monthly_landings_national = fish_df[fish_df['State Name'] == 'Malaysia'].groupby('Month').agg(
    Avg_Monthly_Landings=('landings', 'mean')
).reset_index()
fish_monthly_landings_national['Month'] = pd.Categorical(fish_monthly_landings_national['Month'], categories=month_order, ordered=True)
fish_monthly_landings_national = fish_monthly_landings_national.sort_values('Month')

output_filename_4_2 = 'processed_fish_monthly_landings_national.csv'
fish_monthly_landings_national.to_csv(output_filename_4_2, index=False)
print(f"  - Data for Fish's Challenge (Monthly National) saved to '{output_filename_4_2}'")


# --- 5. Preprocess gdp_annual_real_supply.csv ---
# This file provides annual real GDP by economic sector (2015-2023)

print("\nPreprocessing gdp_annual_real_supply.csv...")
gdp_df = pd.read_csv('gdp_annual_real_supply.csv')

# Filter for absolute values ('abs' series) and relevant sectors ('p0' for total, 'p1' for agriculture)
gdp_filtered_df = gdp_df[
    (gdp_df['series'] == 'abs') &
    (gdp_df['sector'].isin(['p0', 'p1']))
].copy()

# Ensure 'date' is treated as 'YEAR'
gdp_filtered_df['YEAR'] = pd.to_datetime(gdp_filtered_df['date']).dt.year

# Pivot sectors to have separate columns for p0 and p1 values
gdp_pivot_df = gdp_filtered_df.pivot_table(
    index='YEAR',
    columns='sector',
    values='value',
    aggfunc='sum'
).reset_index()
gdp_pivot_df.columns.name = None # Remove columns name 'sector'

# Rename columns for clarity
gdp_pivot_df = gdp_pivot_df.rename(columns={'p0': 'Total_GDP', 'p1': 'Agricultural_GDP'})

output_filename_5 = 'processed_gdp_agriculture_national.csv'
gdp_pivot_df.to_csv(output_filename_5, index=False)
print(f"  - Data for Agriculture's Economic Pulse saved to '{output_filename_5}'")

print("\n--- Preprocessing Complete ---")
print("You now have several CSV files ready for visualization:")
print(f" - '{output_filename_1_1}' (Flood/Rainfall summary by state/year)")
print(f" - '{output_filename_1_2}' (Monthly rainfall patterns for flood/non-flood years by state)")
print(f" - '{output_filename_2}' (Annual crop production by state/crop type)")
print(f" - '{output_filename_3}' (Annual national timber production)")
print(f" - '{output_filename_4_1}' (Annual national fish landings)")
print(f" - '{output_filename_4_2}' (Monthly national fish landings patterns)")
print(f" - '{output_filename_5}' (Annual national GDP, including agricultural sector)")
print("\nRemember to refer to the 'Important Notes' in the code output regarding data limitations.")