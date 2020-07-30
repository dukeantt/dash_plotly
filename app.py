import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd

main_df = pd.DataFrame()

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

    dcc.Tabs([
        dcc.Tab(label='Tab one', children=[
            dcc.Graph(id='proportion-in-month'),
        ]),
        dcc.Tab(label='Tab two', children=[
            dcc.Graph(id='outcome-proportion-of-all-uc'),
        ]),
        dcc.Tab(label='Tab three', children=[
            dcc.Graph(id='outcome-of-uc'),
        ]),
    ]),
])


def uc_proportion_in_month(labels: list, values: list):
    fig = go.Figure(data=[go.Pie(labels=labels,
                                 values=values)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                      marker=dict(line=dict(color='#000000', width=2)))
    return fig


def outcome_proportion_of_uc(labels: list, values: list):
    fig = go.Figure(data=[go.Pie(labels=labels,
                                 values=values)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                      marker=dict(line=dict(color='#000000', width=2)))
    return fig


def outcome_of_uc(labels: list, values1: list, values2: list):
    fig = make_subplots(1, 2, specs=[[{'type': 'domain'}, {'type': 'domain'}]],
                        subplot_titles=['UC 1', 'UC 2'])
    fig.add_trace(go.Pie(labels=labels, values=values1, scalegroup='one',
                         name="UC 1"), 1, 1)
    fig.add_trace(go.Pie(labels=labels, values=values2, scalegroup='one',
                         name="UC 2"), 1, 2)

    fig.update_layout(title_text='UC outcomes')
    return fig


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

    uc_proportion_in_month_fig = uc_proportion_in_month(["UC 1", "UC 2", "Other"], [18, 38, 167])
    outcome_proportion_of_uc_fig = outcome_proportion_of_uc(
        ["thanks", "shipping", "handover", "silence", "other", "agree"],
        [0, 5, 18, 24, 8, 1])
    outcome_of_uc_fig = outcome_of_uc(
        ["thanks", "shipping", "handover", "silence", "other", "agree"],
        [0, 2, 5, 7, 3, 1],
        [0, 3, 13, 17, 5, 0],
    )
    return uc_proportion_in_month_fig, outcome_proportion_of_uc_fig, outcome_of_uc_fig
    # return html.Div([
    #     html.H5(filename),
    #     html.H6(datetime.datetime.fromtimestamp(date)),
    #
    #     dash_table.DataTable(
    #         data=df.to_dict('records'),
    #         columns=[{'name': i, 'id': i} for i in df.columns]
    #     ),
    #
    #     html.Hr(),  # horizontal line
    #
    #     # For debugging, display the raw contents provided by the web browser
    #     html.Div('Raw Content'),
    #     html.Pre(contents[0:200] + '...', style={
    #         'whiteSpace': 'pre-wrap',
    #         'wordBreak': 'break-all'
    #     })
    # ])


@app.callback([Output('proportion-in-month', 'figure'),
               Output('outcome-proportion-of-all-uc', 'figure'),
               Output('outcome-of-uc', 'figure'), ],
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        # children = [
        #     parse_contents(c, n, d) for c, n, d in
        #     zip(list_of_contents, list_of_names, list_of_dates)]
        for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
            uc_proportion_in_month_fig, outcome_proportion_of_uc_fig, outcome_of_uc_fig = parse_contents(c, n, d)
        return uc_proportion_in_month_fig, outcome_proportion_of_uc_fig, outcome_of_uc_fig


if __name__ == '__main__':
    app.run_server(debug=True)
