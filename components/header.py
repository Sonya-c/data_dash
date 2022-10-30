from dash import Dash, html, dcc

def header():
    return html.Header(
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
    )