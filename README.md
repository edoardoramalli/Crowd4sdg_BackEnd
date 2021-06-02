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
nohup python /path/to/file/manage.py runserver 7777
```

- 'crowd' is the name of the anaconda environment created before
- 'nohup' keeps the services 'alive' even if you close the ssh connection
- '7777' is the port on which the services are provided
 