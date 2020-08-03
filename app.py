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

from rasa_chatlog_processor import RasaChalogProcessor
import copy

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
suppress_callback_exceptions = True
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
PAGE_SIZE = 10

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}
app.layout = html.Div(
    id='main-div',
    style={
        'display': 'flex',
        'flexDirection': 'column'
    },
    children=[
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
            id='a',
            children=[
                html.Div(id='first-pie'),
            ]
        ),
        html.Div(
            id='b',
            children=[
                html.Div(id='second-pie'),
            ]
        ),
        html.Div(
            id='c',
            children=[
                html.Div(id='third-pie'),
            ]
        ),
        html.Div(
            id='d',
            children=[
                html.Div(id='forth-pie'),
            ]
        ),
        dcc.Tabs(
            id="tab_parent",
            value="thank",
            children=[
                dcc.Tab(id="thank", label='Thank', value="thank", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='thank-table'), ]
                        ),
                dcc.Tab(label='Shipping', value="shipping", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='shipping-table'), ]
                        ),
                dcc.Tab(label='Handover', value="handover", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='handover-table'), ]
                        ),
                dcc.Tab(label='Silence', value="silence", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='silence-table'), ]
                        ),
                dcc.Tab(label='Other', value="other", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='other-table'), ]
                        ),
                dcc.Tab(label='Agree', value="agree", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='agree-table'), ]
                        ),
            ],
        ),

        html.Div(id='df-data', style={'display': 'none'}),

    ])


def create_trace_uc_propotion_in_month(total: int, uc1: int, uc2: int):
    not_uc1_uc2 = total - uc1 - uc2
    colors = ['mediumturquoise', 'darkorange', 'lightgreen']
    trace = go.Pie(
        labels=['Other', 'UC 1', 'UC 2'],
        values=[not_uc1_uc2, uc1, uc2],
        hoverinfo='label+percent',
        textinfo='label+value+percent',
        textfont_size=15,
        marker=dict(colors=colors, line=dict(color='#000000', width=2))
    )
    first_pie = html.Div(
        # id="leads_source_container",
        className="six columns chart_div pretty_container",
        children=[
            html.P("UC1 and UC2 proportion in June"),
            dcc.Graph(
                figure={"data": [trace]},
                style={"height": "90%", "width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return first_pie


def create_trace_outcome_proportion_in_uc(outcome_uc1: dict, outcome_uc2: dict):
    uc_1_values = [value for index, value in outcome_uc1.items()]
    uc_2_values = [value for index, value in outcome_uc2.items()]
    values = [sum(x) for x in zip(uc_1_values, uc_2_values)]
    trace = go.Pie(
        labels=['thanks', 'shipping', 'handover', "silence", "other", "agree"],
        values=values,
        # values=[0, 5, 18, 24, 8, 1],
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
            html.P("Outcomes proportion in UC1 and UC2 conversations"),
            dcc.Graph(
                figure={"data": [trace]},
                style={"height": "90%", "width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return second_pie


def create_trace_outcome_uc1(outcome_uc1: dict):
    values = [value for index, value in outcome_uc1.items()]
    labels = ['thanks', 'shipping', 'handover', "silence", "other", "agree"]
    trace_1 = go.Pie(labels=labels, values=values, scalegroup='one',
                     name="UC1", direction="clockwise", sort=False, rotation=120, hoverinfo='label+percent',
                     textinfo='label+value', textfont_size=15,
                     marker=dict(line=dict(color='#000000', width=2)))

    third_pie = html.Div(
        # id="leads_source_container",
        className="six columns chart_div pretty_container",
        children=[
            html.P("Outcomes of UC1"),
            dcc.Graph(
                figure={"data": [trace_1]},
                style={"height": "90%", "width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return third_pie


def create_trace_outcome_uc2(outcome_uc2: dict):
    values = [value for index, value in outcome_uc2.items()]
    labels = ['thanks', 'shipping', 'handover', "silence", "other", "agree"]
    trace_2 = go.Pie(labels=labels, values=values, scalegroup='one',
                     name="UC2", direction="clockwise", sort=False, rotation=120, hoverinfo='label+percent',
                     textinfo='label+value', textfont_size=15,
                     marker=dict(line=dict(color='#000000', width=2)))
    forth_pie = html.Div(
        # id="leads_source_container",
        className="six columns chart_div pretty_container",
        children=[
            html.P("Outcomes of UC2"),
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

    return df


def generate_table(df: pd.DataFrame):
    return html.Div([
        dash_table.DataTable(
            id='datatable-paging',
            page_action="native",
            page_current=0,
            page_size=10,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_data={  # style cho ca header va cell
                # 'whiteSpace': 'normal',
                # 'height': 'auto',
                # 'lineHeight': '15px',
            },
            style_cell={
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'minWidth': '0px',
                'width': '160px', 'maxWidth': '300px',
                'textAlign': "left",
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'width': '20px'
                } for c in ['use_case']
            ],
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('rows')
            ],
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            tooltip_duration=None,
            fixed_columns={'headers': True, 'data': 1},
            # style_table={'overflowX': 'auto'},
            style_table={'minWidth': '100%'},

            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
    ])


def get_number_of_each_uc(df: pd.DataFrame):
    total = len(list(dict.fromkeys(list(df["conversation_id"]))))
    uc1 = len(df[df["use_case"] == "uc_1"])
    uc2 = len(df[df["use_case"] == "uc_2"])
    return total, uc1, uc2


def get_number_of_each_outcome_each_uc(df: pd.DataFrame):
    """ thank -> shipping -> handover -> silence ->  other -> agree"""
    uc_outcome = {
        "uc_1": {"thank": 0, "shipping_order": 0, "handover_to_inbox": 0, "silence": 0, "other": 0, "agree": 0},
        "uc_2": {"thank": 0, "shipping_order": 0, "handover_to_inbox": 0, "silence": 0, "other": 0, "agree": 0},
    }
    uc1_uc_2_conversation_id = list(df[(df["use_case"] == "uc_1") | (df["use_case"] == "uc_2")]["conversation_id"])
    uc1_uc_2_conversation_id = list(dict.fromkeys(uc1_uc_2_conversation_id))

    for id in uc1_uc_2_conversation_id:
        sub_df = df[df["conversation_id"] == id]
        use_case = list(filter(lambda x: x != "", list(sub_df["use_case"])))[0]
        outcome = list(filter(lambda x: x != "", list(sub_df["outcome"])))[0]
        uc_outcome[use_case][outcome] += 1
    return uc_outcome["uc_1"], uc_outcome["uc_2"]


def get_conversation_each_outcome(df: pd.DataFrame):
    column_list = ["conversation_id", "use_case", "sender_id", "user_message", "bot_message", "created_time", "intent",
                   "entities"]
    thank_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "thanks"]["conversation_id"]))][column_list]
    shipping_order_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "shipping_order"]["conversation_id"]))][
        column_list]
    handover_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "handover_to_inbox"]["conversation_id"]))][
        column_list]
    silence_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "silence"]["conversation_id"]))][column_list]
    other_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "other"]["conversation_id"]))][column_list]
    agree_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "agree"]["conversation_id"]))][column_list]
    return thank_df, shipping_order_df, handover_df, silence_df, other_df, agree_df


