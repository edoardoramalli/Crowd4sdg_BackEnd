import requests
import pandas as pd

server = '131.175.120.2:7777'
local = '127.0.0.1:8000'

address = server
print('Address:', address)

#  ----------------------    TEST CONNECTION   ------------------------
r = requests.get(url=f'http://{address}/CheckConnection')
print('TEST CONNECTION --> ', r.text)

#  ----------------------   FILTER CSV  POST EXAMPLE   ------------------------
print('FILTER CSV POST')

path = 'test.csv'

params = {'filter_name_list': ['PeopleDetector', 'MemeDetector'],
          'confidence_threshold_list': [0.98, 0.80],
          'column_name': 'media_url',
          'csv_file': open(path, 'r').read()
          }

r = requests.post(url=f'http://{address}/Filter/API/FilterCSV', json=params)

if r.status_code == 200:
    with open('result_filter_post.csv', 'w+') as file:
        file.write(r.text)
else:
    print('Error {} - {}'.format(r.status_code, r.text))

#  ----------------------   FILTER CSV  GET EXAMPLE   ------------------------
print('FILTER CSV GET')

params = {'filter_name_list': ['PeopleDetector', 'MemeDetector'],
          'confidence_threshold_list': [0.98, 0.89],
          'column_name': 'media_url',
          'csv_url': 'https://drive.google.com/uc?export=download&id=12hy5NRkFiNG2lI9t6oXQ_12_QDUQz94c'
          }

r = requests.get(url=f'http://{address}/Filter/API/FilterCSV', params=params)

if r.status_code == 200:
    with open('result_filter_get.csv', 'w+') as file:
        file.write(r.text)
else:
    print('Error {} - {}'.format(r.status_code, r.text))

#  ----------------------   CRAWLER CSV  GET EXAMPLE   ------------------------
print('CRAWLER CSV GET')

r = requests.get(f'http://{address}/Crawler/API/CrawlCSV',
                 params={
                     # 'consumer_key': 'consumer_key_here',  # Optional
                     # 'consumer_secret': 'consumer_secret_here', # Optional
                     'query': 'elephant',
                     'count': 10})

if r.status_code == 200:
    with open('result_crawler_get.csv', 'w+') as file:
        file.write(r.text)

    df_crawler_get = pd.read_csv('result_crawler_get.csv')
    print(df_crawler_get.head)
else:
    print('Error {} - {}'.format(r.status_code, r.text))

#  ----------------------   CRAWLER CSV POST EXAMPLE   ------------------------
print('CRAWLER CSV POST')

r = requests.post(f'http://{address}/Crawler/API/CrawlCSV',
                  json={
                      # 'consumer_key': 'consumer_key_here',  # Optional
                      # 'consumer_secret': 'consumer_secret_here', # Optional
                      'query': 'dog',
                      'count': 1000})

if r.status_code == 200:
    with open('result_crawler_post.csv', 'w+') as file:
        file.write(r.text)
    df_crawler_post = pd.read_csv('result_crawler_post.csv')
    print(df_crawler_post.head)
else:
    print('Error {} - {}'.format(r.status_code, r.text))

#  ----------------------   CRAWL and FILTER GET EXAMPLE   ------------------------
print('CRAWL and FILTER GET')

r = requests.get(f'http://{address}/Crawler/API/CrawlAndFilter',
                 params={
                     'confidence_threshold_list': [0.89],
                     'filter_name_list': ['MemeDetector'],
                     'column_name': 'media_url',
                     'query': 'dog',
                     'count': 5})

if r.status_code == 200:
    with open('result_crawler_filter_get.csv', 'w+') as file:
        file.write(r.text)
    df_crawler_post = pd.read_csv('result_crawler_filter_get.csv')
    print(df_crawler_post.head)
else:
    print('Error {} - {}'.format(r.status_code, r.text))

#  ----------------------   CRAWL and FILTER POST EXAMPLE   ------------------------
print('CRAWL and FILTER POST')

r = requests.post(f'http://{address}/Crawler/API/CrawlAndFilter',
                  json={
                      'confidence_threshold_list': [0.89],
                      'filter_name_list': ['MemeDetector'],
                      'column_name': 'media_url',
                      'query': 'dog',
                      'count': 5})

if r.status_code == 200:
    with open('result_crawler_filter_post.csv', 'w+') as file:
        file.write(r.text)
    df_crawler_post = pd.read_csv('result_crawler_filter_post.csv')
    print(df_crawler_post.head)
else:
    print('Error {} - {}'.format(r.status_code, r.text))
