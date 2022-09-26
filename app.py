
# ---------------------------------------------------------------------------------------------------
# IMPORTAR LIBRERIAS
# Son modulos creados para realizar una tarea en especifico y facilitar el desarrollo
# Para poder utilizarlas primero hay que instalarlas en la maquina (se puede usar la herramienta pip)
# Luego de instalar, se deberan importar para para usarlas en nuestro proyecto.
# Para el diseño del dashboard, usaremos las siguientes librerias

from dash import Dash, html, dcc
import plotly.express as px
import plotly.io as pio
from sodapy import Socrata
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

# Los data frame so una estructura de datos de pandas que formadas por filas y columnas (como una tabla)
# Podemos crear un data frame desde los datos optendios usando la función "from records"
df = pd.DataFrame.from_records(data)

# ---------------------------------------------------------------------------------------------------
# SELECCIONAR LOS DATOS
# Hay muchos datos en el datframe que encontramos, por ello, debemos seleccionar los datos con los que vamos a trabajar
# En este caso, obtendremos el número de reportes por fecha y el número de reportes por edad

# Como a cada reporte corresponde a una fila del dataframe
# Queremos crear, con base a los datos obtenidos, un nuevo data frame con dos columnas
# Fecha de notificiación    | Número de reportes
# Para hacer ello, primero es neesario agrupar los datos por fecha (usamos el comadno groupby)

df_group_fecha = df.groupby(["fecha_de_notificaci_n"])

# Luego, con el comando size() se puede contar el número de elementos por cada grupo (esto crear una nueva columa)
# La nueva columna creada NO tienen un nombre, asi que podemos asiganarselo con reset_index

df_casos_fecha = df_group_fecha.size().reset_index(name='numero_reportes')

# Lo mismo podemos hacer para obtener el número de reportes por edad

df_group_edad = df.groupby(["edad"])
df_casos_edad = df_group_edad.size().reset_index(name='numero_reportes')

# ---------------------------------------------------------------------------------------------------
# GRAFICAR

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
        "fecha_de_notificaci_n": "Fecha de notificación",
        "numero_reportes": "Número de reportes"
    }
)

# Cambiar el color de las graficas
pio.templates.default = "plotly_white"

tailwind_cdn = ["https://tailwindcss.com/",
                {"src": "https://cdn.tailwindcss.com"}]
app = Dash(__name__, external_scripts=tailwind_cdn)
app.scripts.config.serve_locally = True

app.layout = html.Div(

    className="min-h-screen " +  # La antura minima sea el tamaño de la pantalla
              "font-sans " +  # Cambiar el tipo de fuente
              "bg-indigo-50 " +  # Cambiar el dondo de pantalla
              # poadding (espacio) superiro. Esto se hace para evitar un espaico en blanco
              "pt-5 pb-5 ",

    children=[  # Los hijos son los componentes que estan dentro de este

        html.Header(
            # El encabezado (header) presenta infirmación sob re la pagina (titulo, descripción, alguna imagen, ect)

            className="m-3 " +  # Margen de 3
                      "rounded " +  # Puntas redondeadas
                      "p-10 " +  # Padding de 10
                      # Colo de fondo
                      "bg-gradient-to-r from-indigo-500 to-sky-500 bg-clip-padding bg-opacity-20 backdrop-blur-[20px] " +
                      "shadow-lg "  # Sombra
                      "text-slate-50",  # Cambiar el color de texto

            children=[

                html.H1("Casos positivos de COVID-19 en Colombia",
                        className="text-2xl " +  # Cambiar el tamaño del texto
                                  "font-semibold " +  # Cambiar el grosos de la fuente
                                  "pt-3 pb-3"  # Añadir un padding superior y un padding inferior
                        ),
                html.P("Inserte descripción aquí")
            ]
        ),


        html.Main(
            className="m-3 ",  # Añadir un margen de 5
            children=[

                html.Section(
                    className="p-3 mb-5 bg-white border-indigo-100 rounded",
                    children=[
                        html.H2("Número de casos por edad",
                                className="text-xl font-semibold pb-3 pt-3"),
                        dcc.Graph(
                            id="fecha-numreo-casos",
                            figure=fig_casos_fecha
                        )
                    ]
                ),

                html.Section([
                    html.Div(
                        className="grid grid-cols-2 gap-4",
                        children=[
                            html.Div(
                                className="p-3 mb-3 bg-white border-indigo-100 rounded",
                                children=[
                                    html.H2("Número de casos por Edad",
                                            className="text-xl font-semibold pb-3 pt-3"),
                                    dcc.Graph(
                                        id="fehca-numreo-casos",
                                        figure=fig_casos_edad
                                    )
                                ]
                            ),

                            html.Div([
                                html.H2(
                                    "Analisis de Datos", className="text-xl font-semibold pb-3 pt-3"
                                ),
                                html.Table([
                                    html.Tr([
                                        html.Td("Media de casos por día")
                                    ]),
                                    html.Tr([
                                        html.Td("Varianza de casos por día")
                                    ]),
                                    html.Tr([
                                        html.Td("Edad media")
                                    ]),
                                    html.Tr([
                                        html.Td("Varianza edad")
                                    ])
                                ])
                            ])
                        ])
                ])
            ])
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
