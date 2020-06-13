import csvreader
import time


s1 = '23:00:00'
s2 = '06:00:00'


def timestamp_datetime(value):
    t_format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(value))
    dt = time.strftime(t_format, value)
    return dt


def datetime_timestamp(dt):
    time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return int(s)


def filter_night(filename):
    dat = csvreader.csv_reader_no_headers(filename)
    out_dat = []
    for line in dat:
        s = timestamp_datetime(int(line[1]))
        s = s[11:]
        if s >= s1 or s <= s2:
            out_dat.append(line)
    return out_dat


def filter_day(filename):
    dat = csvreader.csv_reader_no_headers(filename)
    out_dat = []
    for line in dat:
        s = timestamp_datetime(int(line[1]))
        s = s[11:]
        if s2 <= s <= s1:
            out_dat.append(line)
    return out_dat


def filter_time(filename, date, sl, sr):
    dat = csvreader.csv_reader_no_headers(filename)
    out_dat = []
    for line in dat:
        s = timestamp_datetime(int(line[1]))
        dat = s[:10]
        tm = s[11:]
        if sl <= tm <= sr and dat == date:
            out_dat.append(line)
    return out_dat


if __name__ == '__main__':
    pass
