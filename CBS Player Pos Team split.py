# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:47:11 2024

@author: homer
"""

import os
import pandas as pd

#'5-Tool Predators', 'Brain Donors', 'Directional Pull', 'E Machine Tigers', 'Why Me', 'High Stinky Cheddar', 'Maroon Platoon', 'Pop Fouls', 'The Balking Dead', 'TopGunners'
            

# Path to the folder containing CSV files
folder_path = r"C:\Users\homer\OneDrive\Documents\Fantasy Baseball\20240515"

# Initialize an empty DataFrame to store the results
# result_df = pd.DataFrame()

counter = 1

for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        shortfilename = os.path.splitext(filename)[0]

        # Read the TXT file with comma-separated values, skipping the first and last two rows
        df = pd.read_csv(file_path, header=0, skiprows=[0], delimiter=",")
        # df = df[:-1]    

        # Drop the 'Unnamed: 18' column, if present
        df = df.drop(columns=['Unnamed: 18'], errors='ignore')
        print(df.columns)

        if not df.empty:
            # df['Team'] = df['Player'].str.split(" \ | ").str[-1]
            df['Team'] = df['Player'].str.split(" &#149; ").str[-1]
            # df['Player'] = df['Player'].str.split(" \| ").str[0]
            df['Player'] = df['Player'].str.split(" &#149; ").str[0]
            df['Position'] = df['Player'].str.rsplit(' ', 1).str[-1]
            df['Player'] = df['Player'].str.rsplit(' ', 1).str[0]
            
            #replace different names
            replacement_dict = {'Vladimir Guerrero': 'Vladimir Guerrero Jr.', 
                                'Nate Lowe': 'Nathaniel Lowe',
                                'Luis Robert': 'Luis Robert Jr.', 
                                'Pete Fairbanks': 'Peter Fairbanks', 
                                'Nestor Cortes': 'Nestor Cortes Jr.', 
                                'Cedric Mullins': 'Cedric Mullins II',
                                'Bobby Witt': 'Bobby Witt Jr.', 
                                'Joshua Lowe': 'Josh Lowe', 
                                'Zachary Neto': 'Zach Neto',
                                'Logan Taylor Allen': 'Logan Allen',
                                'Will Smith': 'Will Smith,P'}
            df['Player'] = df['Player'].replace(replacement_dict)
            
            df = df[df['Player'] != '']
            df = df[df['Player'] != 'Player']
            df = df[df['Player'] != 'TOTALS']
            df = df[df['Avail'] != 'Pitchers']
            df = df[df['Avail'] != 'Batters']
    
            
            # Fill NaN values with an empty string
            df = df.fillna('')
            
            # Filter out rows where the value in the "Rank" column is 9999
            df = df[df['Rank'] != 9999]

            # Save the result DataFrame to a new CSV file in the same folder as the input files
            output_file_path = os.path.join(folder_path, str(shortfilename) + "-fixed.txt")
            df.to_csv(output_file_path, index=False)

            # Debug print to check the result_df
            print(df)

            counter += 1