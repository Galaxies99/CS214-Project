import order_assigner
import datahelper
import odrp_gdp
import csv


if __name__ == '__main__':
    filename = '../../CS214-CourseData/Projects/data/chengdu_order/order_20161105'
    hr = 23
    mt = 0
    ans = []
    while hr != 6:
        hr_str = str(hr)
        if hr < 10:
            hr_str = '0' + hr_str
        mt_str = str(mt)
        mt_str2 = str(mt + 9)
        if mt == 0:
            mt_str = '00'
            mt_str2 = '09'
        str1 = hr_str + ':' + mt_str + ':00'
        str2 = hr_str + ':' + mt_str2 + ':59'
        print('running', str1, 'to', str2)
        order_assigner.assign(filename, str1, str2, 70, 20, 9.12, 0.56, 150, 1.8)
        _n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb = datahelper.load_json('../data/order_data.json')
        bus_num, profit = odrp_gdp.solver(_n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb)
        ans.append([profit, bus_num])
        mt += 10
        if mt == 60:
            hr += 1
            mt = 0
        if hr == 24:
            hr = 0

    with open('../data/profits.csv', 'w', newline='') as out:
        csv_write = csv.writer(out, dialect='excel')
        for item in ans:
            csv_write.writerow(item)
