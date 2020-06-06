from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import csv

total_page = 55

if __name__ == '__main__':
    hotel = []

    url = 'https://hotel.meituan.com/chengdu'
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.userAgent'] = (
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, '
        'like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    browser = webdriver.PhantomJS(executable_path='../ext/phantomjs.exe', desired_capabilities=dcap)

    browser.get(url)

    time.sleep(5)

    for page in range(1, total_page + 1):
        print('page =', page)
        for item in browser.find_elements_by_class_name('info-wrapper'):
            addr = item.find_element_by_class_name('poi-address').text
            pos = addr.find('"')
            addr = addr[pos + 1:]
            pos = addr.find('"')
            addr = addr[:pos]
            hotel.append(addr)

        if page != total_page:
            browser.find_element_by_class_name('paginator').find_element_by_class_name('next').find_element_by_tag_name('a').click()
        time.sleep(3)

        with open('../data/hotel_address_' + str(page) + '.csv', "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file, dialect='excel')
            for item in hotel:
                row = [item]
                csv_writer.writerow(row)

    browser.quit()
    with open('../data/hotel_address_final.csv', "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, dialect='excel')
        for item in hotel:
            row = [item]
            csv_writer.writerow(row)

