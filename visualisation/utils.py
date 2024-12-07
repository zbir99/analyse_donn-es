import matplotlib.pyplot as plt
import plotly.express as px
import base64
from io import BytesIO
import seaborn as sns
import plotly.graph_objects as go



def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph




def get_heatmap(df):
    df=df.select_dtypes(include=['number'])
    fig = px.imshow(df.corr(), x=df.columns, y=df.columns, title='Interactive Heatmap')
    html_string = fig.to_html(full_html=False)
    return html_string

def get_violinplot(df, y_column):
    fig = px.violin(df, y=y_column, title=f'Violin Plot for {y_column}')

    # Save the plot as an HTML string
    html_string = fig.to_html(full_html=False)
    
    return html_string

def get_kdeplot(df, column_name):
    fig = px.density_contour(df, x=column_name, title='Interactive KDE Plot')
    
    # Save the plot as an HTML string
    html_string = fig.to_html(full_html=False)
    
    return html_string


def get_histogram(df, column_name):
    fig = px.histogram(df, x=column_name, title='Interactive Histogram')
    
    html_string = fig.to_html(full_html=False)
    
    return html_string

# def get_boxplot(df, column_name):
#     plt.figure(figsize=(10, 6))
#     sns.boxplot(x=column_name, data=df)
#     plt.title('Boxplot')
#     plt.xlabel(column_name)
#     plt.ylabel('Values')

#     # Sauvegarder le graphique dans un buffer
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
    
#     # Convertir l'image en format base64
#     image_png = base64.b64encode(buffer.read()).decode('utf-8')
    
#     # Fermer le buffer
#     buffer.close()
    
#     return image_png

def get_boxplot(df, column_name):
    fig = px.box(df, x=column_name, title='Boxplot', labels={column_name: 'Values'})
    
    # Convertir la figure en format HTML interactif
    graph = fig.to_html(full_html=False)
    
    return graph


def get_piechart(df, column_name):
    value_counts = df[column_name].value_counts()
    labels = value_counts.index.tolist()
    values = value_counts.values.tolist()
    fig = px.pie(names=labels, values=values, title='Pie Chart')
    graph = fig.to_html(full_html=False)
    return graph


def get_interactive_lineplot(df, a, b):
    fig = px.line(df, x=a, y=b, markers=True)
    fig.update_layout(
        title='Interactive Line Plot',
        xaxis_title=a,
        yaxis_title=b,
        xaxis=dict(tickangle=45),
    )
    
    
    graph = fig.to_html(full_html=False)
    return graph

def get_interactive_barplot(df, a, b):
    fig = px.bar(df, x=a, y=b)
    fig.update_layout(
        title='Interactive Bar Plot',
        xaxis_title=a,
        yaxis_title=b
    )
    
    graph = fig.to_html(full_html=False)
    return graph

def get_interactive_scatterplot(df, x, y, color=None, size=None):
    fig = px.scatter(df, x=x, y=y, color=color, size=size)
    fig.update_layout(
        title='Interactive Scatter Plot',
        xaxis_title=x,
        yaxis_title=y
    )
    
    graph = fig.to_html(full_html=False)
    return graph

###############################################

def get_lineplot(df,a,b):
    sns.set()
    plt.switch_backend('AGG')
    plt.figure(figsize=(7,5))
    plt.title('test')
    sns.lineplot(x= a, y= b, data=df, marker='o',
    color='b')
    plt.xticks(rotation=45)
    plt.xlabel(a)
    plt.ylabel(b)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_barplot(x, y, data):
    sns.set()
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('test')
    sns.barplot(x=x , y=y, data=data)
    plt.xticks(rotation=45)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_scatterplot(x,y,data):
    sns.set()
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('test')
    sns.scatterplot(x=x, y=y, data=data)
    plt.xticks(rotation=45)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.tight_layout()
    graph = get_graph()
    return graph

