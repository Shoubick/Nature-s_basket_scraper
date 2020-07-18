""" Due to occasional inconsistent data , given code scrapes the website twice (can be changed during function call) to get all category names and merges
both files """

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import shutil

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')


def cat_generator(x=2):
    os.makedirs('data')
    for i in range(x):

        driver = webdriver.Chrome()

        url = 'https://www.naturesbasket.co.in'
        driver.get(url)

        time.sleep(3)  # increase for longer loading times

        html = driver.execute_script('return document.documentElement.outerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        filename = 'temp' + str(i) + '.txt'
        file = open(os.path.join('data', filename), 'w')

        menu = soup.findAll('div', {'class': 'mainsupercatnav'})
        category = menu[0].findAll('a')
        for item in category:
            file.write(item.text + '\n')

        sub_cat = soup.findAll('div', {'id': 'divCategoryPopup1'})
        cat_list = sub_cat[0].findAll('a')
        for cat in cat_list:
            file.write(cat.text + '\n')

        file.close()
        driver.close()
    unify(x)
    shutil.rmtree('data')


def unify(x):
    cat_list = []
    for i in range(x):
        filename = 'temp' + str(i) + '.txt'
        file = open(os.path.join('data', filename), 'r')
        for cat in file:
            cat_list.append(cat)
        file.close()

    unified_list = set(cat_list)
    file = open('category.txt', 'w')
    for category in unified_list:
        file.write(category)
    file.close()


if __name__ == "__main__":
    cat_generator()
