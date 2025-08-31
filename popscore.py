import pandas as pd
from geopy.distance import geodesic
import numpy as np
import math

# Hyperparameters
a = 200
b= 0.1

csv_file = 'population.csv'
population = pd.read_csv(csv_file)

def pop_cost(lat, lon, pop_df = population):
    # Calculate the sum of costs for all water bodies within a 300km radius
    total_cost = 0
    distances = []
    costs = []
    
    for _, pop in population.iterrows():
        # Calculate the distance to the water body
        pop_coords = (pop['latitude'], pop['longitude'])
        if not any(math.isnan(x) for x in pop_coords if isinstance(x, float)):   
            center_coords = (lat, lon)
            distances.append(geodesic(center_coords, pop_coords).km)
            norm_pop = pop['Estimated resident population: Persons (no.) (Data year: 2023)'] / pop['Area in square kilometres']
            costs.append(a * np.exp(-b * norm_pop))
    
    index = distances.index(min(distances))
    
    return costs[index]


# Example: Evaluate a candidate site in Wagga Wagga
candidate_lat = -35.1175
candidate_lon = 147.3707

score = pop_cost(candidate_lat, candidate_lon)
print("Pop Score for Wagga Wagga:", score)

lat = 23.6980
lon = 133.8807
score = pop_cost(lat, lon)
print("Pop Score for Alice Springs:",score)