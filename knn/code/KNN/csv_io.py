import csv


def read_csv(path):
    return csv.reader(open(path))

