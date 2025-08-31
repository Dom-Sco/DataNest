import pandas as pd
from geopy.distance import geodesic
import numpy as np

csv_file = 'combined_output.csv'
water_bodies = pd.read_csv(csv_file)

def water_cost(lat, lon, water_bodies = water_bodies, radius_km=300, penalty=1000):
    # Calculate the sum of costs for all water bodies within a 300km radius
    total_cost = 0
    within_radius = False
    
    for _, water in water_bodies.iterrows():
        # Calculate the distance to the water body
        water_coords = (water['latitude'], water['longitude'])
        center_coords = (lat, lon)
        distance = geodesic(center_coords, water_coords).km
        
        # If within the 300km radius, calculate the cost and sum it
        if distance <= radius_km:
            within_radius = True
            water_area = water['Shape__Area']
            cost = water_area / distance
            total_cost += cost
    
    # If no water bodies are within the radius, apply penalty
    if not within_radius:
        return penalty
    
    return np.log(total_cost)


'''
# Example: Evaluate a candidate site in Wagga Wagga
candidate_lat = -35.1175
candidate_lon = 147.3707

score = water_cost(candidate_lat, candidate_lon)
print(f"Water Score for Wagga Wagga: {score:.2f}")

lat = 23.6980
lon = 133.8807
score = water_cost(lat, lon)
print(f"Water Score for Alice Springs: {score:.2f}")
'''