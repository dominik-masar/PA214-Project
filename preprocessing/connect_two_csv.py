import pandas as pd

# Load both CSV files
file1 = 'datasets/space_with_geo_with_countries.csv'
file2 = 'datasets/space_missions_with_goals.csv'
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Choose the column from df1 to add (change 'column_name' to your actual column)
column_to_add = df2['Mission Goal']

# Add the column to df2
df1['Mission Goal'] = column_to_add

# Save the result to a new CSV file
df1.to_csv('final_dataset_missions.csv', index=False)

print("New CSV file 'final_dataset_missions.csv' created successfully.")