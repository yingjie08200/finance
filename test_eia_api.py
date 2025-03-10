import requests
import pprint
apiKey = 'nLYpSpW9IW8bwQX174Ld8k3sMP6PKhtvjzhBqhtA'
apiRoute = 'electricity/retail-sales/data'
filter = 'frequency=monthly&data[0]=customers&data[1]=price&start=2023-02&end=2024-12&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000'

resp = requests.get(f'https://api.eia.gov/v2/{apiRoute}/?{filter}&api_key={apiKey}')
pprint.pprint(resp.json())
apiRoute = 'natural-gas/pri/fut/data'
filter = 'frequency=weekly&data[0]=value&facets[series][]=RNGC3&start=2024-01-01&end=2025-01-31&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000'

resp = requests.get(f'https://api.eia.gov/v2/{apiRoute}/?{filter}&api_key={apiKey}')
pprint.pprint(resp.json())
