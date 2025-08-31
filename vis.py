import pandas as pd
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


# Load the CSV data into a DataFrame
df = pd.read_csv('opt.csv')  # Replace 'your_file.csv' with the path to your CSV file

# Create a plot with a world map projection
fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_global()  # Set the map to show the entire world

# Add coastlines to the map for reference
ax.coastlines()

# Plot the start and end points
ax.scatter(df['lon'], df['lat'], color='green', marker='o', s=100, label='Start', transform=ccrs.PlateCarree())
ax.scatter(df['opt_lon'], df['opt_lat'], color='red', marker='x', s=100, label='End', transform=ccrs.PlateCarree())

# Plot lines between start and end points
for _, row in df.iterrows():
    ax.plot([row['lon'], row['opt_lon']], [row['lat'], row['opt_lat']], color='blue', linewidth=2, transform=ccrs.PlateCarree())

# Add title and labels
ax.set_title("Start and End Points with Connecting Lines")
plt.legend()

# Show the plot
plt.show()