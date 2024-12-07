from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.dataframe, name='df'),
    path('/upload',views.dataframe_upload, name='df_upload'),
    path('/search',views.dataframe_search1, name='df_search'),
    path('laws',views.laws,name='laws'),
    path('laws/binomiale', views.Binomiale, name='binomiale'),
    path('laws/bernoulli', views.Bernoulli, name='bernoulli'),
    path('laws/normale', views.Normale, name='normale'),
    path('laws/poisson', views.Poisson, name='poisson'),
    path('laws/uniforme', views.Uniforme, name='uniforme'),
    path('laws/exponentielle', views.Exponentielle, name='exponentielle'),
    

    ]
