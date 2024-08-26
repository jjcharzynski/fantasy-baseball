# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 00:52:13 2024

@author: homer
"""


import pandas as pd
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import os

# Load the data from the CSV file
file_path = r'C:\Users\homer\Downloads\Cheat-Sheet-Generator-0226unmodified - Hitters.csv'
folder_path = r'C:\Users\homer\Downloads'
players_data = pd.read_csv(file_path)

# Filter out NL players
players_data = players_data[players_data['LG'] != 'NL']

# Assume columns 'AB', 'HR', 'RBI', 'SB', 'H', '2B', '3B', 'BB', '1B' are the scoring categories
# scoring_categories = ['AB', 'H', '1B', '2B', '3B', 'HR', 'BB','RBI', 'SB']
scoring_categories = ['SLG', 'HR', 'RBI', 'AVG', 'OBP', 'SB']

# Calculate percentrank.inc for each scoring category
for category in scoring_categories:
    players_data[f'{category}_percentrank'] = players_data[category].rank(pct=True, method='max')

# Extract the percentrank data
percentrank_data = players_data[[f'{category}_percentrank' for category in scoring_categories]]

# Choose the number of clusters (you can experiment with different values)
num_clusters = 9

# Apply k-means clustering
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
players_data['Cluster'] = kmeans.fit_predict(percentrank_data)

# Create radar charts for each cluster
fig = go.Figure()

for cluster in range(num_clusters):
    cluster_data = players_data[players_data['Cluster'] == cluster]
    average_values = cluster_data[[f'{category}_percentrank' for category in scoring_categories]].mean()
    
    fig.add_trace(go.Scatterpolar(
        r=average_values.values,
        theta=scoring_categories,
        # fill='toself',
        name=f'Cluster {cluster}',
        connectgaps=True
    ))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]  # Adjust the range as needed
        )),
    showlegend=True,
    title="Radar Charts for Player Clusters",
)

fig.show()
fig.write_html('radar_charts.html')

# Save the result DataFrame to a new CSV file in the same folder as the input files
output_file_path = os.path.join(folder_path, "output.csv")
players_data.to_csv(output_file_path, index=False)

# Display the clustered players
print(players_data[['PLAYER', 'POS', 'AB', 'HR', 'RBI', 'SB', 'H', '2B', '3B', 'BB', '1B', 'Cluster']])