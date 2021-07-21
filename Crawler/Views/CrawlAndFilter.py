from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response

from Crawler.Engine import crawl, authenticate
import tweepy

from django.conf import settings
from Filter.Views.FilterCSV import FilterCSV


class CrawlAndFilter(APIView):  # Extend from the view you need

    @staticmethod
    def crawlAndFilter(consumer_key, consumer_secret, query, count, column_name, filter_name_list,
                       confidence_threshold_list):
        api = authenticate(consumer_key=consumer_key, consumer_secret=consumer_secret)
        if not api:
            return Response('CrawlAndFilter. Not able to connect to twitter API.', HTTP_400_BAD_REQUEST)
        else:
            df = crawl(api=api, query=query, count=count)
            print('fine crawler', len(df))
            if type(df) == tweepy.error.TweepError:
                return Response('CrawlAndFilter. Error with twitter: {}.'.format(df), HTTP_400_BAD_REQUEST)

            return FilterCSV.filter(df=df,
                                    column_name=column_name,
                                    filter_name_list=filter_name_list,
                                    confidence_threshold_list=confidence_threshold_list)

    def get(self, request, *args, **kwargs):

        diz = request.query_params

        consumer_key = diz.get('consumer_key', settings.TWITTER_CONSUMER_KEY)
        consumer_secret = diz.get('consumer_secret', settings.TWITTER_CONSUMER_SECRET)
        query = diz.get('query', None)
        count = int(diz.get('count', 200))

        if not consumer_key or not consumer_secret or not query or not count:
            return Response('CrawlCSV. Missing parameter.', HTTP_400_BAD_REQUEST)

        column_name = diz.get('column_name', None)
        filter_name_list = diz.getlist('filter_name_list', [])
        confidence_threshold_list = diz.getlist('confidence_threshold_list', [])

        return self.crawlAndFilter(consumer_key=consumer_key, consumer_secret=consumer_secret, query=query, count=count,
                                   column_name=column_name, filter_name_list=filter_name_list,
                                   confidence_threshold_list=confidence_threshold_list)

    def post(self, request, *args, **kwargs):

        # This code will be executed in a POST request

        diz = dict(request.data)

        # CRAWLER PARAMETERS

        consumer_key = diz.get('consumer_key', settings.TWITTER_CONSUMER_KEY)
        consumer_secret = diz.get('consumer_secret', settings.TWITTER_CONSUMER_SECRET)
        query = diz.get('query', None)
        count = int(diz.get('count', 200))

        # FILTER PARAMETERS

        column_name = str(diz.get('column_name'))
        filter_name_list = diz.get('filter_name_list')
        confidence_threshold_list = diz.get('confidence_threshold_list')

        if not query or not count:
            return Response('CrawlAndFilter. Missing parameter.', HTTP_400_BAD_REQUEST)

        return self.crawlAndFilter(consumer_key=consumer_key, consumer_secret=consumer_secret, query=query, count=count,
                                   column_name=column_name, filter_name_list=filter_name_list,
                                   confidence_threshold_list=confidence_threshold_list)
