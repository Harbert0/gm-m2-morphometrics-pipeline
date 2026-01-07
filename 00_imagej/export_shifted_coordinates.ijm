
// ------------------------------------------------------------
// Export shifted XY landmark coordinates from ImageJ ROI Manager
//
// This macro extracts point ROI coordinates from the ROI Manager,
// shifts all landmarks so that the first point is at the origin,
// and exports the shifted coordinates to a CSV file.
//
// Input:
// - Point ROIs loaded in the ImageJ ROI Manager
//
// Output:
// - shifted_coordinates.csv (columns: X, Y)
//
// Notes:
// - Landmarks must be ordered consistently in the ROI Manager
// - The first landmark is treated as a translational reference point
// ------------------------------------------------------------
// Ensure there are ROIs in the ROI Manager
if (roiManager("count") == 0) {
    exit("No ROIs found in ROI Manager");
}
 
// Get the number of ROIs (points) in the ROI Manager
n = roiManager("count");
 
// Initialize arrays to store the coordinates
xpoints = newArray(n);
ypoints = newArray(n);
 
// Loop through each ROI and get the coordinates
for (i = 0; i < n; i++) {
    roiManager("select", i);
    getSelectionCoordinates(x, y);
    xpoints[i] = x[0];
    ypoints[i] = y[0];
}
 
// Store the coordinates of the first point
x0 = xpoints[0];
y0 = ypoints[0];
 
// Shift all points so the first point is at the origin
for (i = 0; i < n; i++) {
    xpoints[i] = xpoints[i] - x0;
    ypoints[i] = ypoints[i] - y0;
}
 
// Print the shifted coordinates to the log window
print("Shifted Coordinates:");
for (i = 0; i < n; i++) {
    print("Point " + (i + 1) + ": (" + xpoints[i] + ", " + ypoints[i] + ")");
}
 
// Save the shifted coordinates to a file
savePath = getDirectory("Choose a Directory") + "shifted_coordinates.csv";
file = File.open(savePath);
File.write("X,Y\n");
for (i = 0; i < n; i++) {
    File.write(xpoints[i] + "," + ypoints[i] + "\n");
}
File.close();
print("Coordinates saved to: " + savePath);
