
from dash import Dash, html, dcc
import plotly.express as px
import plotly.io as pio
from sodapy import Socrata
import pandas as pd

# GET THE DATA
client = Socrata("www.datos.gov.co", None)
data = client.get("gt2j-8ykr", limit=5000)
df = pd.DataFrame.from_records(data)

# Parse
df.edad = df.edad.astype(int)

# Obtener número de casos por fecha
df_casos_fecha = df.groupby(["fecha_de_notificaci_n"]).size(
).reset_index(name='numero_reportes')

# Número de casos por edad
df_casos_edad = df.groupby(["edad"]).size().reset_index(name='numero_reportes')

# Número de casos por sexo
df_casos_sexo = df.groupby(["sexo"]).size().reset_index(name='numero_reportes')

fig_casos_fecha = px.scatter(
    df_casos_fecha,
    x="fecha_de_notificaci_n",
    y="numero_reportes",
    size='numero_reportes',
    labels={
        "fecha_de_notificaci_n": "Fecha de notificación",
        "numero_reportes": "Número de reportes"
    }
)

fig_casos_edad = px.scatter(
    df_casos_edad,
    x="edad",
    y="numero_reportes",
    size='numero_reportes',
    labels={
        "numero_reportes": "Número de reportes"
    }
)

fig_casos_sexo = px.bar(
    df_casos_sexo,
    x="sexo",
    y="numero_reportes",
    width=100,
    color="sexo",
    labels={
        "numero_reportes": "Número de reportes"
    }
)
# CONFIGURATION
pio.templates.default = "plotly_white"

# añadir wailwind
tailwind_cdn = ["https://tailwindcss.com/",
                {"src": "https://cdn.tailwindcss.com"}]

app = Dash(__name__, external_scripts=tailwind_cdn, meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
])

server = app.server
app.scripts.config.serve_locally = True

# FRONT END
app.layout = html.Div(
    className="min-h-screen font-sans bg-indigo-50 pt-5 pb-5 ",

    children=[
        html.Header(
            className="m-3 rounded p-10 bg-gradient-to-r from-indigo-500 to-sky-500 bg-clip-padding bg-opacity-20 backdrop-blur-[20px] shadow-lg text-slate-50",
            children=[
                html.H1(
                    "Casos positivos de COVID-19 en Colombia",
                    className="text-2xl font-semibold pt-3 pb-3"),
                html.A(
                    "Ver base de datos",
                    href="https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-positivos-de-COVID-19-en-Colombia/gt2j-8ykr",
                    target="black"
                )
            ]
        ),


        html.Main(
            className="m-3 ",
            children=[

                html.Section(
                    className="p-3 mb-5 bg-white border-indigo-100 rounded",
                    children=[
                        html.H2("Número de casos por fecha de notificación",
                                className="text-xl font-semibold pb-3 pt-3"),
                        dcc.Graph(
                            id="fecha-numero-casos",
                            figure=fig_casos_fecha
                        )
                    ]
                ),

                html.Section([
                    html.Div(
                        className="grid md:grid-cols-2 gap-4",
                        children=[
                            html.Div(
                                className="p-3 mb-3 bg-white border-indigo-100 rounded",
                                children=[
                                    html.H2("Número de casos por Edad",
                                            className="text-xl font-semibold pb-3 pt-3"),
                                    dcc.Graph(
                                        id="fehca-numero-casos",
                                        figure=fig_casos_edad
                                    )
                                ]
                            ),
                            html.Div(
                                className="p-3 mb-3 bg-white border-indigo-100 rounded",
                                children=[
                                    html.H2("Número de casos por Sexo",
                                            className="text-xl font-semibold pb-3 pt-3"),
                                    dcc.Graph(
                                        id="fehca-numero-sexo",
                                        figure=fig_casos_sexo
                                    )
                                ]
                            ),
                        ])
                ])
            ])
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
