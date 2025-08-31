from energy import *
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap
from lakes import *
from scipy.optimize import minimize
from scipy.optimize import differential_evolution
from popscore import *
from tempscore import *

printmap = False

def cost(coords):
    lat, lon = coords[0], coords[1]

    energy = station_score(lat, lon, df_power) + score_substations(lat, lon, df_sub)
    water = water_cost(lat,lon)
    population = pop_cost(lat, lon)
    temps = temp_cost(lat, lon)

    return energy + water + population + temps


# Optimisation

# Initial guess for lat, lon (e.g., Alice Springs)
initial_guess = [-27.4698, 153.0251]  # Example: Brisbane coordinates
bounds = [(-44.0, -10.0), (112.0, 154.0)]

# Optimize the cost function
result = differential_evolution(cost, bounds, strategy='best1bin', maxiter=1000, popsize=20, mutation=0.8, recombination=0.7)

# Output the optimized coordinates and cost
print("Optimal solution:", result.x)
print("Objective function value at optimal solution:", result.fun)

print(f"Optimized latitude: {optimized_lat}, Optimized longitude: {optimized_lon}")
print(f"Optimized cost: {optimized_cost}")

'''
# Example: Evaluate a candidate site in Wagga Wagga
candidate_lat = -35.1175
candidate_lon = 147.3707

score = cost(candidate_lat, candidate_lon)
print(f"Power Score for Wagga Wagga: {score:.2f}")


lat = 23.6980
lon = 133.8807
score = cost(lat, lon)
print(f"Power Score for Alice Springs: {score:.2f}")

x = -36.4962190689999
y = 146.131165493

print(geodesic((lat, lon), (x,y)).km)
print(geodesic((candidate_lat, candidate_lon), (x,y)).km)
'''

if printmap == True:
    # Define the bounds for Australia (latitude, longitude)
    lat_min, lat_max = -43.74, -10.68
    lon_min, lon_max = 113.27, 153.57

    # Create a grid of coordinates (e.g., 1-degree grid)
    latitudes = np.arange(lat_min, lat_max, 1)
    longitudes = np.arange(lon_min, lon_max, 1)

    # Create a DataFrame of all the coordinates
    grid = pd.DataFrame([(lat, lon) for lat in latitudes for lon in longitudes], columns=["Latitude", "Longitude"])

    grid["Cost"] = grid.apply(lambda row: cost(row["Latitude"], row["Longitude"]), axis=1)

    grid.to_csv('grid.csv', index=False)  # index=False to not include the index column

    # Plotting the heatmap
    plt.figure(figsize=(10, 8))
    plt.scatter(grid["Longitude"], grid["Latitude"], c=grid["Cost"], cmap="viridis", s=10)
    plt.colorbar(label="Cost")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Heatmap of Cost Across Australia")
    plt.show()

    # Create a base map centered on Australia
    m = folium.Map(location=[-25.0, 133.0], zoom_start=4)

    # Create a list of [latitude, longitude, cost] for the heatmap
    heat_data = [[row["Latitude"], row["Longitude"], row["Cost"]] for _, row in grid.iterrows()]

    # Add the heatmap layer
    HeatMap(heat_data).add_to(m)

    # Save the map to an HTML file
    m.save("australia_cost_heatmap.html")