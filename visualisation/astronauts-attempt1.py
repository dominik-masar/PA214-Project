import csv
from collections import Counter

# Replace with your actual file path
filename = 'datasets/astronauts.csv'

# Counter to store occurrences
ussr_astronauts = Counter()

with open(filename, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["Profile.Nationality"] == "U.S.S.R/Russia":
            name = row["Profile.Name"]
            ussr_astronauts[name] += 1

# Print the results
for name, count in ussr_astronauts.items():
    print(f"{name}: {count} mission(s)")
