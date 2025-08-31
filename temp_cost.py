import pandas as pd
from geopy.distance import geodesic
import numpy as np
import math

# Hyperparameters
w = 200

csv_file = 'temp.csv'
temperature = pd.read_csv(csv_file)

def temp_cost(lat, lon, temp_df = temperature):
    # Calculate the sum of costs for all water bodies within a 300km radius
    total_cost = 0
    distances = []
    costs = []
    
    for _, temp in temperature.iterrows():
        # Calculate the distance to the water body
        temp_coords = (temp['latitude'], temp['longitude'])
        if not any(math.isnan(x) for x in temp_coords if isinstance(x, float)):   
            center_coords = (lat, lon)
            distances.append(geodesic(center_coords, temp_coords).km)
            
            costs.append(w * (temp['mean max temperature last 10 years (degC)'] + center_coords[1]) / (1+ distances[-1]))
    
    index = distances.index(min(distances))
    
    return costs[index]


# Example: Evaluate a candidate site in Wagga Wagga
candidate_lat = -35.1175
candidate_lon = 147.3707

score = temp_cost(candidate_lat, candidate_lon)
print("Pop Score for Wagga Wagga:", score)

lat = 23.6980
lon = 133.8807
score = temp_cost(lat, lon)
print("Pop Score for Alice Springs:",score)