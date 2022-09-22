"""_summary_
"""

# ---------------------------------------------------------------------------------------------------
# IMPORTAR LIBRERIAS
# Son modulos creados para realizar una tarea en especifico y facilitar el desarrollo
# Para poder utilizarlas primero hay que instalarlas en la maquina (se puede usar la herramienta pip)
# Luego de instalar, se deberan importar para para usarlas en nuestro proyecto.
# Para el diseño del dashboard, usaremos las siguientes librerias

# Diseño de las interfaces y la creación de los graficos
from dash import Dash, html, dcc
import plotly.express as px
import plotly.io as pio

# Obtener los datos desde la base de datos remote
from sodapy import Socrata

# Manipulación de los datos
import pandas as pd

# ---------------------------------------------------------------------------------------------------
# OBTENER LOS DATOS
# Los datos se encuentran en una base de datos remota en www.datos.gov.co
# Para poder obtenerlos usaremos la libreria sodapy (en especial, la función socrata)

# Primero, con socrata, crearemos un cliente que se conecte a la fuente de datos (el servidor)
# La función Socrata(fuente, datos de acceso) pide la fuente de los datos
# (en nuestro caso www.datos.gov.co) y los datos de acceso
# Hay fuentes que requieren claves especiales para tener acceso
# Como nuestra fuente de datos es libre, no sera necesario (se especifica None)
client = Socrata("www.datos.gov.co", None)

# Luego, de ese clienete se obtienen los datos con el identificador de la base de datos
# El identificador de la base que nos interesa es gt2j-8ykr
# Tambien, se puede especificar el limite de datos
data = client.get("gt2j-8ykr")
df = pd.DataFrame.from_records(data)

# SELECT THE INFORMATION

# numero de reportes vs fecha de notificación

df_fecha_count = df.groupby(["fecha_de_notificaci_n", "sexo"])\
    .size()\
    .reset_index(name='numero_reportes')

fig_fecha_count = px.scatter(df_fecha_count,
                             x="fecha_de_notificaci_n",
                             y="numero_reportes",
                             size='numero_reportes',
                             color="sexo",
                             labels={
                                 "fecha_de_notificaci_n": "Fecha de notificación",
                                 "numero_reportes": "Número de reportes"
                             }
                             )

# numero de reportes vs edad
df_edad_count = df.groupby(["edad", "sexo"])\
    .size()\
    .reset_index(name='numero_reportes')

fig_edad_count = px.scatter(
    df_edad_count,
    x="edad",
    y="numero_reportes",
    size='numero_reportes',
    color="sexo",
    labels={
        "fecha_de_notificaci_n": "Fecha de notificación",
        "numero_reportes": "Número de reportes"
    }
)

# GLOBAL STYLES

h2_style = "text-xl font-semibold pb-3 pt-3"

# COMPONENTS


def graph_section(figure, figure_id, title="", className=""):
    return html.Div(
        className=className,
        children=[
            html.H2(title, className=h2_style),
            dcc.Graph(
                id=figure_id,
                figure=figure,
                className="rounded"
            )
        ]
    )


header = html.Header(
    className="m-3 rounded p-10 bg-gradient-to-r from-sky-500 to-indigo-500 shadow-lg pt-3 bg-clip-padding bg-opacity-20 backdrop-blur-[20px]",

    children=[
        html.H1(
            "Casos positivos de COVID-19 en Colombia",
            className="text-2xl font-semibold pt-3 pb-3"
        ),
        html.Div("Inserte descripción aquí")
    ]
)

# PAGE LAYOUT
pio.templates.default = "plotly_white"

tailwind_cdn = ["https://tailwindcss.com/",
                {"src": "https://cdn.tailwindcss.com"}]
app = Dash(__name__, external_scripts=tailwind_cdn)
app.scripts.config.serve_locally = True

app.layout = html.Div(
    className="""min-h-screen font-sans bg-gradient-to-r
				from-sky-500 to-indigo-500""",

    children=[
        html.Div(
            className="""bg-white shadow-lg pt-3 bg-clip-padding
						bg-opacity-80 backdrop-blur-[20px]""",

            children=[
                header,

                html.Div(
                    className="grid grid-cols-3 gap-4 ml-3 mr-3 pb-3",
                    children=[

                        html.Aside([
                            html.H2("Infromación de los Datos",
                                    className=h2_style)
                        ]),

                        html.Main(
                            className="col-span-2",
                            children=[

                                html.Section([
                                    graph_section(
                                        fig_fecha_count,
                                        "fecha-numero-casos",
                                        "Casos por fecha")
                                ]),

                                html.Section([
                                    html.Div(
                                        className="grid grid-cols-2 gap-4",
                                        children=[
                                            graph_section(
                                                fig_edad_count,
                                                "edad-numero-casos",
                                                "Casos por edad y sexo"),

                                            html.Div([
                                                html.H2(
                                                    "Analisis de Datos", className=h2_style)
                                            ])
                                        ])
                                ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
