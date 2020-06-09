import csv


def csv_reader_without_headers(filename):
    dat = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            dat.append(row)
    return dat


def csv_reader_with_headers(filename):
    dat = []
    headers = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)
        for row in csv_reader:
            dat.append(row)
    return headers, dat


def csv_reader_no_headers(filename):
    dat = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            dat.append(row)
    return dat


if __name__ == '__main__':
    pass