from dash import Dash, html, dcc
import pandas as pd
from sodapy import Socrata

client = Socrata("www.datos.gov.co", None)
results = client.get("gt2j-8ykr", limit=2000)
results_df = pd.DataFrame.from_records(results)
print(results_df)

app = Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1("Hello World")
])

if __name__ == '__main__':
    app.run_server(debug=True)
