import requests


# r = requests.get(url='http://127.0.0.1:8000/Filter/API/CheckConnection')
#
# print(r.status_code)
# print(r.text)
#
# exit()



#  ----------------------    POST EXAMPLE   ------------------------

path = 'path/to/test.csv'

params = {'filter_name_list': ['PeopleDetector', 'MemeDetector', 'PublicPrivateClassifier'],
          'confidence_threshold_list': [0.98, 0.89, 0.93],
          'column_name': 'media_url',
          'csv_file': open(path, 'r').read()
          }

r = requests.post(url='http://ip:port/Filter/API/filterImage', json=params)

with open('result1.csv', 'w+') as file:
    file.write(r.text)


#  ----------------------    GET EXAMPLE   ------------------------

params = {'filter_name_list': ['PeopleDetector', 'MemeDetector', 'PublicPrivateClassifier'],
          'confidence_threshold_list': [0.98, 0.89, 0.93],
          'column_name': 'media_url',
          'csv_url': 'https://drive.google.com/uc?export=download&id=12hy5NRkFiNG2lI9t6oXQ_12_QDUQz94c'
          }

r = requests.get(url='http://ip:port/Filter/API/filterImageURL', params=params)


with open('result2.csv', 'w+') as file:
    file.write(r.text)



