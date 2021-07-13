import pandas as pd
import requests
from PIL import Image, ImageFile
from io import StringIO, BytesIO

# r = requests.get('http://127.0.0.1:8000/Crawler/API/CrawlCSV',
#                  params={'consumer_key': 'BIIA4eAxf6UkpSNtxAEZLciUn',
#                          'consumer_secret': 'gaXrea9UecJ61XXgvIhDHstjE6QhfNhgMoiFeD2S7LTWjnkKBJ',
#                          'query': 'elephant',
#                          'count': 10})
# print(r.status_code)
# print(r.text)

r = requests.post('http://131.175.120.2:7777/Crawler/API/CrawlCSV',
                  json={'consumer_key': 'BIIA4eAxf6UkpSNtxAEZLciUn',
                        'consumer_secret': 'gaXrea9UecJ61XXgvIhDHstjE6QhfNhgMoiFeD2S7LTWjnkKBJ',
                        'query': 'elephant',
                        'count': 10})

with open('result_crawler.csv', 'w+') as file:
    file.write(r.text)


import pandas as pd

df = pd.read_csv('result_crawler.csv')

print(df.head)

