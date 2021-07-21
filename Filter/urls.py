from django.urls import path
from Filter.views import *
from Filter.Views import *

urlpatterns = [
    path('API/prova', prova, name="prova"),
    path('API/FilterCSV', FilterCSV.as_view(), name="FilterCSV"),
]

