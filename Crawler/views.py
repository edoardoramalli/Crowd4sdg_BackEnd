from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response

from Crawler.Engine import crawl, authenticate
from io import StringIO
from django.http import HttpResponse
import pandas as pd
import tweepy

from django.conf import settings


class CrawlCSV(APIView):  # Extend from the view you need

    def crawl_wrapper(self, consumer_key, consumer_secret, query, count):
        api = authenticate(consumer_key=consumer_key, consumer_secret=consumer_secret)
        if not api:
            return Response('CrawlCSV. Not able to connect to twitter API.', HTTP_400_BAD_REQUEST)
        else:
            df = crawl(api=api, query=query, count=count)
            if type(df) == tweepy.error.TweepError:
                return Response('CrawlCSV. Error with twitter: {}.'.format(df), HTTP_400_BAD_REQUEST)

            result_csv = StringIO()
            df.to_csv(result_csv, index=False)

            response_file = result_csv.getvalue()

            response = HttpResponse(response_file)
            response['Content-Type'] = 'application/CSV'
            response['Content-Disposition'] = 'attachment; filename=result.csv'
            return response

    def get(self, request, *args, **kwargs):

        diz = request.query_params.dict()

        consumer_key = diz.get('consumer_key', settings.TWITTER_CONSUMER_KEY)
        consumer_secret = diz.get('consumer_secret', settings.TWITTER_CONSUMER_SECRET)
        query = diz.get('query', None)
        count = int(diz.get('count', 200))

        if not consumer_key or not consumer_secret or not query or not count:
            return Response('CrawlCSV. Missing parameter.', HTTP_400_BAD_REQUEST)

        return self.crawl_wrapper(consumer_key=consumer_key, consumer_secret=consumer_secret, query=query, count=count)


    def post(self, request, *args, **kwargs):

        # This code will be executed in a POST request

        diz = dict(request.data)

        consumer_key = diz.get('consumer_key', settings.TWITTER_CONSUMER_KEY)
        consumer_secret = diz.get('consumer_secret', settings.TWITTER_CONSUMER_SECRET)
        query = diz.get('query', None)
        count = int(diz.get('count', 200))

        if not consumer_key or not consumer_secret or not query or not count:
            return Response('CrawlCSV. Missing parameter.', HTTP_400_BAD_REQUEST)

        return self.crawl_wrapper(consumer_key=consumer_key, consumer_secret=consumer_secret, query=query, count=count)


