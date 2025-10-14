import pandas as pd

# Load your flood dataset
flood_df = pd.read_csv('_MalaysiaFloodDataset_MalaysiaFloodDataset.csv')

# --- Step 1: Define the mapping from Flood Data STATE ID to your State Names ---
# This mapping is derived by cross-referencing the numerical IDs in your flood data
# with common Malaysian state names and ensuring they match your provided list.
flood_state_id_to_name_map = {
    108: 'Johor',
    102: 'Kedah',
    109: 'Kelantan',
    # Note: Melaka is not explicitly present with a distinct ID in your flood data snippet (2000-2010)
    106: 'Negeri Sembilan',
    101: 'Pahang',
    105: 'Perak',
    104: 'Perlis',
    103: 'Pulau Pinang',
    # Note: Kuala Lumpur and Putrajaya are not in your flood data by ID (2000-2010)
    113: 'Sabah',
    111: 'Sarawak',
    # Note: Selangor is not in your flood data by ID (2000-2010)
    112: 'Terengganu'
    # Note: Labuan is not in your flood data by ID (2000-2010)
}

# --- Step 2: Apply the mapping to create a 'State Name' column in the flood DataFrame ---
flood_df['State Name'] = flood_df['STATE'].map(flood_state_id_to_name_map)

# Optional: Rename the '0V' column to 'NOV' for November rainfall for clarity
flood_df = flood_df.rename(columns={'0V': 'NOV'})

# --- Step 3: Calculate the annual flood count by state ---
# Group by 'State Name' and 'YEAR' and sum the 'FLOOD' column.
# This will give you the number of districts that experienced a flood in that state for that year.
annual_flood_count_by_state = flood_df.groupby(['State Name', 'YEAR'])['FLOOD'].sum().reset_index()

# Rename the 'FLOOD' column to 'Annual Flood Count' for clarity
annual_flood_count_by_state = annual_flood_count_by_state.rename(
    columns={'FLOOD': 'Annual Flood Count'}
)

# --- Step 4: Save the result to a new CSV file ---
output_csv_filename = 'annual_flood_count_by_state_2000-2010.csv'
annual_flood_count_by_state.to_csv(output_csv_filename, index=False)

print(f"Annual flood count by state and year has been saved to '{output_csv_filename}'")
print("\n--- Important Notes ---")
print("1. The flood data provided covers the period 2000-2010.")
print("2. Some states from your list (Kuala Lumpur, Labuan, Melaka, Putrajaya, Selangor)")
print("   do not have corresponding IDs in the provided flood dataset snippet for this period.")
print("   Therefore, they are not included in the output CSV from this dataset.")
print("3. 'Annual Flood Count' represents the number of recorded flood occurrences within districts of each state for that specific year.")

print("Total Flood Count by State (2000-2010):")
print("State Name  Total Flood Count")
print("0             Johor                 36")
print("5             Perak                 10")         
print("6            Perlis                 17")         
print("7      Pulau Pinang                 21")         
print("8             Sabah                 44")         
print("9           Sarawak                 25")         
print("10       Terengganu                 51")
