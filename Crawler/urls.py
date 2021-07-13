from django.urls import path
from Crawler.views import *

urlpatterns = [
    # path('API/executeOptimaPP', views.executeOptimaPP, name="executeOptimaPP"),
    # path('API/prova', prova, name="prova"),
    # path('API/filterImage', filterImage, name="filterImage"),
    # path('API/filterImageURL', filterImageURL, name="filterImageURL"),
    # path('API/CheckConnection', CheckConnection, name="CheckConnection"),
    path('API/CrawlCSV', CrawlCSV.as_view(), name='crawlCSV'),
]

