base_otodom_url_sale = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/"
base_otodom_url_rent = "https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/"

locations_otodom_sale = {
    "warszawa": {
        "path": "mazowieckie/warszawa/warszawa/warszawa",
        "params": {
            'limit': '36',
            'ownerTypeSingleSelect': 'ALL',
            'priceMax': '750000',
            'by': 'BEST_MATCH',
            'direction': 'DESC',
            'viewType': 'listing',
            'areaMin': '50',
        }
    }
}
locations_otodom_rent = {
    "warszawa": {
        "path": "mazowieckie/warszawa/warszawa/warszawa",
        "params": {
            'limit': '36',
            'ownerTypeSingleSelect': 'ALL',
            'priceMax': '750000',
            'by': 'BEST_MATCH',
            'direction': 'DESC',
            'viewType': 'listing',
            'areaMin': '50',
            'priceMax': '12000',
        }
    }
}
