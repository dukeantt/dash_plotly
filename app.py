import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from datetime import date, timedelta
import dash_table

import pandas as pd
import plotly.graph_objects as go
import plotly
from rasa_chatlog_processor import RasaChalogProcessor
import copy
import dash_bootstrap_components as dbc
import numpy as np
from utils.helper import *
import logging
from random import randrange

logging.basicConfig(filename="logging_data/rasa_chatlog_processor_log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

month_dict = {"1": "January", "2": "February", "3": "March", "4": "April", "5": "May", "6": "June", "7": "July",
              "8": "August",
              "9": "September", "10": "October", "11": "November", "12": "December"}
spinner_list = ["assets/cat-spinner.png", "assets/cat-spinner3.png"]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
suppress_callback_exceptions = True
app = dash.Dash(__name__,  # external_stylesheets=external_stylesheets
                external_stylesheets=[dbc.themes.BOOTSTRAP]
                )
server = app.server
PAGE_SIZE = 10
today = date.today()
four_day_before = today - timedelta(4)
date_start = int(str(four_day_before)[8:10])
date_end = int(str(today)[8:10])
month_start = int(str(four_day_before)[5:7])
month_end = int(str(today)[5:7])
year_start = int(str(four_day_before)[0:4])
year_end = int(str(today)[0:4])
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px',

}

