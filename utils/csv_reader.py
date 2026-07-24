import csv

def read_csv(file_path):
    """Read CSV and return a list of tuples for parameterization"""
    data = []
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert salary and age to int
            data.append((row['name'], int(row['salary']), int(row['age'])))
    return data