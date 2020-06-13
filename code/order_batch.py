import order_assigner
import datahelper
import odrp_igdp
import odrp_gdp
import odrp_sgdp
import csv


if __name__ == '__main__':
    filename = '../../CS214-CourseData/Projects/data/haikou_order/order_20171011_20171014.csv'
    hr = 23
    mt = 0
    ans = []
    for day in range(11, 15):
        date = '2017-10-' + str(day)
        for hr in range(6):
            hr_str = '0' + str(hr)
            str1 = hr_str + ':00:00'
            str2 = hr_str + ':29:59'
            print('running', date, str1, 'to', str2)
            order_assigner.assign(filename, date, str1, str2, 50, 40, 4.58, 0.28, 150, 1.8)
            _n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb = datahelper.load_json('../data/order_data.json')
            bus_num, profit = odrp_igdp.solver(_n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb)
            # bus_num, profit = odrp_gdp.solver(_n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb)
            # bus_num, profit = odrp_sgdp.solver(_n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb)
            ans.append([profit, bus_num])

            str1 = hr_str + ':30:00'
            str2 = hr_str + ':59:59'
            print('running', date, str1, 'to', str2)
            order_assigner.assign(filename, date, str1, str2, 50, 40, 4.58, 0.28, 150, 1.8)
            _n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb = datahelper.load_json('../data/order_data.json')
            bus_num, profit = odrp_igdp.solver(_n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb)
            # bus_num, profit = odrp_gdp.solver(_n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb)
            # bus_num, profit = odrp_sgdp.solver(_n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb)
            ans.append([profit, bus_num])

        hr_str = '23'
        str1 = hr_str + ':00:00'
        str2 = hr_str + ':29:59'
        print('running', date, str1, 'to', str2)
        order_assigner.assign(filename, date, str1, str2, 50, 40, 4.58, 0.28, 150, 1.8)
        _n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb = datahelper.load_json('../data/order_data.json')
        bus_num, profit = odrp_igdp.solver(_n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb)
        # bus_num, profit = odrp_gdp.solver(_n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb)
        # bus_num, profit = odrp_sgdp.solver(_n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb)
        ans.append([profit, bus_num])

        str1 = hr_str + ':30:00'
        str2 = hr_str + ':59:59'
        print('running', date, str1, 'to', str2)
        order_assigner.assign(filename, date, str1, str2, 50, 40, 4.58, 0.28, 150, 1.8)
        _n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb = datahelper.load_json('../data/order_data.json')
        bus_num, profit = odrp_igdp.solver(_n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb)
        # bus_num, profit = odrp_gdp.solver(_n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb)
        # bus_num, profit = odrp_sgdp.solver(_n, _m, _k, _L, _dest, _coordinates, _dist, _pb, _pc, _cr, _cb)
        ans.append([profit, bus_num])


    with open('../data/profits_IGDP_haikou_L40.csv', 'w', newline='') as out:
        csv_write = csv.writer(out, dialect='excel')
        for item in ans:
            csv_write.writerow(item)
