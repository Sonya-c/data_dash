
from dash import Dash, html, dcc
import plotly.express as px
import plotly.io as pio

import db
import components

casos_fecha, casos_edad, casos_sexo, _ = db.queries()

fig_casos_fecha = components.casos_fecha(casos_fecha)
fig_casos_edad = components.casos_edad(casos_edad)
fig_casos_sexo = components.casos_sexo(casos_sexo)

pio.templates.default = "plotly_white"

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
        components.header(),

        html.Main(
            className="m-3 ",
            children=[

                components.graph("Número de casos por fecha de notificación",
                                "fecha-numero-casos",
                                fig_casos_fecha),

                html.Section([
                    html.Div(
                        className="grid md:grid-cols-2 gap-4",
                        children=[
                            components.graph("Número de casos por Edad",
                                            "edad-numero-casos",
                                            fig_casos_edad),
                            components.graph("Número de casos por Sexo",
                                            "sexo-numero-caso",
                                            fig_casos_sexo)
                            ])
                    ])
                ])
        ]
    )

if __name__ == '__main__':
    app.run_server(debug=True)
