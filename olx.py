import os
import sys
import requests
import openpyxl
import time
from olx_locs import olx_locations, base_olx_url
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlencode


def create_excel(file_name):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = 'OLX'

    sheet['A1'] = 'Tytuł'
    sheet['B1'] = 'Cena [zł]'
    sheet['C1'] = 'Lokacja'
    sheet['D1'] = 'Powierzchnia [m2]'
    sheet['E1'] = 'URL'

    wb.save(file_name)
    return wb, sheet


def title(soup):
    title_element = soup.find_all('h6', {'class': 'css-1wxaaza'})
    print(f"Znaleziono {len(title_element)} ogłoszeń")
    return [title.text for title in title_element]


def price(soup):
    price_element = soup.find_all('p', {'data-testid': 'ad-price',
                                        'class': 'css-13afqrm'})
    return [price.text.split('zł')[0] if 'zł' in price.text else price.text for price in price_element]


def loc(soup):
    localization_element = soup.find_all('p', {'data-testid': 'location-date',
                                               'class': 'css-1mwdrlh'})
    return [loc.text.split('-')[0] for loc in localization_element if loc]


def area(soup):
    area_element = soup.find_all('span', {'class': 'css-643j0o'})
    return [area.text.split('-')[0].split('m')[0] if 'm' in area.text else '' for area in area_element]


def url_site(soup):
    links_element = soup.find_all('div', {'data-cy': 'ad-card-title'})
    links = [div.find('a').get('href') for div in links_element if div.find('a')]
    return links


def get_next_page_url(soup):
    next_page_link = soup.find('a', {'data-testid': 'pagination-forward'})
    if next_page_link:
        return urljoin("https://www.olx.pl", next_page_link.get('href'))
    return None


def olx_main():
    excel_file = "LOKALE.xlsx"
    wb, sheet = create_excel(excel_file)

    base_url = base_olx_url

    previous_url = None
    row_number = 2

    print("OGŁOSZENIA OLX")

    for location, data in olx_locations.items():
        full_url = f"{base_url}{data['path']}?{urlencode(data['params'])}"

        while True:
            try:
                response = requests.get(full_url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Błąd pobierania strony: {e}")
                sys.exit()

            response_url = response.url

            soup = BeautifulSoup(response.text, 'html.parser')

            time.sleep(1)

            if previous_url == response_url:

                print("Brak kolejnej strony. Zakończono przetwarzanie.\n")
                break

            print(f"Lokalizacja: {location}")
            print(f"Strona: {response_url}")

            title_text = title(soup)
            price_text = price(soup)
            loc_text = loc(soup)
            area_text = area(soup)
            url_site_text = url_site(soup)

            for t, p, l, a, u in zip(title_text, price_text, loc_text, area_text, url_site_text):

                if u.startswith('/d/'):
                    u = f"https://www.olx.pl{u}"

                sheet[f'A{row_number}'].value = t

                sheet[f'B{row_number}'].value = p
                sheet[f'B{row_number}'].number_format = '#,##0.00 [$zł-415];[Red]-#,##0.00 [$zł-415]'

                sheet[f'C{row_number}'].value = l
                sheet[f'D{row_number}'].value = a
                sheet[f'D{row_number}'].number_format = '0'

                sheet[f'E{row_number}'].hyperlink = u
                sheet[f'E{row_number}'].style = "Hyperlink"

                row_number += 1

            previous_url = response_url

            next_page_url = get_next_page_url(soup)

            if not next_page_url:
                print(f"Brak kolejnej strony dla lokalizacji: {location}.\n")
                break

            full_url = next_page_url

    wb.save(excel_file)
    print("Excel zapisany dla wszystkich lokalizacji OLX.\n")


if __name__ == "__main__":
    olx_main()
