from dash import Dash, html, dcc
from sodapy import Socrata
import plotly.express as px
import plotly.io as pio
import pandas as pd

pio.templates.default = "plotly_white"

tailwind_cdn = ["https://tailwindcss.com/",
                {"src": "https://cdn.tailwindcss.com"}]
app = Dash(__name__, external_scripts=tailwind_cdn)
app.scripts.config.serve_locally = True

data = Socrata("www.datos.gov.co", None).get("gt2j-8ykr", limit=2000)
df = pd.DataFrame.from_records(data)

df_fecha_count = df.groupby(["fecha_de_notificaci_n", "sexo"]
                            ).size().reset_index(name='numero_reportes')
fig_fecha_count = px.scatter(df_fecha_count,
                             x="fecha_de_notificaci_n",
                             y="numero_reportes",
                             size='numero_reportes',
                             color="sexo",
                             labels={
                                 "fecha_de_notificaci_n": "Fecha de notificación",
                                 "numero_reportes": "Número de reportes"
                             })

df_edad_count = df.groupby(["edad", "sexo"]).size(
).reset_index(name='numero_reportes')
fig_edad_count = px.scatter(df_edad_count,
                            x="edad",
                            y="numero_reportes",
                            size='numero_reportes',
                            color="sexo",
                            labels={
                                "fecha_de_notificaci_n": "Fecha de notificación",
                                "numero_reportes": "Número de reportes"
                            })

h2_style = "text-xl font-semibold pb-3 pt-3"

app.layout = html.Div(
    className="min-h-screen font-sans bg-gradient-to-r from-sky-500 to-indigo-500",
    children=[
        html.Div(
            className="bg-white shadow-lg pt-3 bg-clip-padding bg-opacity-80 backdrop-blur-[20px]",
            # style={backdrop-filter: blur(20px)},
            children=[
                html.Header(
                    className="m-3 rounded p-10 bg-gradient-to-r from-sky-500 to-indigo-500 shadow-lg pt-3 bg-clip-padding bg-opacity-20 backdrop-blur-[20px]",
                    children=[
                        html.H1("Casos positivos de COVID-19 en Colombia",
                                className="text-2xl font-semibold pt-3 pb-3"),
                        html.Div("Inserte descripción aquí")
                    ]
                ),
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
                                    html.H2("Número de casos por fecha",
                                            className=h2_style),
                                    dcc.Graph(
                                        id='fecha-numero-casos',
                                        figure=fig_fecha_count,
                                        className="rounded"
                                    )
                                ]
                                ),
                                html.Section([
                                    html.Div(
                                        className="grid grid-cols-2 gap-4",
                                        children=[
                                            html.Div([
                                                html.H2("Casos por edad y sexo",
                                                        className=h2_style),
                                                dcc.Graph(
                                                    id='edad-numero-casos',
                                                    figure=fig_edad_count
                                                )
                                            ]),
                                            html.Div([
                                                html.H2(
                                                    "Analisis de Datos", className=h2_style)
                                            ])
                                        ])
                                ])
                            ])
                    ]
                )
            ]
        )
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
