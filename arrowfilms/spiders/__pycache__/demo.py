import json
data = {
            'ProductsPerPage': 12,
            'RequestingPageNumber': 1,
            'ProductionDateDecadeStart': 1900,
            'ProductionDateDecadeEnd': 2020,
            'ReleaseDateDecadeStart': 2003,
            'ReleaseDateDecadeEnd': 2021,
            'SortByField': 'release_date',
            'IsSortByAscendin':'false'
        }
print(json.dumps(data))