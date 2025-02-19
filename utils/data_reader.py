import csv

def read_product_filters(csv_file):
    filters = []
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            filters.append(row)  # Append each row as a dictionary
    return filters