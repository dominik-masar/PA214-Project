import csv
from collections import Counter

# Replace with your actual file path
filename = 'datasets/space_with_geo-firstAttempt.csv'

# Counter to store occurrences per company
company_counts = Counter()

with open(filename, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        company = row["Company Name"]
        company_counts[company] += 1

# Print the results
for company, count in company_counts.items():
    print(f"{company}: {count} launch(es)")
