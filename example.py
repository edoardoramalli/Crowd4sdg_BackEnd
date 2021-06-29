import requests

server = '131.175.120.2:7777'
local = '127.0.0.1:8000'

# r = requests.get(url='http://127.0.0.1:8000/Filter/API/CheckConnection')
#
# print(r.status_code)
# print(r.text)
#
# exit()



#  ----------------------    POST EXAMPLE   ------------------------

path = 'test.csv'

params = {'filter_name_list': ['PeopleDetector', 'MemeDetector'],
          'confidence_threshold_list': [0.98, 0.89],
          'column_name': 'media_url',
          'csv_file': open(path, 'r').read()
          }

r = requests.post(url=f'http://{server}/Filter/API/filterImage', json=params)

if r.status_code == 200:
    with open('result1.csv', 'w+') as file:
        file.write(r.text)
else:
    print('Error {} - {}'.format(r.status_code, r.text))



# #  ----------------------    GET EXAMPLE   ------------------------
#
# params = {'filter_name_list': ['PeopleDetector', 'MemeDetector', 'PublicPrivateClassifier'],
#           'confidence_threshold_list': [0.98, 0.89, 0.93],
#           'column_name': 'media_url',
#           # 'csv_url': 'https://drive.google.com/uc?export=download&id=12hy5NRkFiNG2lI9t6oXQ_12_QDUQz94c'
#           'csv_url': 'https://www.dropbox.com/s/6sddfzu87oz7z83/crawl-dedup-2020082017-w34-project162-10tweets.csv?dl=0'
#           }
#
# r = requests.get(url='http://131.175.120.2:7777/Filter/API/filterImageURL', params=params)
#
#
# with open('result2.csv', 'w+') as file:
#     file.write(r.text)
#
#
#
