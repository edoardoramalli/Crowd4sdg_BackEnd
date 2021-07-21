from django.urls import path
from Crawler.views import *
from Crawler.Views import *

urlpatterns = [
    path('API/CrawlCSV', CrawlCSV.as_view(), name='crawlCSV'),
    path('API/CrawlAndFilter', CrawlAndFilter.as_view(), name='crawlCSV'),
]

