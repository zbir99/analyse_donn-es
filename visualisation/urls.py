from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.dataframe, name='df'),
    path('/home',views.home, name='home'),
    path('/upload',views.dataframe_upload, name='df_upload'),
    path('/search',views.dataframe_search1, name='df_search'),
    path('laws',views.laws,name='laws'),
    path('laws/binomiale', views.Binomiale, name='binomiale'),
    path('laws/bernoulli', views.Bernoulli, name='bernoulli'),
    path('laws/normale', views.Normale, name='normale'),
    path('laws/poisson', views.Poisson, name='poisson'),
    path('laws/uniforme', views.Uniforme, name='uniforme'),
    path('laws/exponentielle', views.Exponentielle, name='exponentielle'),
    path('graphics/', views.graphics, name='graphics'),
    path('graphics/barplot/', views.barplot, name='barplot'),
    path('graphics/lineplot/', views.lineplot, name='lineplot'),
    path('graphics/scatterplot/', views.scatterplot, name='scatterplot'),
    path('graphics/piechart/', views.piechart, name='piechart'),
    path('graphics/histogram/', views.histogram, name='histogram'),
    path('graphics/boxplot/', views.boxplot, name='boxplot'),
    path('graphics/heatmap/', views.heatmap, name='heatmap'),
    path('graphics/violin/', views.violin, name='violin'),
    

    ]
