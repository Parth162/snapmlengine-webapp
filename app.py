from distutils.log import debug
from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc
import os
import plotly.express as px
import pandas as pd
from snapmlengine.ml.linear_regression import *

app = Dash(__name__)
ans = linear_regression_analysis('data.xlsx', ['AT', 'V', 'AP', 'RH'], ['PE'])
data = create_graphs(ans)

def create_graph(title, x_title, y_title, x_data, y_data):
    fig = create_graph_for_report(title, x_title, y_title, x_data, y_data)
    return dcc.Graph(
            figure = fig
        )

def create_graph_for_report(title, x_title, y_title, x_data, y_data):
    df = pd.DataFrame({x_title:x_data, y_title:y_data})
    return px.scatter(df, x = x_title, y = y_title, title=title)

app.layout = html.Div(
    children = [
        html.H1(children = "@snapMLEngine",),
        html.P(children='snapmlengine'),
        html.H2(children = "Analysis",),

        dbc.Row([create_graph(title, x_title, y_title, x_data, y_data) for title, x_title, y_title, x_data, y_data in data]),

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

    figures = [create_graph_for_report(title, x_title, y_title, x_data, y_data) for title, x_title, y_title, x_data, y_data in data]
    print(figures)

    for i,fig in enumerate(figures):
        fig.write_image("temp/graph{}.png".format(i))


if __name__ == "__main__":
    app.run_server(port = 8051, debug=True)
    
