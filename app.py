from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc
import os
import plotly.express as px
import pandas as pd
from snapmlengine.ml.linear_regression import *

app = Dash(__name__)
ans = linear_regression_analysis('data.xlsx', ['AT', 'V', 'AP', 'RH'], ['PE'])
data = create_graphs(ans)

def create_graph(x,y):
    fig = create_graph_for_report(x,y)
    return dcc.Graph(
            figure = fig
        )

def create_graph_for_report(x,y):
    df = pd.DataFrame({'x':x, 'y':y})
    return px.scatter(df, x = "x", y = "y")

app.layout = html.Div(
    children = [
        html.H1(children = "Snap ML Engine",),
        html.H2(children = "By Top G Anish",),
        html.P(children = "Analysis",),

        dbc.Row([create_graph(x[-2], x[-1]) for x in data]),

        html.Button("Download Report", id="btn-download-report"),
        dcc.Download(id = "download-report"),
    ]
)

@app.callback(
    Output("download-report", "data"),
    Input("btn-download-report", "n_clicks"),
    prevent_initial_call = True,
)
def generate_report(n_clicks):
    current_directory = os.getcwd()
    os.mkdir(os.path.join(current_directory, 'temp'))

    figures = [create_graph_for_report(x[-2], x[-1]) for x in data]
    print(figures)

    for i,fig in enumerate(figures):
        fig.write_image("temp/graph{}.png".format(i))


if __name__ == "__main__":
    app.run_server(port = 8051)
