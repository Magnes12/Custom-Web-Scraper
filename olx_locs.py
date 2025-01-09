base_olx_url_sale = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/"
base_olx_url_rent = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/"

olx_locations_sale = {
    "warszawa": {
        "path": "warszawa",
        "params": {
            'search[filter_float_m:from]': '50'
        }
    }
}
olx_locations_rent = {
    "warszawa": {
        "path": "warszawa",
        "params": {
            'search[filter_float_m:from]': '50',
            'search[filter_float_price:to]': '12000'
        }
    }
}
