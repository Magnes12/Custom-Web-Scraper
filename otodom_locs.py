from urllib.parse import urlencode

base_otodom_url = "https://www.otodom.pl/pl/wyniki/sprzedaz/lokal/"

locations_otodom = {
    "warszawa": {
        "path": "mazowieckie/warszawa/warszawa/warszawa",
        "params": {
            'limit': '36',
            'ownerTypeSingleSelect': 'ALL',
            'priceMax': '750000',
            'by': 'BEST_MATCH',
            'direction': 'DESC',
            'viewType': 'listing'
        }
    },
    "grodzisk_mazowiecki": {
        "path": "mazowieckie/grodziski/grodzisk-mazowiecki/grodzisk-mazowiecki",
        "params": {
            'limit': '36',
            'ownerTypeSingleSelect': 'ALL',
            'priceMax': '750000',
            'by': 'BEST_MATCH',
            'direction': 'DESC',
            'viewType': 'listing'
        }
    },
    "zyrardow": {
        "path": "mazowieckie/zyrardowski/zyrardow/zyrardow",
        "params": {
            'limit': '36',
            'ownerTypeSingleSelect': 'ALL',
            'priceMax': '750000',
            'by': 'BEST_MATCH',
            'direction': 'DESC',
            'viewType': 'listing'
        }
    },
    "pruszkow": {
        "path": "mazowieckie/pruszkowski/pruszkow/pruszkow",
        "params": {
            'limit': '36',
            'ownerTypeSingleSelect': 'ALL',
            'priceMax': '750000',
            'by': 'BEST_MATCH',
            'direction': 'DESC',
            'viewType': 'listing'
        }
    },
    "piastow": {
        "path": "mazowieckie/pruszkowski/piastow/piastow",
        "params": {
            'limit': '36',
            'ownerTypeSingleSelect': 'ALL',
            'priceMax': '750000',
            'by': 'BEST_MATCH',
            'direction': 'DESC',
            'viewType': 'listing'
        }
    },
    "ozarow_mazowiecki": {
        "path": "mazowieckie/warszawski-zachodni/ozarow-mazowiecki/ozarow-mazowiecki",
        "params": {
            'distanceRadius': '5',
            'limit': '36',
            'ownerTypeSingleSelect': 'ALL',
            'priceMax': '750000',
            'by': 'BEST_MATCH',
            'direction': 'DESC',
            'viewType': 'listing'
        }
    },
    "oltarzew": {
        "path": "mazowieckie/warszawski-zachodni/ozarow-mazowiecki/oltarzew",
        "params": {
            'distanceRadius': '5',
            'limit': '36',
            'ownerTypeSingleSelect': 'ALL',
            'priceMax': '750000',
            'by': 'BEST_MATCH',
            'direction': 'DESC',
            'viewType': 'listing'
        }
    },
    "skierniewice": {
        "path": "lodzkie/skierniewice/skierniewice/skierniewice",
        "params": {
            'distanceRadius': '5',
            'limit': '36',
            'ownerTypeSingleSelect': 'ALL',
            'priceMax': '750000',
            'by': 'BEST_MATCH',
            'direction': 'DESC',
            'viewType': 'listing'
        }
    },
    "nowy_dwor_mazowiecki": {
        "path": "mazowieckie/nowodworski/nowy-dwor-mazowiecki/nowy-dwor-mazowiecki",
        "params": {
            'distanceRadius': '5',
            'limit': '36',
            'ownerTypeSingleSelect': 'ALL',
            'priceMax': '750000',
            'by': 'BEST_MATCH',
            'direction': 'DESC',
            'viewType': 'listing'
        }
    },
    "piaseczno": {
        "path": "mazowieckie/piaseczynski/piaseczno/piaseczno",
        "params": {
            'distanceRadius': '5',
            'limit': '36',
            'ownerTypeSingleSelect': 'ALL',
            'priceMax': '750000',
            'by': 'BEST_MATCH',
            'direction': 'DESC',
            'viewType': 'listing'
        }
    },
    "plock": {
        "path": "mazowieckie/plock/plock/plock",
        "params": {
            'distanceRadius': '5',
            'limit': '36',
            'ownerTypeSingleSelect': 'ALL',
            'priceMax': '750000',
            'by': 'BEST_MATCH',
            'direction': 'DESC',
            'viewType': 'listing'
        }
    },
    "legionowo": {
        "path": "mazowieckie/legionowski/legionowo/legionowo",
        "params": {
            'distanceRadius': '5',
            'limit': '36',
            'ownerTypeSingleSelect': 'ALL',
            'priceMax': '750000',
            'by': 'BEST_MATCH',
            'direction': 'DESC',
            'viewType': 'listing'
        }
    },
    "lomianki": {
        "path": "mazowieckie/warszawski-zachodni/lomianki/lomianki",
        "params": {
            'distanceRadius': '5',
            'limit': '36',
            'ownerTypeSingleSelect': 'ALL',
            'priceMax': '750000',
            'by': 'BEST_MATCH',
            'direction': 'DESC',
            'viewType': 'listing'
        }
    }
}


for location, data in locations_otodom.items():
    full_url = f"{base_otodom_url}{data['path']}?{urlencode(data['params'])}"
