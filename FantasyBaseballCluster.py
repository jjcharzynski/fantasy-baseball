# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 00:06:35 2024

@author: homer
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go

# Load the data from the CSV file
file_path = r'C:\Users\homer\Downloads\Cheat-Sheet-Generator-0226unmodified - Hitters.csv'
players_data = pd.read_csv(file_path)

# Filter out NL players
players_data = players_data[players_data['LG'] != 'NL']

# Assume columns 'AB', 'HR', 'RBI', 'SB', 'H', '2B', '3B', 'BB', '1B' are the scoring categories
scoring_categories = ['AB', 'HR', 'RBI', 'SB', 'H', '2B', '3B', 'BB', '1B']

# Set the minimum and maximum values for each category
min_values = players_data[scoring_categories].min()
max_values = players_data[scoring_categories].max()

# Extract the scoring data
scoring_data = players_data[scoring_categories]

# Set the minimum and maximum values for each axis
fig_range = [min_values, max_values]

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(scoring_data)

# Choose the number of clusters (you can experiment with different values)
num_clusters = 5

# Apply k-means clustering
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
players_data['Cluster'] = kmeans.fit_predict(scaled_data)

# Create radar charts for each cluster
fig = go.Figure()

for cluster in range(num_clusters):
    cluster_data = players_data[players_data['Cluster'] == cluster]
    average_values = cluster_data[scoring_categories].mean()
    
    fig.add_trace(go.Scatterpolar(
        r=average_values.values,
        theta=scoring_categories,
        fill='toself',
        name=f'Cluster {cluster}'
    ))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=fig_range  # Set the range to [min_values, max_values]
        )),
    showlegend=True,
    title="Radar Charts for Player Clusters",
)

fig.show()


# plt.show()
ArithmeticError(
    )fig.write_html('radar_charts.html')



# Visualize the clusters
# sns.scatterplot(x='BattingAvg', y='HomeRuns', hue='Cluster', data=players_data, palette='viridis')
# plt.title('Clustering Players based on Batting Avg and Home Runs')
# plt.xlabel('Batting Avg')
# plt.ylabel('Home Runs')
# plt.show()


# Display the clustered players
print(players_data[['PLAYER', 'POS', 'AB', 'HR', 'RBI', 'SB', 'H', '2B', '3B', 'BB', '1B', 'Cluster']])
