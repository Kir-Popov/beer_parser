import csv
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver


driver = webdriver.Chrome()


def add_space_and_beer_end(beer_name):
    i = 0
    while i != len(beer_name):
        if beer_name[i] == ' ':
            beer_name = f"{beer_name[:i]}%20{beer_name[i + 1:]}"
        i += 1
    beer_name = f"{beer_name}%20beer"
    return beer_name


def find_img_href(text):
    start_index = text.find('"img_href":"')
    if start_index == -1:
        return
    text = text[start_index + 12:]
    end_index = text.find('"')
    link = text[:end_index]
    return link


def write_file(data, beer_id):
    filename = f"{str(beer_id)}.png"
    with open(filename, 'wb') as file:
        file.write(data)


def find_first_image_link(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    first_image_link = soup.find('a', class_='serp-item__link').get('href')
    return first_image_link


def find_download_link(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    download_link = soup.find("img", class_="MMImage-Origin").get("src")
    print(download_link)
    return download_link


def main():
    url = "https://yandex.ru"
    f = open('log.txt', 'w')
    driver.get(url)
    time.sleep(20)
    with open('beer.csv') as File:
        reader = csv.reader(File, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        k = 0
        for row in reader:
            if k == 0:
                k += 1
                continue

            beer_id = row[0]
            beer_name = row[1]

            print(beer_id, beer_name)
            search_link = f"https://yandex.ru/images/search?text={add_space_and_beer_end(beer_name)}"
            try:
                """Взять первую картинку с сайта"""
                first_link = url + find_first_image_link(search_link)
                print(first_link)
                download_link = find_download_link(first_link)
                if download_link[0] != 'h':
                    download_link = "http:" + download_link
                driver.get(download_link)
                img = requests.get(download_link)
                write_file(img.content, beer_id)
            except Exception as err:
                f.write(str(err))
                f.write(beer_id + " " + beer_name)
                continue


if __name__ == '__main__':
    main()

