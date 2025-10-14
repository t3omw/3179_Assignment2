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

# --- Step 3: Calculate the total flood count by state ---
# Group by the new 'State Name' column and sum the 'FLOOD' column.
# Since 'FLOOD' is 1 for a flood and 0 for no flood, summing it gives the total count.
total_flood_count_by_state = flood_df.groupby('State Name')['FLOOD'].sum().reset_index()

# Rename the 'FLOOD' column to 'Total Flood Count' for clarity
total_flood_count_by_state = total_flood_count_by_state.rename(
    columns={'FLOOD': 'Total Flood Count'}
)

# Display the total flood count by state
print("Total Flood Count by State (2000-2010):\n")
print(total_flood_count_by_state)

print("\n--- Important Notes ---")
print("1. The flood data provided (_MalaysiaFloodDataset_MalaysiaFloodDataset.csv) covers the period 2000-2010.")
print("2. Some states from your list (Kuala Lumpur, Labuan, Melaka, Putrajaya, Selangor)")
print("   do not have corresponding IDs in the provided flood dataset snippet.")
print("   Therefore, they are not included in the 'Total Flood Count by State' output from this dataset.")
print("3. The 'Total Flood Count' represents the number of recorded flood events for each state's districts")
print("   during the 2000-2010 period, where a '1' in the 'FLOOD' column indicates a flood occurrence.")