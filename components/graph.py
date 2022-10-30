from dash import Dash, html, dcc
import plotly.express as px

def graph(title, id, figure):
    return html.Div(
        className="p-3 mb-5 bg-white border-indigo-100 rounded",
            
        children=[html.H2(title,
                className="text-xl font-semibold pb-3 pt-3"),
                dcc.Graph(id=id, figure=figure)
            ]
        )

def casos_fecha(df):
    return px.scatter(df,
        x="fecha",
        y="numero_casos",
        size='numero_casos',
        labels={
            "fecha": "Fecha de reporte",
            "numero_casos": "Número de reportes"
        }
    )

def casos_edad(df):
    return px.scatter(df,
        x="edad",
        y="numero_casos",
        size='numero_casos',
        labels={
            "numero_casos": "Número de reportes"
        }
    )

def casos_sexo(df):
    return px.bar(df,
        x="sexo",
        y="numero_casos",
        width=100,
        color="sexo",
        labels={
            "numero_casos": "Número de reportes"
        }
    )

def casos_estado(df):
    return px.scatter(df,
        x="estado",
        y="numero_casos",
        width=100,
        labels={
            "numero_casos": "Número de reportes"
        }
    )