@app.callback(
    Output('df-data', 'children'),
    [Input('upload-data', 'contents')],
    [
        State('upload-data', 'filename'),
        State('upload-data', 'last_modified')
    ]
)
def handle_df(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        df = children[0]
        processor = RasaChalogProcessor()
        df = processor.process_rasa_chatlog("06", "abc", df)
        return df.to_json(date_format='iso', orient='split')
    else:
        return None


@app.callback(
    [
        Output('first-pie', 'children'),
        Output('second-pie', 'children'),
        Output('third-pie', 'children'),
        Output('forth-pie', 'children'),
        Output('thank-table', 'children'),
        Output('shipping-table', 'children'),
        Output('handover-table', 'children'),
        Output('silence-table', 'children'),
        Output('other-table', 'children'),
        Output('agree-table', 'children'),
    ],
    [
        Input('df-data', 'children')
    ],
)
def update_output(df):
    if df is not None:
        df = pd.read_json(df, orient="split")

        total, uc1, uc2 = get_number_of_each_uc(df[["conversation_id", "use_case"]])
        outcome_uc1, outcome_uc2 = get_number_of_each_outcome_each_uc(df[["conversation_id", "use_case", "outcome"]])

        first_pie = create_trace_uc_propotion_in_month(total, uc1, uc2)
        second_pie = create_trace_outcome_proportion_in_uc(outcome_uc1, outcome_uc2)
        third_pie = create_trace_outcome_uc1(outcome_uc1)
        forth_pie = create_trace_outcome_uc2(outcome_uc2)

        thank_df, shipping_order_df, handover_df, silence_df, other_df, agree_df = get_conversation_each_outcome(df[[
            "conversation_id", "use_case", "outcome", "sender_id", "user_message", "bot_message", "created_time",
            "intent", "entities"]])

        thank_df = generate_table(thank_df)
        shipping_order_df = generate_table(shipping_order_df)
        handover_df = generate_table(handover_df)
        silence_df = generate_table(silence_df)
        other_df = generate_table(other_df)
        agree_df = generate_table(agree_df)

        return first_pie, second_pie, third_pie, forth_pie, thank_df, shipping_order_df, handover_df, silence_df, other_df, agree_df
    else:
        return "", "", "", "", "", "", "", "", "", ""


if __name__ == '__main__':
    app.run_server(debug=True)
