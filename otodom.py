import os
import sys
import requests
import openpyxl
import time
from otodom_locs import base_otodom_url, locations_otodom
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlencode


def create_excel(file_name):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = 'LOKALE'

    sheet['A1'] = 'Tytuł'
    sheet['B1'] = 'Cena [zł]'
    sheet['C1'] = 'Lokacja'
    sheet['D1'] = 'Powierzchnia [m2]'
    sheet['E1'] = 'URL'

    wb.save(file_name)
    return wb, sheet


def title(soup):
    title_element = soup.find_all('p', {'data-cy': 'listing-item-title',
                                        'class': 'css-u3orbr e1g5xnx10'})
    return [title.text for title in title_element]


def price(soup):
    price_element = soup.find_all('span', {'class': 'css-2bt9f1 evk7nst0'})
    return [price.text.split('zł')[0] for price in price_element]


def loc(soup):
    localization_element = soup.find_all('p', {'class': 'css-42r2ms eejmx80'})
    return [loc.text for loc in localization_element]


def area(soup):
    area_element = soup.find_all('span', {'class': 'css-643j0o'})
    return [area.text.split('-')[0].split('m')[0] for area in area_element]


def url_site(soup):
    links_element = soup.find_all('a', {'data-cy': 'listing-item-link',
                                        'class': 'css-16vl3c1 e17g0c820'})
    links = [link.get('href') for link in links_element if link.get('href')]
    unique_links = list(dict.fromkeys(links))
    return unique_links


# def get_next_page_url(soup):
#     next_page_link = soup.find('a', {'data-testid': 'pagination-forward'})
#     if next_page_link:
#         return urljoin("https://www.olx.pl", next_page_link.get('href'))
#     return None


def main():
    excel_file = "LOKALE.xlsx"
    wb, sheet = create_excel(excel_file)

    base_url = base_otodom_url

    previous_url = None
    row_number = 2

    for location, data in locations_otodom.items():
        full_url = f"{base_url}{data['path']}?{urlencode(data['params'])}"
        print(full_url)

        while True:
            try:

                response = requests.get(full_url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Błąd pobierania strony: {e}")
                sys.exit()

            response_url = response.url
            print(response_url)

            soup = BeautifulSoup(response.text, 'html.parser')

            time.sleep(1)

            # if previous_url == response_url or not next_page_url:

            #     print("Brak kolejnej strony. Zakończono przetwarzanie.")
            #     break

            title_text = title(soup)
            price_text = price(soup)
            loc_text = loc(soup)
            area_text = area(soup)
            url_site_text = url_site(soup)

            print(title_text[1])
            print(price_text[1])
            print(loc_text[1])
            print(area_text[1])
            print(url_site_text[1])

    #         for t, p, l, a, u in zip(title_text, price_text, loc_text, area_text, url_site_text):

    #             if u.startswith('/d/'):
    #                 u = f"https://www.olx.pl{u}"

    #             sheet[f'A{row_number}'].value = t

    #             sheet[f'B{row_number}'].value = p
    #             sheet[f'B{row_number}'].number_format = '#,##0.00 [$zł-415];[Red]-#,##0.00 [$zł-415]'

    #             sheet[f'C{row_number}'].value = l
    #             sheet[f'D{row_number}'].value = a
    #             sheet[f'D{row_number}'].number_format = '0'

    #             sheet[f'E{row_number}'].hyperlink = u
    #             sheet[f'E{row_number}'].style = "Hyperlink"

    #             row_number += 1

    #         previous_url = response_url
    #         full_url = next_page_url

    #     wb.save(excel_file)
    #     print(f"Excel zapisany dla lokalizacji: {location}\n")

    # if sys.platform == "win32":
    #     os.startfile(excel_file)


if __name__ == "__main__":
    main()
