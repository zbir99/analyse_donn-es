from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import pandas as pd
import io
import matplotlib.pyplot as plt
import base64
from io import BytesIO, StringIO
import seaborn as sns
import numpy as np
from . import utils
import pickle
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
import os
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
import pandas as pd  
from .forms import BinomialForm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO, BytesIO
import base64
from .forms import ExponentielleForm,TraitementForm
import json
import plotly.express as px
import matplotlib
import plotly.graph_objs as go
from scipy.stats import binom
from django.http import JsonResponse
import plotly.io as pio
from .forms import BernoulliForm 
from scipy.stats import bernoulli
matplotlib.use('Agg')
from .forms import NormaleForm 
from .forms import PoissonForm 
from .forms import UniformeForm

def dataframe(request):
    return render(request, "visualisation/dataFrameTable.html")

def dataframe_upload(request):
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            return HttpResponse("Aucun fichier téléchargé. Veuillez télécharger un fichier CSV ou Excel.")
        
        csv_file = request.FILES['csv_file']
        file_type = csv_file.name.split('.')[-1].lower()
        
        try:
            if file_type == 'csv':
                df = pd.read_csv(csv_file)
            elif file_type in ['xls', 'xlsx']:
                df = pd.read_excel(csv_file)
            else:
                return HttpResponse("Type de fichier non pris en charge. Veuillez télécharger un fichier CSV ou Excel.")
            
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            request.session['df'] = csv_buffer.getvalue()
            request.session['cols'] = list(df.columns)
            
            df_html = df.to_html(classes='table')
            context = {
                'df': df_html, 
                'cols': list(df.columns),
                'max_row': len(df) - 1
            }
            return render(request, 'visualisation/dataFrameTable.html', context)
        except Exception as e:
            return HttpResponse(f"Erreur lors du traitement du fichier : {str(e)}")
    
    return render(request, "visualisation/dataFrameTable.html")

def dataframe_search1(request):
    df_csv = request.session.get('df')
    if not df_csv:
        return HttpResponse("Aucun DataFrame chargé. Veuillez d'abord télécharger un fichier.")
    
    df = pd.read_csv(io.StringIO(df_csv))
    columns_choices = request.session.get('cols', [])
    
    if request.method == 'POST':
        parcourir_chart_type = request.POST.get('parcourir_chart')
        
        try:
            # Gestion des statistiques
            if parcourir_chart_type == 'Statistics':
                stat_type = request.POST.get('stat_type')
                column = request.POST.get('stat_column')
                
                # Vérifier si la colonne est numérique
                if not pd.to_numeric(df[column], errors='coerce').notnull().all():
                    return HttpResponse(f"La colonne {column} doit contenir uniquement des valeurs numériques.")
                
                # Convertir la colonne en numérique
                df[column] = pd.to_numeric(df[column], errors='coerce')
                
                stats_result = {}
                if stat_type == 'mean':
                    result = df[column].mean()
                    resultat = f"La moyenne de la colonne {column} est : {result:.2f}"
                elif stat_type == 'median':
                    result = df[column].median()
                    resultat = f"La médiane de la colonne {column} est : {result:.2f}"
                elif stat_type == 'mode':
                    result = df[column].mode()[0]
                    resultat = f"Le mode de la colonne {column} est : {result}"
                elif stat_type == 'all':
                    stats_result = {
                        'Moyenne': df[column].mean(),
                        'Médiane': df[column].median(),
                        'Mode': df[column].mode()[0],
                        'Écart-type': df[column].std(),
                        'Min': df[column].min(),
                        'Max': df[column].max()
                    }
                    resultat = "\n".join([f"{k}: {v:.2f}" for k, v in stats_result.items()])
                
                context = {
                    'df': df.to_html(classes='table table-bordered'),
                    'cols': columns_choices,
                    'resultat': resultat,
                    'max_row': len(df) - 1
                }
                return render(request, 'visualisation/dataFrameTable.html', context)
            
            # Code existant pour FindElem
            elif parcourir_chart_type == 'FindElem':
                col_name1 = request.POST.get('col_name1')
                row_numb = request.POST.get('RowNumb')
                if col_name1 and row_numb:
                    row_numb = int(row_numb)
                    if row_numb < 0 or row_numb >= len(df):
                        raise IndexError("Ligne hors des limites du DataFrame.")
                    resultats_recherche = df.at[row_numb, col_name1]
                    context = {
                        'resultat': resultats_recherche,
                        'cols': columns_choices,
                        'df': df.to_html(classes='table table-bordered'),
                        'max_row': len(df) - 1
                    }
                    return render(request, 'visualisation/dataFrameTable.html', context)
            
            # Code existant pour le slicing
            parcourir_rows_type = request.POST.get('parcourir_rows')
            if parcourir_rows_type == 'NbrOfRowsTop':
                nb_rows_top = int(request.POST.get('Head', 5))
                df = df.head(nb_rows_top)
            elif parcourir_rows_type == 'NbrOfRowsBottom':
                nb_rows_bottom = int(request.POST.get('Tail', 5))
                df = df.tail(nb_rows_bottom)
            elif parcourir_rows_type == 'FromRowToRow':
                from_row = int(request.POST.get('FromRowNumb', 0))
                to_row = int(request.POST.get('ToRowNumb', len(df) - 1))
                df = df.iloc[from_row:to_row + 1]
            
            selected_columns = request.POST.getlist('selected_columns')
            if selected_columns:
                df = df[selected_columns]
                
        except Exception as e:
            return HttpResponse(f"Erreur : {str(e)}")
        
        context = {
            'df': df.to_html(classes='table table-bordered'),
            'cols': columns_choices,
            'max_row': len(df) - 1
        }
        return render(request, 'visualisation/dataFrameTable.html', context)
    
    context = {
        'df': df.to_html(classes='table table-bordered'),
        'cols': columns_choices,
        'max_row': len(df) - 1
    }
    return render(request, 'visualisation/dataFrameTable.html', context)

