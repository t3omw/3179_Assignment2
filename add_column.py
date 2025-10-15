import pandas as pd

# Define the file paths
flood_summary_file = 'processed_flood_summary_by_state_year.csv'
state_area_file = 'malaysia_state_area.csv'

# Load the flood summary data
df_flood_summary = pd.read_csv(flood_summary_file) # [8, 9, 12, 15, 16]

# Load the state area data
df_state_area = pd.read_csv(state_area_file) # [8, 9, 12, 15, 16]

# Merge the two dataframes to bring in the Area_sqkm
# Merging on 'State Name' from df_flood_summary and 'State' from df_state_area
df_merged = pd.merge(df_flood_summary, df_state_area, left_on='State Name', right_on='State', how='left') # [2, 3, 4, 5, 7]

# Calculate the 'Annual_Density_mm_per_km2' column
# Average_Annual_Rainfall is in mm, Area_sqkm is in km^2
df_merged['Annual_Density_mm_per_km2'] = df_merged['Average_Annual_Rainfall'] / df_merged['Area_sqkm'] # [13, 17, 18, 19, 20]

# Drop the 'State' and 'Area_sqkm' columns that were only needed for the calculation
# The original request implies only adding the new calculated column to the first CSV.
df_updated = df_merged.drop(columns=['State', 'Area_sqkm'])

# Save the updated DataFrame back to the original CSV file
df_updated.to_csv(flood_summary_file, index=False) # [1, 6, 10, 11, 14]

print(f"'{flood_summary_file}' has been updated with the 'Annual_Density_mm_per_km2' column.")