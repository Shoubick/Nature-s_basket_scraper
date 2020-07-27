import csv
from wget import download
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import os
import re


def scroll(driver, timeout):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(timeout)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height


def replace_ill_char(name):
    illegal_char = ['/', '%', '<', '>', '?', '*', '"', '|', ':']
    for symbol in illegal_char:
        name = name.replace(symbol, '')
    return name


def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome('chromedriver.exe')
    i = 0
    link_list = open('links.txt', 'r').readlines()
    for link in link_list:
        driver.get(link)
        time.sleep(5)
        scroll(driver, 3)

        html = driver.execute_script("return document.documentElement.outerHTML")
        soup = bs(html, 'html.parser')
        prod_list = soup.select('div[class*="divOuterStructure_Search_"]')

        directory = 'All_Data\\' + link.replace('https://www.naturesbasket.co.in/Online-grocery-shopping/', '').replace(
            '/', '\\').replace('\n', '').replace('_', '')
        directory = re.sub("\\d", '', directory)

        try:
            os.makedirs(directory + '\\images')
        except FileExistsError:
            pass

        rows = []

        for products in prod_list:
            name = products.find('a', {'class': 'search_Ptitle linkdisabled'}).text
            name = replace_ill_char(name)
            img_url = products.find('img')['src']
            price = products.find('span', {'class': 'search_PSellingP'}).text.replace('MRP', '').replace('₹', 'Rs. ')
            try:
                quantity = products.find('div', {'class': 'productvariantdiv'}).text
            except AttributeError:
                quantity = products.find('div', {'class': 'productvariantdivsoldout'}).text

            rows.append([name, price, quantity])
            img_name = directory + 'images\\' + name + '.jpg'
            download(img_url, img_name)

        fields = ['name', 'price', 'quantity']
        with open(os.path.join(directory, 'data.csv'), 'w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
            writer.writerows(rows)

        print('Data extracted from', link)
        i += 1
    return i


if __name__ == '__main__':
    print(main())
