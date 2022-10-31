import db
import plotly.express as px
import plotly.io as pio
from dash import Dash, html, dcc, Input, Output

pio.templates.default = "plotly_white"

tailwind_cdn = ["https://tailwindcss.com/",
                {"src": "https://cdn.tailwindcss.com"}]

app = Dash(__name__, external_scripts=tailwind_cdn, meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
])

server = app.server
app.scripts.config.serve_locally = True

casos_fecha, casos_edad, casos_sexo, casos_estado = db.queries()

fig_casos_sexo = px.bar(casos_sexo,
    x="sexo",
    y="numero_casos",
    color='sexo',
    labels={
        "numero_casos": "Número de reportes"
    }
)

fig_casos_estado = px.bar(casos_estado,
    x="estado",
    y="numero_casos",
    labels={
        "numero_casos": "Número de reportes"
    }
)

fig_casos_edad = px.scatter(casos_edad,
    x="edad",
    y="numero_casos",
    size='numero_casos',
    labels={
        "numero_casos": "Número de reportes"
    }
)
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

                html.Div(
                    className="p-3 mb-5 bg-white border-indigo-100 rounded",
                        
                    children=[
                        html.H2(
                            "Casos por fecha",
                            className="text-xl font-semibold pb-3 pt-3"
                        ),
                        dcc.Dropdown(
                            casos_fecha["municipio"].unique(),
                            None,
                            id="dropdown-municipio"
                        ),
                        dcc.RadioItems(
                            ['Fallecido', 'Otro', 'Ambos'],
                            'Ambos',
                            id='radio-estado',
                            inline=True
                        ),
                        dcc.RadioItems(
                            ['F', 'M', 'Ambos'],
                            'Ambos',
                            id='radio-sexo',
                            inline=True
                        ),
                        dcc.Graph(
                            id="fecha-casos"
                        )]
                    ),
                

                html.Section([
                    html.Div(
                        className="grid md:grid-cols-2 gap-4", 
                        children=[
                            html.Div(
                                className="p-3 mb-5 bg-white border-indigo-100 rounded",
                                
                                children=[
                                    html.H2(
                                        "Casos por sexo",
                                        className="text-xl font-semibold pb-3 pt-3"
                                    ),
                                    dcc.Graph(
                                        id="caso-sexo",
                                        figure=fig_casos_sexo
                                    )
                                ]
                            ), 
                            html.Div(
                                className="p-3 mb-5 bg-white border-indigo-100 rounded",
                                
                                children=[
                                    html.H2(
                                        "Casos por estado",
                                        className="text-xl font-semibold pb-3 pt-3"
                                    ),
                                    dcc.Graph(
                                        id="caso-estado",
                                        figure=fig_casos_estado
                                    )
                                ]
                            )
                        ])
                    ]),

                html.Div(
                    className="p-3 mb-5 bg-white border-indigo-100 rounded",
                        
                    children=[
                        html.H2(
                            "Casos por edad",
                            className="text-xl font-semibold pb-3 pt-3"
                        ),
                        dcc.Graph(
                            id="casos-edad",
                            figure=fig_casos_edad
                        )]
                    ) 
            ])
        ]
    )

@app.callback(
    Output('fecha-casos', 'figure'),
    Input('radio-estado', 'value'),
    Input('dropdown-municipio', 'value'),
    Input('radio-sexo', 'value')
)
def update(estado, municipio, sexo):
    filter_df = casos_fecha

    if (municipio != None):
        filter_df = filter_df[filter_df.municipio == municipio]
    
    if (estado != None or estado != "Ambos"):
        if (estado == "Fallecido"):
            filter_df = filter_df[filter_df.estado == "Fallecido"]
        else: 
            filter_df = filter_df[filter_df.estado != "Fallecido"]
            
    if (sexo != None or sexo != "Ambos"):
        if (sexo == "F"):
            filter_df = filter_df[filter_df.sexo == "F"]
        else:
            filter_df = filter_df[filter_df.sexo == "M"]

    filter_df = filter_df.groupby("fecha")["numero_casos"].sum().reset_index()
    
    fig_casos_fecha = px.scatter(filter_df,
        x="fecha",
        y="numero_casos",
        size='numero_casos',
        labels={
            "fecha": "Fecha de reporte",
            "numero_casos": "Número de reportes"
        }
    )

    return fig_casos_fecha

if __name__ == '__main__':
    app.run_server(debug=True)
