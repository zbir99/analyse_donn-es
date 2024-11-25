from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import io
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

def dataframe(request):
    return render(request,"visualisation/dataFrameTable.html")

def dataframe_upload(request):
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            return HttpResponse("Aucun fichier téléchargé. Veuillez télécharger un fichier CSV ou Excel.")
        
        csv_file = request.FILES['csv_file']
        file_type = csv_file.name.split('.')[-1].lower()  # Extension du fichier

        try:
            if file_type == 'csv':
                df = pd.read_csv(csv_file)
            elif file_type in ['xls', 'xlsx']:
                # Conversion Excel en DataFrame
                df = pd.read_excel(csv_file)
            else:
                return HttpResponse("Type de fichier non pris en charge. Veuillez télécharger un fichier CSV ou Excel.")

            # Sérialisation du DataFrame en CSV et stockage dans la session
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            request.session['df'] = csv_buffer.getvalue()  # Sauvegarde sous forme de chaîne
            request.session['cols'] = list(df.columns)  # Sauvegarde des colonnes

            # Convertir en HTML pour affichage
            df_html = df.to_html(classes='table')
            context = {'df': df_html, 'cols': list(df.columns)}
            return render(request, 'visualisation/dataFrameTable.html', context)

        except Exception as e:
            return HttpResponse(f"Erreur lors du traitement du fichier : {str(e)}")
    
    # Si la méthode n'est pas POST, renvoyer la page vide
    return render(request, "visualisation/dataFrameTable.html")

def dataframe_search1(request):
    df_csv = request.session.get('df')  # Récupérer le DataFrame sérialisé depuis la session
    if not df_csv:
        return HttpResponse("Aucun DataFrame chargé. Veuillez d'abord télécharger un fichier.")

    # Charger le DataFrame à partir de la chaîne CSV
    df = pd.read_csv(io.StringIO(df_csv))
    columns_choices = request.session.get('cols', [])

    if request.method == 'POST':
        parcourir_chart_type = request.POST.get('parcourir_chart')
        col_name1 = request.POST.get('col_name1')
        row_numb = request.POST.get('RowNumb')

        try:
            if parcourir_chart_type == 'FindElem' and col_name1 and row_numb:
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

            # Gérer les autres options de parcours
            parcourir_rows_type = request.POST.get('parcourir_rows')

            if parcourir_rows_type == 'NbrOfRowsTop':
                nb_rows_top = int(request.POST.get('Head', 5))  # Par défaut, prendre 5 lignes
                df = df.head(nb_rows_top)
            elif parcourir_rows_type == 'NbrOfRowsBottom':
                nb_rows_bottom = int(request.POST.get('Tail', 5))  # Par défaut, prendre 5 lignes
                df = df.tail(nb_rows_bottom)
            elif parcourir_rows_type == 'FromRowToRow':
                from_row = int(request.POST.get('FromRowNumb', 0))
                to_row = int(request.POST.get('ToRowNumb', len(df) - 1))
                df = df.iloc[from_row:to_row + 1]

            # Filtrer les colonnes sélectionnées
            selected_columns = request.POST.getlist('selected_columns')
            if selected_columns:
                df = df[selected_columns]

        except Exception as e:
            return HttpResponse(f"Erreur : {str(e)}")

    context = {
        'df': df.to_html(classes='table table-bordered'),
        'cols': columns_choices
    }
    return render(request, 'visualisation/dataFrameTable.html', context)

def dataframe_search(request):
    df = request.session.get('df')
    df = pd.read_csv(io.StringIO(df))
    df_html = df.to_html(classes='table')

    if request.method == 'get':
        methode = request.get['methode']
        line1 = request.get['line1']
        line2 = request.get['line2']

        if methode == "Slicing":

            if line1 and line2:
                sliced_df = df.loc[line1 : line2]
            elif line1:
                sliced_df = df.loc[line1:]
            elif line2:
                sliced_df = df.loc[:line2]
            else:
                # Aucun choix, afficher le DataFrame entier
                sliced_df = df

            df_html = sliced_df.to_html(classes='table table-striped', index=False)

            context={
            'df': df_html,
            }
            return render(request,"visualisation/dataFrameTable.html", context)
    context={
        'df': df_html,
        }
    return render(request,"visualisation/dataFrameTable.html", context)

