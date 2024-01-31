import requests
import time
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# price_to = int(input("Maximum price ?: "))
# area_from = int(input("Area from ?: "))
# area_up_to = int(input("Area up to ?: "))

def title():
    title_element = soup.find_all('h6')
    titles = [title.text for title in title_element]
    return titles


def price():
    price_element = soup.find_all('p', {'data-testid': 'ad-price', 'class': 'css-10b0gli er34gjf0'})
    prices = [price.text for price in price_element]
    return prices


def loc():
    localization_element = soup.find_all('p', {'data-testid': 'location-date', 'class': 'css-1a4brun er34gjf0'})
    addresses = [loc.text.split('-')[0] for loc in localization_element]
    return addresses


def area():
    area_element = soup.find_all('span', {'class': 'css-643j0o'})
    areas = [(area.text.split('-')[0], area.text.split('-')[1] if len(area.text.split('-')) > 1 else None) for area in area_element]
    return areas


csv_file_name = "olx_data.csv"

with open(csv_file_name, 'w', newline='', encoding='utf=8') as csv_file:

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Title', 'Price', 'Location', 'Area'])

    page_number = 1

    while True:

        base_url = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/bialystok/"
        url = urljoin(base_url, f"?page={page_number}&search%5Bfilter_float_m%3Afrom%5D=40&search%5Bfilter_float_m%3Ato%5D=80&search%5Bfilter_float_price%3Ato%5D=500000")

        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        ul_element = soup.find('ul', class_='pagination-list')
        li_elements = ul_element.find_all('li')
        number_of_li_elements = int(len(li_elements))+1

        if page_number <= number_of_li_elements:

            titles = title()
            prices = price()
            addresses = loc()
            areas = area()

            for i in range(len(titles)):
                csv_writer.writerow([titles[i], prices[i], addresses[i], areas[i]])

            time.sleep(1)
            page_number += 1
        else:
            break