app.layout = html.Div(
    id='main-div',
    style={
        'display': 'flex',
        'flexDirection': 'column'
    },
    children=[

        html.Div(
            id="main_title",
            className="markdown-title",
            children=[
                # dcc.Markdown(''' # Salesbot performance '''),
                html.H1(
                    className='gradient-text',
                    style={"fontSize": "3.5rem"},
                    children=["Salesbot performance"]),
                html.Br(),
                html.Br(),
                # dcc.Markdown(''' ## Overall Performance '''),
                html.H2(
                    className='gradient-text',
                    style={"fontSize": "2.5rem"},
                    children=["Overall Performance"]),
                html.Br(),
                html.Br(),
            ]
        ),
        html.Div(
            id="loading-div",
            style={"display": "block"},
        ),
        html.Div(
            id="loading-div-2",
            style={"display": "none"},
            children=[
                html.Img(id="loading_spinner", src="assets/cat-spinner.png")
            ]
        ),

        html.Div(
            className="d-flex flex-wrap",
            style={
                "marginBottom": "30px"
            },
            children=[
                html.Div(
                    # className="col-md-6 h-50 overall-text-info",
                    className="col-md-6",
                    style={
                        "marginLeft": "118px",
                        "marginTop": "24px",
                    },
                    children=[
                        html.Div(
                            className="d-flex flex-wrap",
                            style={"marginLeft": "13px"},
                            children=[
                                dcc.DatePickerRange(
                                    id='my-date-picker-range',
                                    min_date_allowed=dt(2020, 1, 1),
                                    max_date_allowed=dt(2020, 12, 31),
                                    # initial_visible_month=dt(2020, 7, 1),
                                    start_date=dt(year_start, month_start, date_start).date(),
                                    end_date=dt(year_end, month_end, date_end).date()
                                ),
                                html.Button('Run', id='run-analytics'),
                            ]
                        ),
                        html.Div(
                            className="row",
                            style={
                                "marginTop": "73px"
                            },
                            children=[
                                html.Div(
                                    className="col-md-4",
                                    children=[
                                        html.Div(
                                            className="hvr-grow",
                                            id="no-conversations",),
                                    ]
                                ),
                                html.Div(
                                    className="col-md-4",
                                    children=[
                                        html.Div(
                                            className="hvr-grow",
                                            id="no-users"),
                                    ]
                                ),
                                html.Div(
                                    className="col-md-4",
                                    children=[
                                        html.Div(
                                            className="hvr-grow",
                                            id="success-rate"),
                                    ]
                                ),
                            ]
                        )
                    ],
                ),
                html.Div(
                    className="col-md-5 h-50",
                    # style={"marginLeft": "58px"},
                    children=[
                        html.Div(id='success-proportion-in-conversations'),
                    ]
                ),
            ]
        ),

        html.Hr(),

        html.Div(
            className="markdown-title",
            style={
                "marginTop": "60px",
                "marginBottom": "25px"
            },
            children=[
                html.H2(
                    className='gradient-text',
                    style={"fontSize": "2.5rem"},
                    children=["Bot performance by Outcomes"]),
                html.Br(),
                html.Br(),
            ]
        ),
        html.Div(
            className="d-flex flex-wrap",
            style={
                "marginBottom": "30px"
            },
            children=[
                html.Div(
                    className="col-md-5",
                    style={"marginLeft": "118px"},
                    children=[
                        html.P(id="number-of-outcomes", className="outcome_uc_pie_title gradient-text",
                               children=["Number of Outcomes"]),
                        html.Div(id='outcome-proportion-bar-chart')
                    ]
                ),
                html.Div(
                    className="col-md-5",
                    style={"marginLeft": "58px"},
                    children=[
                        html.P(id="percentages-of-outcomes", className="outcome_uc_pie_title gradient-text",
                               children=["Percentages of Outcomes"]),
                        html.Div(id='outcome-proportion-in-conversations'),
                    ]
                ),
            ]
        ),

        dcc.Tabs(
            id="tab_parent",
            style={"width":"1783px"},
            value="shipping",
            children=[
                dcc.Tab(id="thank", label='Thank', value="thank", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='thank-table', style={'marginTop': "40px"}), ]
                        ),
                dcc.Tab(label='Shipping', value="shipping", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='shipping-table', style={'marginTop': "40px"})]
                        ),
                dcc.Tab(label='Handover', value="handover", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='handover-table', style={'marginTop': "40px"}), ]
                        ),
                dcc.Tab(label='Silence', value="silence", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='silence-table', style={'marginTop': "40px"}), ]
                        ),
                dcc.Tab(label='Other', value="other", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='other-table', style={'marginTop': "40px"}), ]
                        ),
                # dcc.Tab(label='Agree', value="agree", style=tab_style, selected_style=tab_selected_style,
                #         children=[html.Div(id='agree-table', style={'marginTop': "40px"}), ]
                #         ),
            ],
        ),

        html.Br(),
        html.Br(),
        html.Hr(),

        html.Div(
            className="markdown-title",
            style={
                "marginTop": "60px",
                "marginBottom": "25px"
            },
            children=[
                html.H2(
                    className='gradient-text',
                    style={"fontSize": "2.5rem"},
                    children=["Bot performance by Use case"]),
                html.Br(),
                html.Br(),
            ]
        ),
        html.Div(
            className="d-flex flex-wrap",
            style={
                "marginBottom": "30px"
            },
            children=[
                html.Div(
                    className="col-md-5 h-50",
                    style={"marginLeft": "118px"},
                    children=[
                        html.P(id="number-of-usecases", className="outcome_uc_pie_title gradient-text",
                               children=["Number of Use cases"]),
                        html.Div(id='uc-proportion-bar-chart')
                    ]
                ),
                html.Div(
                    className="col-md-5 h-50",
                    style={"marginLeft": "58px"},
                    children=[
                        html.P(id="percentages-of-usecases", className="outcome_uc_pie_title gradient-text",
                               children=["Percentages of Use cases"]),
                        html.Div(id='uc-proportion-in-month'),
                    ]
                ),
            ]
        ),

        dcc.Tabs(
            id="uc_tab_parent",
            style={"width":"1785px"},
            value="uc_s1",
            children=[
                dcc.Tab(id="uc_s1", label='UC_S1', value="uc_s1", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='uc-s1', style={'marginTop': "40px"}), ]
                        ),
                dcc.Tab(id="uc_s2", label='UC_S2', value="uc_s2", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='uc-s2', style={'marginTop': "40px"}), ]
                        ),
                dcc.Tab(id="uc_s31", label='UC_S31', value="uc_s31", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='uc-s31', style={'marginTop': "40px"}), ]
                        ),
                dcc.Tab(id="uc_s32", label='UC_S32', value="uc_s32", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='uc-s32', style={'marginTop': "40px"}), ]
                        ),
                dcc.Tab(id="uc_s4", label='UC_S4', value="uc_s4", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='uc-s4', style={'marginTop': "40px"}), ]
                        ),
                dcc.Tab(id="uc_s5", label='UC_S5', value="uc_s5", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='uc-s5', style={'marginTop': "40px"}), ]
                        ),
                dcc.Tab(id="other_usecase_df", label='Other', value="other_usecase_df", style=tab_style,
                        selected_style=tab_selected_style,
                        children=[html.Div(id='other-usecase-df', style={'marginTop': "40px"}), ]
                        ),
            ]
        ),
        html.Div(
            className="d-flex flex-wrap",
            style={"marginBottom": "60px"},
            children=[
                html.Div(
                    className="col-md-6 outcome-uc-pie",
                    children=[
                        html.P(id="outcome-uc1-pie_title", className="outcome_uc_pie_title gradient-text",
                               children=["Outcome of UC-S1"]),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-md-6",
                                    id='outcome-uc1-bar',
                                ),
                                html.Div(
                                    className="col-md-6",
                                    id='outcome-uc1-pie'
                                ),
                            ]
                        ),

                    ]
                ),
                html.Div(
                    className="col-md-6 outcome-uc-pie",
                    children=[
                        html.P(id="outcome-uc2-pie_title", className="outcome_uc_pie_title gradient-text",
                               children=["Outcome of UC-S2"]),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-md-6",
                                    id='outcome-uc2-bar'
                                ),
                                html.Div(
                                    className="col-md-6",
                                    id='outcome-uc2-pie',
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
        html.Div(
            className="d-flex flex-wrap",
            children=[
                html.Div(
                    className="col-md-6 outcome-uc-pie",
                    children=[
                        html.P(id="outcome-uc31-pie_title", className="outcome_uc_pie_title gradient-text",
                               children=["Outcome of UC-S3.1"]),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-md-6",
                                    id='outcome-uc31-bar'
                                ),
                                html.Div(
                                    className="col-md-6",
                                    id='outcome-uc31-pie'
                                ),
                            ]
                        ),
                    ]
                ),
                html.Div(
                    className="col-md-6 outcome-uc-pie",
                    children=[
                        html.P(id="outcome-uc32-pie_title", className="outcome_uc_pie_title gradient-text",
                               children=["Outcome of UC-S3.2"]),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-md-6",
                                    id='outcome-uc32-bar'
                                ),
                                html.Div(
                                    className="col-md-6",
                                    id='outcome-uc32-pie'
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
        html.Div(
            className="d-flex flex-wrap",
            children=[
                html.Div(
                    className="col-md-6 h-50 outcome-uc-pie",
                    children=[
                        html.P(id="outcome-uc4-pie_title", className="outcome_uc_pie_title gradient-text",
                               children=["Outcome of UC-S4"]),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-md-6",
                                    id='outcome-uc4-bar'
                                ),
                                html.Div(
                                    className="col-md-6",
                                    id='outcome-uc4-pie'
                                ),
                            ]
                        ),
                    ]
                ),
                html.Div(
                    className="col-md-6 outcome-uc-pie",
                    children=[
                        html.P(id="outcome-uc5-pie_title", className="outcome_uc_pie_title gradient-text",
                               children=["Outcome of UC-S5"]),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-md-6",
                                    id='outcome-uc5-bar',
                                ),
                                html.Div(
                                    className="col-md-6",
                                    id='outcome-uc5-pie',
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
        html.Div(id='df-data', style={'display': 'none'}),
        html.P(id='custom-from-date-data', style={'display': 'none'}),
        html.P(id='custom-to-date-data', style={'display': 'none'}),
        html.P(id='is-click', style={'display': 'none'}, children=["0"]),

    ])


def create_trace_uc_propotion_in_month(total: int, uc1: int, uc2: int, uc31: int, uc32: int, uc_s4, uc_s51, uc_s52,
                                       uc_s53):
    logger.info("Create trace uc proportion in month")

    other = total - uc1 - uc2 - uc31 - uc32 - uc_s4 - uc_s51 - uc_s52 - uc_s53
    colors = ['mediumturquoise', 'darkorange', 'lightgreen']
    trace = go.Pie(
        labels=['UC S1', 'UC S2', "UC S3.1", "UC S3.2", "UC S4", "UC S5.1", "UC S5.2", "UC S5.3", 'Other' + " " * 8],
        values=[uc1, uc2, uc31, uc32, uc_s4, uc_s51, uc_s52, uc_s53, other],
        hoverinfo='label+percent',
        textinfo='label+percent',
        direction="clockwise",
        sort=False,
        textfont_size=13,
        marker=dict(
            colors=["#4385f5", "#ea4235", "#fabd04", "#34a853", "#fed966"],
            line=dict(color='#f9f9f9', width=1)
        )
    )
    first_pie = html.Div(
        className="six columns chart_div pretty_container",
        children=[
            # html.P("Usecases proportion in month"),
            dcc.Graph(
                figure={
                    "data": [trace],
                    'layout': {
                        # 'legend': {
                        #     'orientation': "v",
                        #     'yanchor': "top",
                        #     'y': 0.99,
                        #     'xanchor': "left",
                        #     'x': 0.01,
                        #     'width': "500px",
                        #     "font": {
                        #         # 'family': "Courier",
                        #         'size': 20,
                        #         'color': "black",
                        #     },
                        # },
                        'height': "500",
                        'width': "592.07",
                    }
                },
                style={"height": "90%", "width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return first_pie


def create_trace_uc_propotion_bar_chart(total: int, uc1: int, uc2: int, uc31: int, uc32: int, uc_s4, uc_s51, uc_s52, uc_s53):
    other = total - uc1 - uc2 - uc31 - uc32 - uc_s4 - uc_s51 - uc_s52 - uc_s53
    y_value = [uc1, uc2, uc31, uc32, uc_s4, uc_s51 + uc_s52 + uc_s53, other]
    trace = go.Bar(
        x=['UC-S1', 'UC-S2', 'UC-S3.1', "UC-S3.2", "UC S4", "UC S5", "Other"],
        y=y_value,
        text=y_value,
        textposition='outside',
        texttemplate='%{text:.2s}',
        marker_color='#4385f5',
    )
    bar_chart = html.Div(
        className="six columns chart_div pretty_container",
        children=[
            dcc.Graph(
                figure={
                    "data": [trace],
                    'layout': {
                        'height': "500",
                        'width': "592.07",
                    }
                },
                style={"width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return bar_chart


def create_trace_outcome_proportion_in_all_conversation(uc_outcome: dict):
    logger.info("Create trace ourcome proportion in all conversation")

    outcome_uc1 = uc_outcome["uc_s1"]
    outcome_uc2 = uc_outcome["uc_s2"]
    outcome_uc31 = uc_outcome["uc_s31"]
    outcome_uc32 = uc_outcome["uc_s32"]
    outcome_uc4 = uc_outcome["uc_s4"]
    outcome_uc5 = uc_outcome["uc_s5"]
    outcome_other = uc_outcome["other"]

    uc_s1_values = [value for index, value in outcome_uc1.items()]
    uc_s2_values = [value for index, value in outcome_uc2.items()]
    uc_s31_values = [value for index, value in outcome_uc31.items()]
    uc_s32_values = [value for index, value in outcome_uc32.items()]
    uc_s4_values = [value for index, value in outcome_uc4.items()]
    uc_s5_values = [value for index, value in outcome_uc5.items()]
    uc_other_values = [value for index, value in outcome_other.items()]

    values = [sum(x) for x in zip(uc_s1_values, uc_s2_values, uc_s31_values, uc_s32_values,uc_s4_values,uc_s5_values, uc_other_values)]
    trace = go.Pie(
        labels=['Thanks', 'Shipping', 'Handover', "Silence", 'Other' + " " * 10],
        values=values,
        direction="clockwise",
        sort=False,
        # rotation=120,
        hoverinfo='label+value',
        textinfo='label+percent',
        textfont_size=13,
        marker=dict(
            colors=["#7b92d0", "#ea4235", "#34a853", "#fabd03", "#ff6d00"],
            line=dict(color='#f9f9f9', width=1)
        )
    )
    second_pie = html.Div(
        className="six columns chart_div pretty_container",
        children=[
            # html.P("Outcomes proportion in all conversations"),
            dcc.Graph(
                figure={
                    "data": [trace],
                    'layout': {
                        'height': "500",
                        'width': "592.07",
                    }
                },
                style={"height": "90%", "width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return second_pie, values


def create_trace_outcome_proportion_bar_chart(no_each_outcome: list):
    # 'thanks', 'shipping', 'handover', "silence", "other", "agree"

    trace = go.Bar(
        x=['Thanks', 'Shipping', 'Handover', "Silence", "Other"],
        y=no_each_outcome,
        text=no_each_outcome,
        textposition='outside',
        texttemplate='%{text:.2s}',
        marker_color='#4385f5',
    )
    bar_chart = html.Div(
        className="six columns chart_div pretty_container",
        children=[
            dcc.Graph(
                figure={
                    "data": [trace],
                    'layout': {
                        'height': "500",
                        'width': "592.07",
                    }
                },
                style={"width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return bar_chart


def create_trace_success_proportion_in_all_conversations(no_each_outcome: list):
    # 'thanks', 'shipping', 'handover', "silence", "other", "agree"
    no_success = no_each_outcome[0] + no_each_outcome[1]
    no_other = no_each_outcome[2] + no_each_outcome[3] + no_each_outcome[4]
    success_rate = str('{0:.2f}'.format((no_success * 100) / (no_other + no_success))) + "%"
    trace = go.Pie(
        labels=['Successful', 'Other' + " " * 13],
        values=[no_success, no_other],
        direction="clockwise",
        sort=False,
        # rotation=120,
        hoverinfo='label+value',
        textinfo='label+percent',
        textfont_size=11,
        marker=dict(
            colors=["#fe0000", "#4286f5"],
            line=dict(color='#f9f9f9', width=1)
        )
    )
    pie = html.Div(
        className="six columns chart_div pretty_container",
        children=[
            dcc.Graph(
                figure={
                    "data": [trace],
                    'layout': {
                        # 'legend': {
                        #     'orientation': "v",
                        #     'yanchor': "top",
                        #     'y': 0.99,
                        #     'xanchor': "left",
                        #     'x': 0.01,
                        #     'width' : "500px",
                        #     "font": {
                        #         # 'family': "Courier",
                        #         'size': 20,
                        #         'color': "black",
                        #     },
                        # },
                    }
                },
                style={"height": "90%", "width": "100%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return pie, success_rate


def create_trace_outcome_uc(uc_outcome: dict, key: str, name: str, title: str):
    logger.info("Create trace ourcome proportion in each use_case")

    outcome_uc = uc_outcome[key]
    values = [value for index, value in outcome_uc.items()]
    labels = ['Thanks', 'Shipping', 'Handover', "Silence", 'Other' + " " * 10]
    trace_2 = go.Pie(
        labels=labels, values=values, scalegroup='one',
        name=name,
        direction="clockwise",
        sort=False,
        # rotation=120,
        hoverinfo='label+value',
        textinfo='label+percent',
        textfont_size=10,
        marker=dict(
            colors=["#7b92d0", "#ea4235", "#34a853", "#fabd03", "#ff6d00"],
            line=dict(color='#f9f9f9', width=1)
        )
    )
    pie = html.Div(
        # className="six columns chart_div pretty_container",
        # className="six columns chart_div",
        children=[
            # html.P(title),
            dcc.Graph(
                figure={
                    "data": [trace_2],
                    'layout': {
                        'height': "300",
                        'width': "400",
                    }
                },
                style={"height": "90%", "width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return pie


def create_trace_outcome_uc_bar_chart(uc_outcome: dict, key: str, name: str, title: str):
    outcome_uc = uc_outcome[key]
    values = [value for index, value in outcome_uc.items()]
    trace = go.Bar(
        x=['Thanks', 'Shipping', 'Handover', "Silence", "Other"],
        y=values,
        text=values,
        textposition='inside',
        texttemplate='%{text:.2s}',
        marker_color='#4385f5',
    )
    bar_chart = html.Div(
        # className="six columns chart_div pretty_container",
        # className="six columns chart_div",
        children=[
            dcc.Graph(
                figure={
                    "data": [trace],
                    'layout': {
                        'height': "300",
                        'width': "400",
                        'xaxis': {
                            "tickfont": {
                                "size": "9"
                            }
                        }
                    },

                },
                style={"width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return bar_chart

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


def reformat_df_output_for_table(df: pd.DataFrame):
    sub_df_list = []
    conversation_ids = df["conversation_id"].drop_duplicates().to_list()
    for conversation_id in conversation_ids:
        info_dict = {x: [] for x in list(df.columns)}
        info_dict.pop('turn', None)
        info_dict.pop('message_id', None)
        info_dict.pop('sender', None)
        info_dict.pop('attachments', None)
        user_counter = 0
        bot_counter = 0
        counter = 0
        conversation_outcome = []

        sub_df = df[df["conversation_id"] == conversation_id]
        sub_df["user_message"] = sub_df["user_message"].astype(str)
        sub_df["bot_message"] = sub_df["bot_message"].astype(str)
        sub_df = sub_df[(sub_df['user_message'] != sub_df['bot_message'])]
        try:
            conversation_uc = [x for x in sub_df["use_case"].drop_duplicates().to_list() if x != ''][0]
        except:
            conversation_uc = ""
        if "outcome" in sub_df:
            conversation_outcome = [x for x in sub_df["outcome"].drop_duplicates().to_list() if x != '']
            if conversation_outcome:
                conversation_outcome = conversation_outcome[0]
            else:
                conversation_outcome = ""

        sender_id = df[df["conversation_id"] == conversation_id]["sender_id"].drop_duplicates().to_list()[0]
        for row in sub_df.itertuples():
            counter += 1
            user_message = row.user_message
            bot_message = row.bot_message
            if user_message is None or user_message == "None" or user_message == "":
                user_message = np.NaN
            if bot_message is None or bot_message == "None" or bot_message == "":
                bot_message = np.NaN
            if str(user_message) == str(bot_message) == "nan":
                continue
            if str(user_message) != "nan" and str(bot_message) == "nan":
                bot_counter = 0
                user_counter += 1

                info_dict["user_message"].append(user_message)
                info_dict["intent"].append(row.intent)
                info_dict["entities"].append(row.entities)
                info_dict["created_time"].append(row.created_time)

                if user_counter > 1:
                    info_dict["bot_message"].append(np.NaN)
                    info_dict["created_time_bot"].append("")

                if counter == len(sub_df):
                    info_dict["bot_message"].append(np.NaN)
                    info_dict["created_time_bot"].append("")

            elif str(user_message) == "nan" and str(bot_message) != "nan":
                bot_counter += 1
                user_counter = 0

                info_dict["bot_message"].append(bot_message)
                info_dict["created_time_bot"].append(row.created_time)

                if bot_counter > 1 or counter == 1:
                    info_dict["user_message"].append(np.NaN)
                    info_dict["created_time"].append("")
                    info_dict["intent"].append("")
                    info_dict["entities"].append("")

        dict_len = len(info_dict["user_message"])
        info_dict["conversation_id"] += [conversation_id] * dict_len
        info_dict["sender_id"] += [sender_id] * dict_len
        info_dict["use_case"].append(conversation_uc)
        info_dict["use_case"] += [""] * (dict_len - 1)
        if "outcome" in sub_df:
            info_dict["outcome"].append(conversation_outcome)
            info_dict["outcome"] += [""] * (dict_len - 1)
        try:
            # for index, item in info_dict.items():
            #     info_dict[index].append("")
            new_sub_df = pd.DataFrame.from_dict(info_dict)
        except:
            a = 0
        sub_df_list.append(new_sub_df)
    if sub_df_list:
        new_df = pd.concat(sub_df_list)
        return new_df
    return df


def generate_table(df: pd.DataFrame):
    logger.info("Generate table")

    df.insert(list(df.columns).index("created_time") + 1, "created_time_bot", "")
    df = reformat_df_output_for_table(df)

    # df = df[df["sender_id"] != 3547113778635846]
    df = df.dropna(subset=["user_message", "bot_message"], how="all")
    col_order = ['created_time', 'sender_id', 'use_case', 'user_message', 'intent', 'entities', 'bot_message']
    if "outcome" in df:
        col_order = ['created_time', 'sender_id', 'use_case', 'user_message', 'intent', 'entities', 'bot_message',
                     'outcome']

    df = df.reindex(columns=col_order)
    df = df.rename(columns={"created_time": "timestamp", "sender_id": "conv_id", "user_message": "input_text",
                            "bot_message": "bot_text"})
    return html.Div([
        dash_table.DataTable(
            id='datatable-paging',
            page_action="native",
            page_current=0,
            page_size=10,

            style_header={
                'backgroundColor': '#0c5395',
                'color': 'white',
                'fontWeight': 'bold',
                'height': '40px',
            },
            style_data={  # style cho ca header va cell
                # 'whiteSpace': 'normal',
                # 'height': 'auto',
                # 'lineHeight': '15px',
                'height': '40px',
            },
            style_cell={
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                # 'minWidth': '0px',
                # 'width': '160px', 'maxWidth': '300px',
                'textAlign': "left",
            },
            style_cell_conditional=
            [
                {
                    'if': {'column_id': c},
                    'minWidth': '60px',
                    'width': '60px',
                    'maxWidth': '60px',
                } for c in ['use_case']
            ] +
            [
                {
                    'if': {'column_id': x},
                    'color': 'blue',
                } for x in ["use_case", "input_text", "bot_text"]
            ] +
            [
                {
                    'if': {'column_id': x},
                    'minWidth': '130px',
                    'width': '130px',
                    'maxWidth': '130px'
                } for x in ["timestamp", "conv_id"]
            ] +
            [
                {
                    'if': {'column_id': x},
                    'minWidth': '260px',
                    'width': '260px',
                    'maxWidth': '260px',
                } for x in ["input_text", "bot_text"]
            ] +
            [
                {
                    'if': {'column_id': x},
                    'minWidth': '160px',
                    'width': '160px',
                    'maxWidth': '160px',

                } for x in ["intent", "entities"]
            ] +
            [
                {
                    'if': {'column_id': x},
                    'minWidth': '80px',
                    'width': '80px',
                    'maxWidth': '80px',

                } for x in ["outcome"]
            ]
            ,
            tooltip_data=[  # hover  data
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('rows')
            ],
            style_data_conditional=[  # stripe style table
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            tooltip_duration=None,
            # fixed_columns={'headers': True, 'data': 1},
            # fixed_rows={'headers': True},

            style_table={
                'minWidth': '100%',
                # 'height': '400px',
                # 'overflowY': 'auto',
                # 'overflowX': 'auto'
            },

            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
    ])


def get_number_of_each_uc(df: pd.DataFrame):
    logger.info("Count each usecase")

    total = len(list(dict.fromkeys(list(df["conversation_id"]))))
    uc_s1 = len(df[df["use_case"] == "uc_s1"])
    uc_s2 = len(df[df["use_case"] == "uc_s2"])
    uc_s31 = len(df[df["use_case"] == "uc_s31"])
    uc_s32 = len(df[df["use_case"] == "uc_s32"])
    uc_s41 = len(df[df["use_case"] == "uc_s4.1"])
    uc_s42 = len(df[df["use_case"] == "uc_s4.2"])
    uc_s43 = len(df[df["use_case"] == "uc_s4.3"])
    uc_s51 = len(df[df["use_case"] == "uc_s5.1"])
    uc_s52 = len(df[df["use_case"] == "uc_s5.2"])
    uc_s53 = len(df[df["use_case"] == "uc_s5.3"])

    uc_s4 = uc_s41 + uc_s42 + uc_s43

    return total, uc_s1, uc_s2, uc_s31, uc_s32, uc_s4, uc_s51, uc_s52, uc_s53


def get_number_of_each_outcome_each_uc(df: pd.DataFrame):
    logger.info("Count outcome each use_case")

    """ thank -> shipping -> handover -> silence ->  other"""
    uc_outcome = {
        "uc_s1": {"thank": 0, "shipping_order": 0, "handover_to_inbox": 0, "silence": 0, "other": 0},
        "uc_s2": {"thank": 0, "shipping_order": 0, "handover_to_inbox": 0, "silence": 0, "other": 0},
        "uc_s31": {"thank": 0, "shipping_order": 0, "handover_to_inbox": 0, "silence": 0, "other": 0},
        "uc_s32": {"thank": 0, "shipping_order": 0, "handover_to_inbox": 0, "silence": 0, "other": 0},
        "uc_s4": {"thank": 0, "shipping_order": 0, "handover_to_inbox": 0, "silence": 0, "other": 0},
        "uc_s5": {"thank": 0, "shipping_order": 0, "handover_to_inbox": 0, "silence": 0, "other": 0},
        "other": {"thank": 0, "shipping_order": 0, "handover_to_inbox": 0, "silence": 0, "other": 0},
    }

    conversation_id = list(df["conversation_id"])
    conversation_id = list(dict.fromkeys(conversation_id))

    for id in conversation_id:
        greet_first_turn = False
        sub_df = df[df["conversation_id"] == id]
        use_case = list(filter(lambda x: x != "", list(sub_df["use_case"])))
        if sub_df.iloc[0]["intent"] == "start_conversation" or sub_df.iloc[0]["intent"] == "greet":
            greet_first_turn = True

        if len(use_case) > 0:
            use_case = use_case[0]
        else:
            use_case = "other"
        try:
            if use_case in ["uc_s4.1", "uc_s4.2", "uc_s4.3"]:
                use_case = "uc_s4"
            if use_case in ["uc_s5.1", "uc_s5.2", "uc_s5.3"]:
                use_case = "uc_s5"
            outcome = list(filter(lambda x: x != "", list(sub_df["outcome"])))[0]
            if greet_first_turn and outcome == "thank" and len(sub_df["turn"].drop_duplicates()) == 2:
                continue
            elif outcome == "thank" and len(sub_df["turn"].drop_duplicates()) == 1:
                continue
            # if greet_first_turn and outcome == "shipping_order" and len(sub_df["turn"].drop_duplicates()) == 2:
            #     continue
            # elif outcome == "shipping_order" and len(sub_df["turn"].drop_duplicates()) == 1:
            #     continue
            uc_outcome[use_case][outcome] += 1
        except:
            a = 0

    return uc_outcome


def get_conversation_each_outcome(df: pd.DataFrame):
    logger.info("Get conversation for each outcome")

    column_list = ["conversation_id", "use_case", "sender_id", "user_message", "bot_message", "created_time", "intent",
                   "entities"]
    qualified_thank = []
    qualified_shipping = []

    for id in df[df["outcome"] == "thank"]["conversation_id"].to_list():
        if len(df[df["conversation_id"] == id]["turn"].drop_duplicates()) > 1:
            qualified_thank.append(id)

    # for id in df[df["outcome"] == "shipping_order"]["conversation_id"].to_list():
    #     if len(df[df["conversation_id"] == id]["turn"].drop_duplicates()) > 1:
    #         qualified_shipping.append(id)

    thank_df = df[df["conversation_id"].isin(qualified_thank)][column_list]
    # shipping_order_df = df[df["conversation_id"].isin(qualified_shipping)][column_list]
    shipping_order_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "shipping_order"]["conversation_id"]))][column_list]
    handover_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "handover_to_inbox"]["conversation_id"]))][column_list]
    silence_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "silence"]["conversation_id"]))][column_list]
    other_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "other"]["conversation_id"]))][column_list]
    # agree_df = df[df["conversation_id"].isin(list(df[df["outcome"] == "agree"]["conversation_id"]))][column_list]

    return thank_df, shipping_order_df, handover_df, silence_df, other_df, \
        # agree_df


def get_conversation_each_usecase(df: pd.DataFrame):
    logger.info("Get conversation for each use_case")

    column_list = ["conversation_id", "use_case", "outcome", "sender_id", "user_message", "bot_message", "created_time",
                   "intent",
                   "entities"]
    uc1_df = df[df["conversation_id"].isin(list(df[df["use_case"] == "uc_s1"]["conversation_id"]))][column_list]
    uc2_df = df[df["conversation_id"].isin(list(df[df["use_case"] == "uc_s2"]["conversation_id"]))][column_list]
    uc31_df = df[df["conversation_id"].isin(list(df[df["use_case"] == "uc_s31"]["conversation_id"]))][column_list]
    uc32_df = df[df["conversation_id"].isin(list(df[df["use_case"] == "uc_s32"]["conversation_id"]))][column_list]
    uc4_df = df[df["conversation_id"].isin(list(df[df["use_case"].isin(["uc_s4.1", "uc_s4.2", "uc_s4.3"])]["conversation_id"]))][column_list]
    uc5_df = df[df["conversation_id"].isin(list(df[df["use_case"].isin(["uc_s5.1", "uc_s5.2", "uc_s5.3"])]["conversation_id"]))][column_list]

    noticable_usecase_conversation_id = uc1_df["conversation_id"].drop_duplicates().to_list() \
                                        + uc2_df["conversation_id"].drop_duplicates().to_list() \
                                        + uc31_df["conversation_id"].drop_duplicates().to_list() \
                                        + uc32_df["conversation_id"].drop_duplicates().to_list() \
                                        + uc4_df["conversation_id"].drop_duplicates().to_list() \
                                        + uc5_df["conversation_id"].drop_duplicates().to_list()

    other_usecase_df = df[~df["conversation_id"].isin(noticable_usecase_conversation_id)][column_list]

    return uc1_df, uc2_df, uc31_df, uc32_df, uc4_df, uc5_df, other_usecase_df


@app.callback(
    [
        Output(component_id='custom-from-date-data', component_property='children'),
        Output(component_id='custom-to-date-data', component_property='children'),

    ],
    [
        Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date'),
    ],
)
def set_date_data(start_date, end_date):
    if start_date is not None and end_date is not None:
        return start_date, end_date
    else:
        return "", ""


@app.callback(
    [
        Output(component_id='loading-div', component_property='children'),
        Output(component_id='loading-div-2', component_property='children'),
        Output(component_id='is-click', component_property='children'),
    ],
    [
        Input(component_id='run-analytics', component_property='n_clicks')
    ],
    [
        State('custom-from-date-data', 'children'),
        State('custom-to-date-data', 'children'),
        State('loading-div', 'style'),
        State('loading-div-2', 'style'),
    ]
)
def show_loading(n_clicks, start_date, end_date, loading1, loading2):
    if start_date is not None and end_date is not None:
        spinner = randrange(2)
        loading_child = html.Div(style={
            'display': 'block',
            'position': 'fixed',
            'top': '0',
            'bottom': '0',
            'left': '-200',
            'right': '-100',
            'backgroundColor': '#f9f9f9',
            'opacity': '0.8',
            'zIndex': '1002',
            'width': '2000px',
        },
            children=[html.Img(id="cat_loading_spinner", src=spinner_list[spinner], style={"position": "sticky"})]
        )
        display_loading_1 = loading1["display"]
        display_loading_2 = loading2["display"]
        if display_loading_1 != "none":
            loading_1_child = loading_child
            loading_2_child = ""
            return loading_1_child, loading_2_child, "1"
        elif display_loading_2 != "none":
            loading_1_child = ""
            loading_2_child = loading_child
            return loading_1_child, loading_2_child, "1"
    else:
        return html.Div(style={'display': 'none'}), html.Div(style={'display': 'none'}), "0"


@app.callback(
    Output('df-data', 'children'),
    [
        Input('is-click', 'children'),
    ],
    [
        State('custom-from-date-data', 'children'),
        State('custom-to-date-data', 'children'),
    ],
)
def handle_df(is_click, start_date, end_date):
    if is_click == "1" and start_date is not None and end_date is not None:
        df = get_chatlog_from_db(from_date=start_date, to_date=end_date)
        # processor = RasaChalogProcessor()
        # df = processor.process_rasa_chatlog("06", "abc", df)
        if len(df) == 0:
            return None
        return df.to_json(date_format='iso', orient='split')
    else:
        return None


@app.callback(
    [
        Output("success-proportion-in-conversations", 'children'),
        Output("no-conversations", 'children'),
        Output("no-users", 'children'),
        Output("success-rate", 'children'),
        Output("uc-proportion-bar-chart", 'children'),
        Output('uc-proportion-in-month', 'children'),
        Output('outcome-proportion-bar-chart', 'children'),
        Output('outcome-proportion-in-conversations', 'children'),

        Output('outcome-uc1-pie', 'children'),
        Output('outcome-uc2-pie', 'children'),
        Output('outcome-uc31-pie', 'children'),
        Output('outcome-uc32-pie', 'children'),
        Output('outcome-uc4-pie', 'children'),
        Output('outcome-uc5-pie', 'children'),

        Output('outcome-uc1-bar', 'children'),
        Output('outcome-uc2-bar', 'children'),
        Output('outcome-uc31-bar', 'children'),
        Output('outcome-uc32-bar', 'children'),
        Output('outcome-uc4-bar', 'children'),
        Output('outcome-uc5-bar', 'children'),

        Output('thank-table', 'children'),
        Output('shipping-table', 'children'),
        Output('handover-table', 'children'),
        Output('silence-table', 'children'),
        Output('other-table', 'children'),

        Output('uc-s1', 'children'),
        Output('uc-s2', 'children'),
        Output('uc-s31', 'children'),
        Output('uc-s32', 'children'),
        Output('uc-s4', 'children'),
        Output('uc-s5', 'children'),

        Output('other-usecase-df', 'children'),
        Output(component_id='loading-div', component_property='style'),
        Output(component_id='loading-div-2', component_property='style'),
        Output(component_id='outcome-uc1-pie_title', component_property='style'),
        Output(component_id='outcome-uc2-pie_title', component_property='style'),
        Output(component_id='outcome-uc31-pie_title', component_property='style'),
        Output(component_id='outcome-uc32-pie_title', component_property='style'),
        Output(component_id='number-of-outcomes', component_property='style'),
        Output(component_id='percentages-of-outcomes', component_property='style'),
        Output(component_id='number-of-usecases', component_property='style'),
        Output(component_id='percentages-of-usecases', component_property='style'),
    ],
    [
        Input('df-data', 'children')
    ],
    [
        State('loading-div', 'style'),
        State('loading-div-2', 'style')
    ]
)
def update_output(df, loading1, loading2):
    if df is not None:
        df = pd.read_json(df, orient="split")
        df = df[df["sender_id"] != 3547113778635846]

        not_qualified_thank = []
        not_qualified_shipping = []
        for id in df[df["outcome"] == "thank"]["conversation_id"].to_list():
            if len(df[df["conversation_id"] == id]["turn"].drop_duplicates()) <= 1:
                not_qualified_thank.append(id)

        for id in df[df["outcome"] == "shipping_order"]["conversation_id"].to_list():
            if len(df[df["conversation_id"] == id]["turn"].drop_duplicates()) <= 1:
                not_qualified_shipping.append(id)
        df = df[~df["conversation_id"].isin(not_qualified_thank+not_qualified_shipping)]

        no_conversations = str(len(df["conversation_id"].drop_duplicates(keep='first')))
        no_customers = str(len(df["sender_id"].drop_duplicates(keep='first')))
        total, uc1, uc2, uc31, uc32, uc_s4, uc_s51, uc_s52, uc_s53 = get_number_of_each_uc(df[["conversation_id", "use_case"]])

        uc_outcome = get_number_of_each_outcome_each_uc(df[["conversation_id","user_message", "use_case", "outcome", "turn", "intent"]])

        uc_proportion_in_month = create_trace_uc_propotion_in_month(total, uc1, uc2, uc31, uc32, uc_s4, uc_s51, uc_s52, uc_s53)
        uc_proportion_bar_chart = create_trace_uc_propotion_bar_chart(total, uc1, uc2, uc31, uc32, uc_s4, uc_s51, uc_s52, uc_s53)

        outcome_proportion_in_conversations, number_of_each_outcome = create_trace_outcome_proportion_in_all_conversation(uc_outcome)
        outcome_proportion_bar_chart = create_trace_outcome_proportion_bar_chart(number_of_each_outcome)

        success_proportion_in_conversations, success_rate = create_trace_success_proportion_in_all_conversations(number_of_each_outcome)

        outcome_uc1_pie = create_trace_outcome_uc(uc_outcome, "uc_s1", "UC S1", "Outcomes of UC-S1")
        outcome_uc2_pie = create_trace_outcome_uc(uc_outcome, "uc_s2", "UC S2", "Outcomes of UC-S2")
        outcome_uc31_pie = create_trace_outcome_uc(uc_outcome, "uc_s31", "UC S31", "Outcomes of UC-S31")
        outcome_uc32_pie = create_trace_outcome_uc(uc_outcome, "uc_s32", "UC S32", "Outcomes of UC-S32")
        outcome_uc_s4_pie = create_trace_outcome_uc(uc_outcome, "uc_s4", "UC S4", "Outcomes of UC-S4")
        outcome_uc_s5_pie = create_trace_outcome_uc(uc_outcome, "uc_s5", "UC S5", "Outcomes of UC-S5")

        outcome_uc1_bar = create_trace_outcome_uc_bar_chart(uc_outcome, "uc_s1", "UC S1", "Outcomes of UC-S1")
        outcome_uc2_bar = create_trace_outcome_uc_bar_chart(uc_outcome, "uc_s2", "UC S2", "Outcomes of UC-S2")
        outcome_uc31_bar = create_trace_outcome_uc_bar_chart(uc_outcome, "uc_s31", "UC S31", "Outcomes of UC-S31")
        outcome_uc32_bar = create_trace_outcome_uc_bar_chart(uc_outcome, "uc_s32", "UC S32", "Outcomes of UC-S32")
        outcome_uc_s4_bar = create_trace_outcome_uc_bar_chart(uc_outcome, "uc_s4", "UC S4", "Outcomes of UC-S4")
        outcome_uc_s5_bar = create_trace_outcome_uc_bar_chart(uc_outcome, "uc_s5", "UC S5", "Outcomes of UC-S5")

        thank_df, shipping_order_df, handover_df, silence_df, other_df = get_conversation_each_outcome(df[[
            "conversation_id", "use_case", "outcome", "sender_id", "user_message", "bot_message", "created_time",
            "intent", "entities", "turn"]])
        thank_df = generate_table(thank_df)
        shipping_order_df = generate_table(shipping_order_df)
        handover_df = generate_table(handover_df)
        silence_df = generate_table(silence_df)
        other_df = generate_table(other_df)

        uc1_df, uc2_df, uc31_df, uc32_df, uc4_df, uc5_df, other_usecase_df = get_conversation_each_usecase(df[["conversation_id", "use_case", "outcome", "sender_id", "user_message",
                "bot_message", "created_time", "intent", "entities"]])
        uc1_df = generate_table(uc1_df)
        uc2_df = generate_table(uc2_df)
        uc31_df = generate_table(uc31_df)
        uc32_df = generate_table(uc32_df)
        uc4_df = generate_table(uc4_df)
        uc5_df = generate_table(uc5_df)
        other_usecase_df = generate_table(other_usecase_df)

        loading_1_display = ""
        loading_2_display = ""
        if loading1["display"] == "none":
            loading_1_display = {'display': 'block'}
            loading_2_display = {'display': 'none'}
        elif loading2["display"] == "none":
            loading_1_display = {'display': 'none'}
            loading_2_display = {'display': 'block'}

        no_conversations_div = html.Div(
            className="col-md-12",
            style={
                "backgroundColor": "#ffffff",
                "textAlign": "center",
                "height": "330px",
                "borderRadius": "10px",
            },
            children=[
                html.Img(src="assets/conversation2.png", style={"marginTop": "68px"}),
                html.P("CONVERSATIONS", style={"marginTop": "24px", "color": "#21556a", "fontWeight": "bold", "fontSize": "20px"}),
                html.P(no_conversations, style={"marginTop": "24px", "color": "#21556a", "fontWeight": "bold", "fontSize": "35px"}),
            ]
        )
        no_customers_div = html.Div(
            className="col-md-12",
            style={
                "backgroundColor": "#80c7e3",
                "textAlign": "center",
                "height": "330px",
                "borderRadius": "10px",
            },
            children=[
                html.Img(src="assets/customer_icon2.png", style={"marginTop": "68px"}),
                html.P("USERS", style={"marginTop": "24px", "color": "white", "fontWeight": "bold", "fontSize": "20px"}),
                html.P(no_customers, style={"marginTop": "24px", "color": "white", "fontWeight": "bold", "fontSize": "35px"})
            ]
        )
        success_rate_div = html.Div(
            className="col-md-12",
            style={
                "backgroundColor": "#af28ef",
                "backgroundImage": "linear-gradient(#af28ef, #7876fe)",
                "textAlign": "center",
                "height": "330px",
                "marginLeft": "5px",
                "borderRadius": "10px",
            },
            children=[
                html.Img(src="assets/success_icon2.png", style={"marginTop": "68px"}),
                html.P("SUCCESS RATE", style={"marginTop": "24px", "color": "white", "fontWeight": "bold", "fontSize": "20px"}),
                html.P(success_rate, style={"marginTop": "24px", "color": "white", "fontWeight": "bold", "fontSize": "35px"}),
            ]
        )
        return success_proportion_in_conversations, no_conversations_div, no_customers_div, success_rate_div, \
               uc_proportion_bar_chart, uc_proportion_in_month, outcome_proportion_bar_chart, outcome_proportion_in_conversations, outcome_uc1_pie, outcome_uc2_pie, outcome_uc31_pie, outcome_uc32_pie, outcome_uc_s4_pie, outcome_uc_s5_pie, \
               outcome_uc1_bar, outcome_uc2_bar, outcome_uc31_bar, outcome_uc32_bar, outcome_uc_s4_bar, outcome_uc_s5_bar, \
               thank_df, shipping_order_df, handover_df, silence_df, other_df, uc1_df, uc2_df, uc31_df, uc32_df, uc4_df, uc5_df, other_usecase_df, \
               loading_1_display, loading_2_display, \
               {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {
                   'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    else:
        loading_1_display = ""
        loading_2_display = ""
        if loading1["display"] == "none":
            loading_1_display = {'display': 'block'}
            loading_2_display = {'display': 'none'}
        elif loading2["display"] == "none":
            loading_1_display = {'display': 'none'}
            loading_2_display = {'display': 'block'}
        return "", "", "", "", \
               "", "", "", "", "", "", "", "", "", "", \
               "", "", "", "", "", "", \
               "", "", "", "", "", "", "", "", "", "", "", "", \
               loading_1_display, loading_2_display, \
               {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {
                   'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


if __name__ == '__main__':
    app.run_server(debug=True)
