"""
Prepare landmark coordinates for GPA

This script loads digitized landmark coordinates from a CSV file and reshapes
them into a format suitable for Generalized Procrustes Analysis (GPA).

Input:
- CSV file containing landmark coordinates (e.g., X1, Y1, ..., Xn, Yn)

Output:
- CSV file with coordinates formatted for downstream GPA workflows

Notes:
- No alignment, scaling, or rotation is performed here
- This step only reshapes and exports coordinates
"""
import numpy as np
import pandas as pd
 
# Load the data from a CSV file
data = pd.read_csv('GM_M2_Metaconid_3_Cleaned.csv')
 
# Select only the coordinate columns (X1 to Y23)
coordinate_columns = [
    'X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'X5', 'Y5', 'X6', 'Y6',
    'X7', 'Y7', 'X8', 'Y8', 'X9', 'Y9', 'X10', 'Y10', 'X11', 'Y11', 'X12', 'Y12',
    'X13', 'Y13', 'X14', 'Y14', 'X15', 'Y15', 'X16', 'Y16', 'X17', 'Y17', 'X18', 'Y18',
    'X19', 'Y19', 'X20', 'Y20', 'X21', 'Y21', 'X22', 'Y22', 'X23', 'Y23'
]
coordinates = data[coordinate_columns].to_numpy()
 
# Reshape the coordinates array to prepare for export
num_specimens = len(coordinates)
num_landmarks = 23
reshaped_coordinates = coordinates.reshape((num_specimens, num_landmarks, 2))
 
# Convert reshaped coordinates to a 2D array for export
flat_coordinates = reshaped_coordinates.reshape((num_specimens, num_landmarks * 2))
 
# Export the data to a CSV file for R to read
export_df = pd.DataFrame(flat_coordinates, columns=coordinate_columns)
export_df.to_csv('landmarks_for_R.csv', index=False)
 
print("Landmark data prepared and exported to 'landmarks_for_R.csv'")
