# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 20:08:26 2024

@author: homer
"""

#This script reads positional rankings exports and compiles them

import os
import pandas as pd

# Path to the folder containing TXT files
folder_path = r"C:\Users\homer\OneDrive\Documents\Fantasy Baseball\20240330"

# Initialize an empty DataFrame to store the results
result_df = pd.DataFrame()

target_rows = 1

# Order of positions
position_order = ['C', '1B', '2B', '3B', 'SS', 'OF', 'DH', 'SP', 'RP']

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)

        # Read the TXT file with comma-separated values, skipping the first and last two rows
        df = pd.read_csv(file_path, header=0, skiprows=[0], delimiter=",")
        df = df[:-2]        

        # Drop the 'Unnamed: 9' column, if present
        df = df.drop(columns=['Unnamed: 9'], errors='ignore')

        # Filter out rows where the value in the "Rank" column is 9999
        df = df[df['Rank'] != 9999]
        
        # Add NULL rows to df
        current_rows = len(df)
        target_rows = max(target_rows, current_rows)
        null_rows_needed = max(0, target_rows - current_rows)
        null_df = pd.DataFrame(index=range(null_rows_needed), columns=df.columns)
        df = pd.concat([df, null_df], ignore_index=True)
        
        # Add NULL rows to result_df
        current_rows = len(result_df)
        target_rows = max(target_rows, current_rows)
        null_rows_needed = max(0, target_rows - current_rows)
        null_df = pd.DataFrame(index=range(null_rows_needed), columns=result_df.columns)
        result_df = pd.concat([result_df, null_df], ignore_index=True)

        # If there are remaining rows, proceed to the next steps
        if not df.empty:
            # Split the 'Player' column into 'Player', 'Position', and 'Team'
            df[['Player', 'Position', 'Team']] = df['Player'].str.extract(r'(.+?) (\w{1,2}) \| (\w+)')

            # Modify column_name to exclude the file extension
            column_name = os.path.splitext(filename)[0]

            # Merge result_df with the current column
            result_df[column_name] = df['Player']

            # Print the number of rows for each file
            print(f"File: {filename}, Rows: {len(df)}")
            # print(df)
            # print(result_df)

# Fill NaN values with an empty string
result_df = result_df.fillna('')

# Reorder columns after the loop
result_df = result_df[position_order]

# Add a new column 'All' to result_df with empty strings
result_df['All'] = ''

# Initialize an empty list to store unique values
all_values = []

# Iterate over each position in position_order
for position in position_order:
    # Extract unique values from the position column and append to the list
    unique_values = result_df[position].dropna().unique().tolist()
    all_values.extend(unique_values)

# Remove duplicates from the list
unique_all_values = list(set(all_values))

# Set the number of rows in result_df to match the length of unique_all_values
target_rows = max(target_rows, len(unique_all_values))
null_rows_needed = max(0, target_rows - current_rows)
null_df = pd.DataFrame(index=range(null_rows_needed), columns=result_df.columns)
result_df = pd.concat([result_df, null_df], ignore_index=True)

# Assign the unique values list to the 'All' column
result_df['All'] = unique_all_values

# Debug print to check the result_df
print(result_df)

# Save the result DataFrame to a new CSV file in the same folder as the input files
output_file_path = os.path.join(folder_path, "output.csv")
result_df.to_csv(output_file_path, index=False)

# Debug print to check the result_df
print(result_df)