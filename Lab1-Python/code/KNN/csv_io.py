import csv


def read_csv(path):
    csv_file = csv.reader(open(path))
    next(csv_file)
    return csv_file
