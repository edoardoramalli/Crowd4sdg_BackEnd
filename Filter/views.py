from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from django.http import HttpResponse

# Create your views here.

from Filter.Filters import *
from PIL import Image, ImageFile
from io import StringIO, BytesIO

from django.conf import settings
import pandas as pd

import os
import requests

# Create SandBox
import tempfile

available_filters = {'MemeDetector': MemeDetector(),
                     # 'NSFWClassifier': 2,
                     'PublicPrivateClassifier': PublicPrivateClassifier(),
                     'PeopleDetector': PeopleDetector()}


def filter(df, column_name, filter_name_list, confidence_threshold_list):

    if len(filter_name_list) != len(confidence_threshold_list):
        return Response('filter. The length of filter_name_list and confidence_threshold should be the same', status=HTTP_400_BAD_REQUEST)

    threshold = dict(zip(filter_name_list, confidence_threshold_list))

    if column_name not in df.columns:
        return Response("filter. '{}' is not a column of the csv file.".format(column_name),
                        status=HTTP_400_BAD_REQUEST)

    for index, row in df.iterrows():
        url = str(row[column_name])
        r = requests.get(url=url)
        # path_image = os.path.join(sandbox, str(index)) + '.jpg'
        # open(path_image, 'wb').write(r.content)
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        # image_data = Image.open(path_image).convert('RGB')
        image_data = Image.open(BytesIO(r.content)).convert('RGB')
        for filter_name in filter_name_list:
            c_filter = available_filters[filter_name]
            accepted, confidence, detailed_out = c_filter.classify(pil_image=image_data)
            if accepted and confidence >= float(threshold[filter_name]):
                df.loc[index, filter_name] = confidence

    df = df.dropna(subset=list(filter_name_list))
    result_csv = StringIO()
    df.to_csv(result_csv, index=False)

    response_file = result_csv.getvalue()

    response = HttpResponse(response_file)
    response['Content-Type'] = 'application/CSV'
    response['Content-Disposition'] = 'attachment; filename=result.csv'
    return response



@api_view(['GET'])
def CheckConnection(request):
    # DO MY STUff

    return Response('Hi professor!', HTTP_200_OK)

@api_view(['GET'])
def filterImageURL(request):

    params = dict(request.query_params)

    csv_url = params.get('csv_url')
    column_name = params.get('column_name')
    filter_name_list = params.get('filter_name_list')
    confidence_threshold_list = params.get('confidence_threshold_list')

    if not csv_url:
        return Response("filterImageURL. 'csv_url' parameters is not valid.", status=HTTP_400_BAD_REQUEST)

    if not column_name:
        return Response("filterImageURL. 'column_name' parameters is not valid.", status=HTTP_400_BAD_REQUEST)

    if not confidence_threshold_list:
        return Response("filterImageURL. 'confidence_threshold' parameters is not valid.", status=HTTP_400_BAD_REQUEST)

    confidence_threshold = list(confidence_threshold_list)
    column_name = str(column_name[0])
    csv_url = str(csv_url[0])

    for confidence in confidence_threshold_list:
        if not 0 <= float(confidence) <= 1:
            return Response("filterImage. 'confidence_threshold' value '{}' is not valid.".format(confidence_threshold_list),
                            status=HTTP_400_BAD_REQUEST)

    for c_filter in filter_name_list:
        if c_filter not in available_filters.keys():
            return Response(
                "filterImage. '{}' filter is not available. Only {}.".format(c_filter,
                                                                             ', '.join(list(available_filters.keys()))),
                status=HTTP_400_BAD_REQUEST)


    dataFrame = pd.read_csv(csv_url)


    return filter(df=dataFrame,
                  column_name=column_name,
                  filter_name_list=filter_name_list,
                  confidence_threshold_list=confidence_threshold_list)


@api_view(['POST'])
def filterImage(request):
    params = dict(request.data)

    csv_file = str(params.get('csv_file'))
    # csv_url = request.data.params.get('csv_url')
    column_name = str(params.get('column_name'))
    filter_name_list = list(params.get('filter_name_list'))
    confidence_threshold_list = list(params.get('confidence_threshold_list'))

    if not csv_file:
        return Response("filterImage. 'csv_file' parameters is not valid.", status=HTTP_400_BAD_REQUEST)

    if not column_name:
        return Response("filterImage. 'column_name' parameters is not valid.", status=HTTP_400_BAD_REQUEST)

    if not confidence_threshold_list:
        return Response("filterImage. 'confidence_threshold' parameters is not valid.", status=HTTP_400_BAD_REQUEST)

    for confidence in confidence_threshold_list:
        if not 0 <= float(confidence) <= 1:
            return Response("filterImage. 'confidence_threshold' value '{}' is not valid.".format(confidence_threshold_list),
                            status=HTTP_400_BAD_REQUEST)

    for c_filter in filter_name_list:
        if c_filter not in available_filters.keys():
            return Response(
                "filterImage. '{}' filter is not available. Only {}.".format(c_filter,
                                                                             ', '.join(list(available_filters.keys()))),
                status=HTTP_400_BAD_REQUEST)

    # Create Pandas from csv_file as a string

    file = StringIO(csv_file)

    dataFrame = pd.read_csv(file)

    return filter(df=dataFrame,
                  column_name=column_name,
                  filter_name_list=filter_name_list,
                  confidence_threshold_list=confidence_threshold_list)





@api_view(['POST'])
def prova(request):
    params = dict(request.data)

    f = PeopleDetector()

    h = MemeDetector()

    j = NSFWClassifier()

    a = PublicPrivateClassifier()

    path_image = os.path.join(settings.BASE_DIR, "Files/Test/img4.jpg")

    ImageFile.LOAD_TRUNCATED_IMAGES = True
    image_data = Image.open(path_image).convert('RGB')

    accepted, confidence, detailed_out = j.classify(pil_image=image_data)

    print(accepted, confidence, detailed_out)

    return Response(status=HTTP_200_OK)
