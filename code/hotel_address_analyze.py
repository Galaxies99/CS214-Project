import csvreader
import csv
from urllib.request import urlopen
from urllib.parse import quote
import json
import hashlib

if __name__ == '__main__':
    dat = csvreader.csv_reader_no_headers('../data/hotel_address_final.csv')
    count = 0

    output = 'json'
    ak = '???????????????' # Please fill in your AK code

    addr_list = []
    cnt = 0
    for line in dat:
        cnt += 1
        addr = line[0]
        pos = addr.find('] ')
        addr = addr[pos + 2:]
        pos = addr.find('（')
        if pos != -1:
            addr = addr[: pos + 1]
        pos = addr.find('号')
        addr = addr[: pos + 1]
        if addr == "":
            continue

        uri = 'http://api.map.baidu.com/geocoding/v3/?address=' + quote(addr) + '&output=json&ak=' + ak

        uh = urlopen(uri)
        data = uh.read().decode()
        js = json.loads(data)

        if not js or 'status' not in js or js['status'] != 0:
            print('Fail!')
            continue

        lat = js["result"]["location"]["lat"]
        lng = js["result"]["location"]["lng"]

        addr_list.append([lat, lng])
        print(cnt)

    with open('../data/hotel_address_lat_lng.csv', "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, dialect='excel')
        for item in addr_list:
            csv_writer.writerow(item)

