"""
Merge specimen metadata with Procrustes-aligned coordinates

This script concatenates specimen-level metadata with Procrustes-aligned
landmark coordinates generated in a prior GPA step.

Input:
- Original CSV containing specimen metadata and raw landmark coordinates
  (e.g., GM_M2_Metaconid_3_Cleaned.csv)
- CSV containing Procrustes-aligned landmark coordinates
  (e.g., adjusted_landmarks.csv)

Output:
- CSV containing metadata concatenated with Procrustes-aligned coordinates
  (e.g., SuperImposed_GM_M2_4.csv)

Notes:
- No transformation or modification of coordinates is performed here
- Row order is assumed to match between metadata and GPA outputs
"""

import pandas as pd
 
# Load the original data including metadata
data = pd.read_csv('GM_M2_Metaconid_3_Cleaned.csv')
 
# Load the adjusted landmarks from R
adjusted_data = pd.read_csv('adjusted_landmarks.csv')
 
# Select the metadata columns (everything except the coordinates)
metadata_columns = data.columns[:-adjusted_data.shape[1]]  # Adjust if number of columns differs
metadata_df = data[metadata_columns]
 
# Concatenate metadata with the adjusted coordinates
output_df = pd.concat([metadata_df.reset_index(drop=True), adjusted_data], axis=1)
 
# Save the final data to a new CSV file
output_df.to_csv('SuperImposed_GM_M2_4.csv', index=False)
 
print("Procrustes superimposed data saved to 'SuperImposed_GM_M2_4.csv'")
 
 
