#Crowd4sdg_BackEnd

## Requirements

- Install Caffe [https://caffe.berkeleyvision.org/installation.html](https://caffe.berkeleyvision.org/installation.html)

- Create a virtual environment using anaconda

    `conda create --name crowd --file requirements.txt`
    
    This instruct create a conda environment called 'crowd' installing all the dependencies listed in the requirements.txt file.
   
    Make sure the caffe library is visible from your anaconda environment

- Fill the Files/FilterModels folder with all the weights needed for ML part. [https://gitlab.iiia.csic.es/crowd4sdg/polimipipeline/-/tree/master/src/input_pipeline](https://gitlab.iiia.csic.es/crowd4sdg/polimipipeline/-/tree/master/src/input_pipeline)
    1. alexnet_places365.caffemodel
    2. coco.names
    3. deploy.prototxt
    4. deploy_alexnet_places365.prototxt
    5. ilsvrc_2012_mean.npy
    6. ImgMemeWeights.h5
    7. labels.pkl
    8. resnet_50_1by2_nsfw.caffemodel
    9. vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5
    10. yolov3.cfg
    11. yolov3.weights

## Run

Under the Files folder execute the bash script 'start.sh'.
The content of the file is the following:

```
source /path/to/miniconda3/bin/activate crowd
nohup python /path/to/file/manage.py runserver 0.0.0.0:7777
```

- 'crowd' is the name of the anaconda environment created before
- 'nohup' keeps the services 'alive' even if you close the ssh connection
- '7777' is the port on which the services are provided
<<<<<<< Updated upstream
 
 
## Using the service:

### EndPoints

To apply a filter(s) on a csv file, we can leverage two endpoints: 
- Get Request : http://127.0.0.1:7777/Filter/API/filterImageURL
- Post Request : http://127.0.0.1:7777/Filter/API/filterImage

### Parameters

The endpoints accepts the following parameters:
- 'filter_name_list' --> accept a list of filter names. Each filter is apply one after the other. The supported filter are 'PeopleDetector', 'MemeDetector', ‘PublicPrivateClassifier'
- ‘confidence_threshold_list' --> confidence threshold list. If the confidence of a filter over a twitter is below the confidence_threshold, then the twitter is discarded. The first element in this list is related to the threshold of the first filter in filter_name_list, and so on.
- 'column_name' --> the name of the column of the input csv under which could be found the media url link

In case of the GET request, we need an additional parameter:
- 'csv_url' --> the url where the machine can download the input csv file 

In case of the POST request, we need an additional parameter:
- 'csv_file' --> the string that represents the input csv file

Pay attention: until now we have blocking requests. The suggestion is not to use big csv files. Start with csv with very few rows (each rows is a
twitter) and incrementally increase the number.

### Example GET request

The request below filters a test CSV file at https://drive.google.com/uc?export=download&id=12hy5NRkFiNG2lI9t6oXQ_12_QDUQz94c using 3 consecutive filters: People Detector, MemeDetector,PublicPrivateClassifier, setting the confidence thresholds for the filters to be 0.98, 0.89, and 0.93 respectively:
- http://127.0.0.1:7777/Filter/API/filterImageURL?filter_name_list=PeopleDetector&filter_name_list=MemeDetector&filter_name_list=PublicPrivateClassifier&confidence_threshold_list=0.98&confidence_threshold_list=0.89&confidence_threshold_list=0.93&column_name=media_url&csv_url=https%3A%2F%2Fdrive.google.com%2Fuc%3Fexport%3Ddownload%26id%3D12hy5NRkFiNG2lI9t6oXQ_12_QDUQz94c

### Example POST request from Python

This request below filters the a CSV file in variable .... 
....TODO .....

## Render a new HTML Page

1. Add the html file (e.g. example.html) into the templates folder
2. Create a new endpoint in the Main/urls.py python file
```
    path('example', example_function, name='example'),
```

3. Render the HTML file implementing the endpoint in this way:

```
    def example_function(request):
        return render(request, 'example.html')
```
=======
 
>>>>>>> Stashed changes
