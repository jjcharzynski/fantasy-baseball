# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 00:52:13 2024

@author: homer
"""

import pandas as pd
import io
import csv
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import os

# Load the data from the CSV file
file_path = r'C:\Users\homer\Downloads\Cheat-Sheet-Generator-0226unmodified - Pitchers.csv'
folder_path = r'C:\Users\homer\Downloads'

# Read the content of the file
with open(file_path, 'r', encoding='utf-8') as infile:
    csv_content = infile.readlines()

# Replace the first comma with '*' in lines starting with '"'
csv_content = [line.replace(',', '*', 1) if line.startswith('"') else line for line in csv_content]

# Load the preprocessed data from the CSV content
players_data = pd.read_csv(io.StringIO(''.join(csv_content)), quoting=csv.QUOTE_NONNUMERIC)

# Replace '*' with ',' in the 'PLAYER' column
players_data['PLAYER'] = players_data['PLAYER'].str.replace('*', ',')

# Filter out players
players_data = players_data[players_data['LG'] != 'NL']
players_data = players_data[players_data['POS'] != 'RP']
print("Number of Players: ", len(players_data)-1)

# # Sort the DataFrame by 'W' in descending order within each 'Team'
players_data = players_data.sort_values(by='IP', ascending=False)

# Create a mapping dictionary for numerical roles to words
role_mapping = {1: 'Ace', 2: 'Number Two', 3: 'Number Three', 4: '4th Starter', 5: '5th Starter', 6: 'Spot Starter'}

# Create a new column 'Role' and set it to 'Starter' initially
players_data['Role'] = 'Starter'

N = 6  # Start with the second highest
while N >= 1:  # Adjust the condition based on your requirement
    # Identify the player with the Nth highest 'IP' in each 'Team' and set their role to N
    players_data.loc[players_data.groupby('TM')['IP'].head(N).index, 'Role'] = N
    N -= 1
    
# Map numerical roles to words
players_data['Role'] = players_data['Role'].map(role_mapping)    

# Assign Free Agent Role
players_data.loc[players_data['LG'].isna(), 'Role'] = 'Free Agent'

scoring_categories = ['K', 'ERA', 'WHIP', 'QS', 'W']

# Check if 'QS' column exists and its max value is 0
if 'QS' in players_data.columns and players_data['QS'].max() == 0:
    # Calculate the value using the specified equation
    players_data['QS'] = players_data.apply(
    lambda row: (((row['IP'] / row['GS']) / 6.15) - (0.11 * row['ERA'])) * row['GS'] if row['GS'] > 0 and row['POS'] == 'SP' else 0, axis=1)
    # players_data['QS'] = players_data.apply(lambda row: ((((row['IP'] / row['GS']) / 6.15) - (0.11 * row['ERA'])) * row['GS']) if row['POS'] == 'SP' else 0, axis=1)
    # players_data['QS'] = players_data.apply(lambda row: (((row['IP'] / row['GS']) / 6.15) - (0.11 * row['ERA'])) * row['GS'] if row['POS'] == 'SP' else 0, axis=1)
else:
    print("Either 'QS' column does not exist in players_data or its max value is not 0.")

#Reverse ERA and WHIP
players_data['ERA'] = players_data['ERA'] * -1
players_data['WHIP'] = players_data['WHIP'] * -1

# Calculate percentrank.inc for each scoring category
for category in scoring_categories:
    players_data[f'{category}_percentrank'] = players_data[category].rank(pct=True, method='max')

# Extract the percentrank data
percentrank_data = players_data[[f'{category}_percentrank' for category in scoring_categories]]

# Choose the number of clusters (you can experiment with different values)
num_clusters = 5

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

#Reverse ERA and WHIP
players_data['ERA'] = players_data['ERA'] * -1
players_data['WHIP'] = players_data['WHIP'] * -1

# Save the result DataFrame to a new CSV file in the same folder as the input files
output_file_path = os.path.join(folder_path, "output.csv")
players_data.to_csv(output_file_path, index=False, sep='\t')

# Display the clustered players
print(players_data[['PLAYER', 'POS', 'TM', 'Role', 'SV', 'K', 'ERA', 'WHIP', 'W', 'QS', 'Cluster']])
print("Number of Players: ", len(players_data)-1)