from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView

from Filter.Filters import *
from PIL import Image, ImageFile
from io import StringIO, BytesIO
from requests_cache import CachedSession

import pandas as pd
import requests
from hashlib import sha1


class FilterCSV(APIView):  # Extend from the view you need

    session = CachedSession(expire_after=86400) # 1 day in seconds

    available_filters = {'MemeDetector': MemeDetector(),
                         # 'NSFWClassifier': 2,
                         'PublicPrivateClassifier': PublicPrivateClassifier(),
                         'PeopleDetector': PeopleDetector()}

    @staticmethod
    def filter(column_name, filter_name_list, confidence_threshold_list, csv_url_or_file='', df=None):
        if df is not None and csv_url_or_file:
            return Response("filter. You cannot specify url/file and dataframe.", status=HTTP_500_INTERNAL_SERVER_ERROR)

        if df is None and not csv_url_or_file:
            return Response("filter. You have to specify url/file or dataframe.", status=HTTP_500_INTERNAL_SERVER_ERROR)
        if df is None:
            try:
                # Create a pandas dataframe from an StringIO object or a link
                csv_dataframe = pd.read_csv(csv_url_or_file, error_bad_lines=False)
                # error_bad_lines will be deprecated. Since pandas version 1.3 use on_bad_lines='skip'
                # Same meaning: if a line is badly formatted skip it
            except ValueError as e:
                return Response("filter. {}.".format(e), status=HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response("filter. {}.".format(e), status=HTTP_400_BAD_REQUEST)
        else:
            csv_dataframe = df

        if not column_name:
            return Response("filter. 'column_name' parameters is not valid.", status=HTTP_400_BAD_REQUEST)

        if not confidence_threshold_list:
            return Response("filter. 'confidence_threshold_list' parameters is not valid.", status=HTTP_400_BAD_REQUEST)

        # Check each confidence 0 < = threshold  <= 1
        for confidence in confidence_threshold_list:
            if not 0 <= float(confidence) <= 1:
                return Response(
                    "filter. 'confidence_threshold_list' value '{}' is not valid.".format(confidence_threshold_list),
                    status=HTTP_400_BAD_REQUEST)

        # Check if the requested filter is available. Case sensitive!
        for c_filter in filter_name_list:
            if c_filter not in FilterCSV.available_filters.keys():
                return Response(
                    "filter. '{}' filter is not available. Only {}.".format(c_filter,
                                                                            ', '.join(list(
                                                                                FilterCSV.available_filters.keys()))),
                    status=HTTP_400_BAD_REQUEST)

        # The number of thresholds and filters should be the same
        if len(filter_name_list) != len(confidence_threshold_list):
            return Response('filter. The length of filter_name_list and confidence_threshold_list should be the same',
                            status=HTTP_400_BAD_REQUEST)

        # If we have a duplicate requested filter, the corresponding column name in the df
        # will be overwritten
        if len(filter_name_list) != len(set(filter_name_list)):
            return Response('filter. There is at least one duplicate filter', status=HTTP_400_BAD_REQUEST)

        # The first threshold in the list corresponds to the first filter in the list, and so on
        filter_and_threshold = list(zip(filter_name_list, confidence_threshold_list))

        # Check if the media url column is a column of the csv
        if column_name not in csv_dataframe.columns:
            return Response("filter. '{}' is not a column of the csv file.".format(column_name),
                            status=HTTP_400_BAD_REQUEST)

        # set to store the hashes of the images to avoid duplicates
        image_hashes = set()

        # Iter over the csv dataframe row by row
        for index, row in csv_dataframe.iterrows():
            try:
                # Download the image
                url = str(row[column_name])
                r = FilterCSV.session.get(url=url)
                ImageFile.LOAD_TRUNCATED_IMAGES = True
                image_data = Image.open(BytesIO(r.content)).convert('RGB')

                # Compute the hash of the image
                current_hash = sha1(r.content).hexdigest()

                # Check if is a duplicate: if so, delete the row, otherwise update image_hashes
                if current_hash in image_hashes:
                    csv_dataframe.drop(index, inplace=True)
                    continue
                else:
                    image_hashes.add(current_hash)

                # For each requested filter, filter the image
                for filter_name, threshold in filter_and_threshold:
                    c_filter = FilterCSV.available_filters[filter_name]
                    accepted, confidence, detailed_out = c_filter.classify(pil_image=image_data)
                    # If accepted, save the confidence, otherwise delete the row
                    if accepted and confidence >= float(threshold):
                        csv_dataframe.loc[index, filter_name] = confidence
                    else:
                        csv_dataframe.drop(index, inplace=True)
                        break

            except Exception as e:
                csv_dataframe.drop(index, inplace=True)

        result_csv = StringIO()
        csv_dataframe.to_csv(result_csv, index=False)

        response_file = result_csv.getvalue()

        response = HttpResponse(response_file)
        response['Content-Type'] = 'application/CSV'
        response['Content-Disposition'] = 'attachment; filename=result.csv'
        return response

    def get(self, request, *args, **kwargs):

        params = request.query_params

        csv_url = params.get('csv_url', None)
        column_name = params.get('column_name', None)
        filter_name_list = params.getlist('filter_name_list', [])
        confidence_threshold_list = params.getlist('confidence_threshold_list', [])

        return FilterCSV.filter(csv_url_or_file=csv_url,
                                column_name=column_name,
                                filter_name_list=filter_name_list,
                                confidence_threshold_list=confidence_threshold_list)

    def post(self, request, *args, **kwargs):

        params = dict(request.data)

        csv_file = str(params.get('csv_file'))
        column_name = str(params.get('column_name'))
        filter_name_list = list(params.get('filter_name_list'))
        confidence_threshold_list = list(params.get('confidence_threshold_list'))

        if not csv_file:
            return Response("filterImage. 'csv_file' parameters is not valid.", status=HTTP_400_BAD_REQUEST)

        return FilterCSV.filter(csv_url_or_file=StringIO(csv_file),
                                column_name=column_name,
                                filter_name_list=filter_name_list,
                                confidence_threshold_list=confidence_threshold_list)
