from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.dataframe, name='df'),
    path('/upload',views.dataframe_upload, name='df_upload'),
    path('/search',views.dataframe_search1, name='df_search'),
    

    ]
