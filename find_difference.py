import csv


with open('combined.csv') as f:
    reader = csv.reader(f)
    headers = next(reader)
    combined_rows = {tuple(row[:3]): row for row in reader}


with open('pyopenworm_dump.csv') as f:
    reader = csv.reader(f)
    next(reader)
    pyopenworm_rows = {tuple(row[:3]): row for row in reader}


novel_rows = sorted(
    [value for key, value in combined_rows.items() if key not in pyopenworm_rows],
    key=lambda row: (row[1], row[0], row[2])
)

with open('difference.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(novel_rows)