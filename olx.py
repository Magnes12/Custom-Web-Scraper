import sys
import requests
import openpyxl
import time
import urllib.parse
from olx_locs import olx_locations_rent, base_olx_url_rent, olx_locations_sale, base_olx_url_sale
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlencode


def create_excel(file_name):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = 'OLX WYNAJEM'

    sheet['A1'] = 'Tytuł'
    sheet['B1'] = 'Cena [zł]'
    sheet['C1'] = 'Lokacja'
    sheet['D1'] = 'Powierzchnia [m2]'
    sheet['E1'] = 'URL'

    wb.save(file_name)
    return wb, sheet


def title(soup):
    title_element = soup.find_all('h4', {'class': 'css-1s3qyje'})
    print(f"Znaleziono {len(title_element)} ogłoszeń. \n")
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
    area_element = soup.find_all('span', {'class': 'css-1cd0guq'})
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


def scrape_olx_data(wb, sheet, base_url, olx_locations):

    previous_url = None
    row_number = 2

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

            parsed_url = urllib.parse.urlparse(response_url)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            page = query_params.get('page', ['1'])[0]
            print(f"Strona: {page}")

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
                print(f"Brak kolejnej strony.\n")
                break

            full_url = next_page_url


def olx_main():
    excel_file = "LOKALE.xlsx"
    wb, sheet = create_excel(excel_file)

    print("OGŁOSZENIA OLX WYNAJEM. \n")
    scrape_olx_data(wb, sheet, base_olx_url_rent, olx_locations_rent)

    sheet = wb.create_sheet(title="OLX SPRZEDAŻ")
    sheet = wb["OLX SPRZEDAŻ"]
  
    sheet['A1'] = 'Tytuł'
    sheet['B1'] = 'Cena [zł]'
    sheet['C1'] = 'Lokacja'
    sheet['D1'] = 'Powierzchnia [m2]'
    sheet['E1'] = 'URL'

    print("OGŁOSZENIA OLX SPRZEDAŻ. \n")
    scrape_olx_data(wb, sheet, base_olx_url_sale, olx_locations_sale)

    wb.save(excel_file)
    print("Excel zapisany dla OLX.\n")