def laws(request):
    return render(request,"visualisation/laws.html")


def Binomiale(request):
    if request.method == 'POST':
        form = BinomialForm(request.POST)
        if form.is_valid():
            n = form.cleaned_data['n']
            p = form.cleaned_data['p']

            # Générer des échantillons de la distribution binomiale
            data_binomial = binom.rvs(n=n, p=p, loc=0, size=1000)

            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_binomial, nbins=n+1, title='Distribution Binomiale')
            fig.update_layout(xaxis_title='Binomial', yaxis_title='Fréquence relative',bargap=0.2)

            # Convertir la figure en JSON
            plot_data = fig.to_html()

            return render(request, 'visualisation/binomiale.html', {'form': form, 'plot_data': plot_data})
    else:
        form = BinomialForm()

    return render(request, 'visualisation/binomiale.html', {'form': form})



def Bernoulli(request):
    if request.method == 'POST':
        form = BernoulliForm(request.POST)
        if form.is_valid():
            p = form.cleaned_data['p']
            # Générer des échantillons de la distribution de Bernoulli
            data_bernoulli = bernoulli.rvs(p, size=1000)
            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_bernoulli, nbins=2, title='Distribution de Bernoulli')
            fig.update_layout(xaxis_title='Bernoulli', yaxis_title='Fréquence relative',bargap=0.2)
            # Convertir la figure en JSON
            plot_data = fig.to_html()

            return render(request, 'visualisation/bernoulli.html', {'form': form, 'plot_data': plot_data})
    else:
        form = BernoulliForm()

    return render(request, 'visualisation/bernoulli.html', {'form': form})

#///////////////////////////


def Normale(request):
    if request.method == 'POST':
        form = NormaleForm(request.POST)
        if form.is_valid():
            mean = form.cleaned_data['mean']
            std_dev = form.cleaned_data['std_dev']

            # Générer des échantillons de la distribution normale
            data_normale = np.random.normal(mean, std_dev, size=1000)

            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_normale, title='Distribution Normale Continue')
            fig.update_layout(xaxis_title='Valeur', yaxis_title='Fréquence relative',bargap=0.2)

            # Convertir la figure en JSON
            plot_data = fig.to_html()

            return render(request, 'visualisation/normale.html', {'form': form, 'plot_data': plot_data})
    else:
        form = NormaleForm()

    return render(request, 'visualisation/normale.html', {'form': form})



def Poisson(request):
    if request.method == 'POST':
        form = PoissonForm(request.POST)
        if form.is_valid():
            lambda_param = form.cleaned_data['lambda_param']

            # Générer des échantillons de la distribution de Poisson
            data_poisson = np.random.poisson(lambda_param, size=1000)

            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_poisson, title='Distribution de Poisson')
            fig.update_layout(xaxis_title='Valeur', yaxis_title='Fréquence relative',bargap=0.2)

            # Convertir la figure en JSON
            plot_data = fig.to_html()

            return render(request, 'visualisation/poisson.html', {'form': form, 'plot_data': plot_data})
    else:
        form = PoissonForm()

    return render(request, 'visualisation/poisson.html', {'form': form})



def Uniforme(request):
    if request.method == 'POST':
        form = UniformeForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']

            # Générer des échantillons de la distribution uniforme
            data_uniforme = np.random.uniform(a, b, size=1000)

            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_uniforme, title='Distribution Uniforme')
            fig.update_layout(xaxis_title='Valeur', yaxis_title='Fréquence relative',bargap=0.2)

            # Convertir la figure en JSON
            plot_data = fig.to_html()

            return render(request, 'visualisation/uniforme.html', {'form': form, 'plot_data': plot_data})
    else:
        form = UniformeForm()

    return render(request, 'visualisation/uniforme.html', {'form': form})



def Exponentielle(request):
    if request.method == 'POST':
        form = ExponentielleForm(request.POST)
        if form.is_valid():
            beta = form.cleaned_data['beta']

            # Générer des échantillons de la distribution exponentielle
            data_exponentielle = np.random.exponential(scale=beta, size=1000)

            # Créer un histogramme interactif avec Plotly Express
            fig = px.histogram(x=data_exponentielle, title='Distribution Exponentielle')
            fig.update_layout(xaxis_title='Valeur', yaxis_title='Fréquence relative',bargap=0.2)

            # Convertir la figure en JSON
            plot_data = fig.to_html()

            return render(request, 'visualisation/exponentielle.html', {'form': form, 'plot_data': plot_data})
    else:
        form = ExponentielleForm()

    return render(request, 'visualisation/exponentielle.html', {'form': form})

