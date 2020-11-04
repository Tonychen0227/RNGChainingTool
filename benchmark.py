import json

from search import search_details


class Benchmark:
    def __init__(self):
        with open(f'DemoPlat.json') as json_file:
            existing = json.load(json_file)

        existing["Maxdelay"] = "7000"

        search_details(existing, True)
