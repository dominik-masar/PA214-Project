import pandas as pd

# Load the CSV file
input_file = 'datasets/space_with_geo-firstAttempt.csv'
output_file = 'datasets/space_with_geo_with_mission_year.csv'

# Read the CSV into a DataFrame
df = pd.read_csv(input_file)

# Ensure the 'Datum' column is in datetime format
df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce')

# Extract the year from the 'Datum' column and create a new column 'Mission.Year'
df['Mission.Year'] = df['Datum'].dt.year
df['Mission.Year'] = df['Mission.Year'].fillna(-1).astype(int).astype(str)
df['Company ID'] = df['Company Name'].factorize()[0]


# Save the updated DataFrame to a new CSV file
df.to_csv(output_file, index=False)

print(f"File saved as {output_file}")