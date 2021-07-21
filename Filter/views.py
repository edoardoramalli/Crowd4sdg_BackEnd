from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView

# Create your views here.

from Filter.Filters import *
from PIL import Image, ImageFile
from io import StringIO, BytesIO

from django.conf import settings
import pandas as pd
import hashlib
import csv
import os
import requests
import time

# Create SandBox
import tempfile








from django.http import StreamingHttpResponse


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


@api_view(['POST'])
def prova(request):
    print('EDOOOO')
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )
    import time

    # writer = csv.writer(response)
    #
    #
    # writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    # time.sleep(10)
    # writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    # return response

    def scrivi():
        import time
        time.sleep(5)
        return (['First row', 'Foo', 'Bar', 'Baz'])

    rows = (["Row {}".format(idx), str(idx)] for idx in range(5))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    return StreamingHttpResponse(
        (writer.writerow(scrivi()) for row in rows),
        content_type="text/csv",
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )
