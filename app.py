import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(
        [html.Div(id='first-pie'),
         html.Div(id='second-pie'), ]
    ),
    html.Div(id='third-pie'),
    html.Div(id='forth-pie'),
])


def create_trace1():
    colors = ['mediumturquoise', 'darkorange', 'lightgreen']
    trace = go.Pie(
        labels=['Other', 'UC 1', 'UC 2'],
        values=[167, 18, 38],
        hoverinfo='label+percent',
        textinfo='label+value+percent',
        textfont_size=15,
        marker=dict(colors=colors, line=dict(color='#000000', width=2))
    )
    first_pie = html.Div(
        # id="leads_source_container",
        className="six columns chart_div pretty_container",
        children=[
            html.P("First pie"),
            dcc.Graph(
                figure={"data": [trace]},
                style={"height": "90%", "width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return first_pie


def create_trace2():

    trace = go.Pie(
        labels=['thanks', 'shipping', 'handover', "silence", "other", "agree"],
        values=[0, 5, 18, 24, 8, 1],
        direction="clockwise",
        sort=False,
        rotation=120,
        hoverinfo='label+percent',
        textinfo='label+value',
        textfont_size=15,
        marker=dict(line=dict(color='#000000', width=2))
    )
    second_pie = html.Div(
        # id="leads_source_container",
        className="six columns chart_div pretty_container",
        children=[
            html.P("Second pie"),
            dcc.Graph(
                figure={"data": [trace]},
                style={"height": "90%", "width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return second_pie


def create_trace3():
    labels = ['thanks', 'shipping', 'handover', "silence", "other", "agree"]
    trace_1 = go.Pie(labels=labels, values=[0, 2, 5, 7, 3, 1], scalegroup='one',
                     name="UC1", direction="clockwise", sort=False, rotation=120, hoverinfo='label+percent',
                     textinfo='label+value', textfont_size=15,
                     marker=dict(line=dict(color='#000000', width=2)))

    third_pie = html.Div(
        # id="leads_source_container",
        className="six columns chart_div pretty_container",
        children=[
            html.P("Third pie"),
            dcc.Graph(
                figure={"data": [trace_1]},
                style={"height": "90%", "width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return third_pie


def create_trace4():
    labels = ['thanks', 'shipping', 'handover', "silence", "other", "agree"]
    trace_2 = go.Pie(labels=labels, values=[0, 3, 13, 17, 5, 0], scalegroup='one',
                     name="UC2", direction="clockwise", sort=False, rotation=120, hoverinfo='label+percent',
                     textinfo='label+value', textfont_size=15,
                     marker=dict(line=dict(color='#000000', width=2)))
    forth_pie = html.Div(
        # id="leads_source_container",
        className="six columns chart_div pretty_container",
        children=[
            html.P("Forth pie"),
            dcc.Graph(
                figure={"data": [trace_2]},
                style={"height": "90%", "width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return forth_pie


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    first_pie = create_trace1()
    second_pie = create_trace2()
    third_pie = create_trace3()

    return first_pie


@app.callback(
    [
        Output('first-pie', 'children'),
        Output('second-pie', 'children'),
        Output('third-pie', 'children'),
        Output('forth-pie', 'children'),
    ],
    [
        Input('upload-data', 'contents')
    ],
    [
        State('upload-data', 'filename'),
        State('upload-data', 'last_modified')
    ])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        first_pie = create_trace1()
        second_pie = create_trace2()
        third_pie = create_trace3()
        forth_pie = create_trace4()

        # return first_pie, second_pie, third_pie
        # return children[0]
        return first_pie, second_pie, third_pie,forth_pie
    else:
        return "", "", "", ""


if __name__ == '__main__':
    app.run_server(debug=True)
