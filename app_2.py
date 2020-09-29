import dash
from dash.dependencies import Input, Output, State

import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import numpy as np
from utils.helper import *
import logging
from random import randrange
import pandas as pd
import dash_table
from datetime import datetime as dt
from datetime import date, timedelta

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP]
                )

app.layout = html.Div(children=[
    html.Div(
        id="sidebar",
        className="sidebar",
        children=[
            html.H5(
                style={"color": "white"},
                children=["SALESBOT"]
            ),
            html.A(id="a1_title_sidebar", href="#part_1_title", className="title_sidebar", children=["Overall Performance"]),
            html.A(id="a2_title_sidebar", href="#part_2_title", className="title_sidebar", children=["Bot performance by Outcomes"]),
            html.A(id="a3_title_sidebar", href="#part_3_title", className="title_sidebar", children=["Bot performance by Use cases"]),
            html.A(id="a4_title_sidebar", href="#part_4_title", className="title_sidebar", children=["Outcome of each Use case"]),
        ]
    ),

    html.Div(
        id="page_content_and_graph",
        children=[
            html.Div(
                id="part_1_title",
                children=["Overall Performance"],
            ),
            html.Div(
                id="part_1_subtitle_1",
                className="part_1_subtitle",
                children=["Statistics by last week: abc"],
            ),
            html.Div(
                className="basic-metrics",
                children=[
                    html.Div(
                        className="col-md-4",
                        children=[
                            html.Div(
                                id="no_conversations_lastweek",
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.Img(src="assets/icon/conversation_icon.png",
                                                     className="sub_basic_metrics_img"),
                                            html.P("Conversations", style={"display": "inline", "paddingLeft": "19px",
                                                                           "fontSize": "19px"}),
                                        ]
                                    )
                                ]
                            ),
                        ]
                    ),
                    html.Div(
                        className="col-md-4",
                        children=[
                            html.Div(
                                id="no_users_lastweek",
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.Img(src="assets/icon/user_icon.png",
                                                     className="sub_basic_metrics_img"),
                                            html.P("Users", style={"display": "inline", "paddingLeft": "19px",
                                                                   "fontSize": "19px"}),
                                        ]
                                    )
                                ]
                            ),
                        ]
                    ),
                    html.Div(
                        className="col-md-4",
                        children=[
                            html.Div(
                                id="success_rate_lastweek",
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.Img(src="assets/icon/success_rate_icon.png",
                                                     className="sub_basic_metrics_img"),
                                            html.P("Success Rate", style={"display": "inline", "paddingLeft": "19px",
                                                                          "fontSize": "19px"}),
                                        ]
                                    )
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            html.Div(
                id="part_1_subtitle_2",
                className="part_1_subtitle",
                children=["Statistics by month"],
            ),
            html.Div(
                className="basic-metrics",
                children=[
                    html.Div(
                        className="col-md-4",
                        children=[
                            html.Div(
                                id="no_conversations_by_month",
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            # html.Img(src="assets/icon/conversation_icon.png", className="sub_basic_metrics_img"),
                                            html.P("Conversations by month",
                                                   style={"display": "inline", "paddingLeft": "19px",
                                                          "fontSize": "19px"}),
                                        ]
                                    )
                                ]
                            ),
                        ]
                    ),
                    html.Div(
                        className="col-md-4",
                        children=[
                            html.Div(
                                id="no_users_by_month",
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.P("Users by month", style={"display": "inline", "paddingLeft": "19px",
                                                                            "fontSize": "19px"}),
                                        ]
                                    )
                                ]
                            ),
                        ]
                    ),
                    html.Div(
                        className="col-md-4",
                        children=[
                            html.Div(
                                id="success_rate_by_month",
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.P("Success rate by month",
                                                   style={"display": "inline", "paddingLeft": "19px",
                                                          "fontSize": "19px"}),
                                        ]
                                    )
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            html.Div(
                id="part_1_subtitle_3",
                className="part_1_subtitle",
                children=["Overall Performance by selected period"],
            ),
            html.Div(
                id="date_picker_and_run",
                children=[
                    dcc.DatePickerSingle(
                        id='my_date_picker_start',
                        min_date_allowed=dt(2020, 1, 1),
                        max_date_allowed=dt(2021, 12, 31),
                        style={"borderRadius": "25px"},
                        placeholder='Start date',
                    ),
                    dcc.DatePickerSingle(
                        style={"paddingLeft": "20px", "borderRadius": "25px", "paddingRight": "20px"},
                        id='my_date_picker_end',
                        min_date_allowed=dt(2020, 1, 1),
                        max_date_allowed=dt(2021, 12, 31),
                        placeholder='End date',
                    ),
                    html.Button('Run', id='run-analytics',
                                style={"borderRadius": "4px", "backgroundColor": "#448efc", "color": "white",
                                       "width": "45px", "height": "45px", "borderStyle": "hidden"}, ),
                ]
            ),
            html.Div(
                className="basic-metrics",
                children=[
                    html.Div(
                        className="col-md-4",
                        children=[
                            html.Div(
                                id="no_conversations_in_period",
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.Img(src="assets/icon/conversation_icon.png",
                                                     className="sub_basic_metrics_img"),
                                            html.P("Conversations", style={"display": "inline", "paddingLeft": "19px",
                                                                           "fontSize": "19px"}),
                                        ]
                                    )
                                ]
                            ),
                        ]
                    ),
                    html.Div(
                        className="col-md-4",
                        children=[
                            html.Div(
                                id="no_users_in_period",
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.Img(src="assets/icon/user_icon.png",
                                                     className="sub_basic_metrics_img"),
                                            html.P("Users", style={"display": "inline", "paddingLeft": "19px",
                                                                   "fontSize": "19px"}),
                                        ]
                                    )
                                ]
                            ),
                        ]
                    ),
                    html.Div(
                        className="col-md-4",
                        children=[
                            html.Div(
                                id="success_rate_in_period",
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.Img(src="assets/icon/success_rate_icon.png",
                                                     className="sub_basic_metrics_img"),
                                            html.P("Success Rate", style={"display": "inline", "paddingLeft": "19px",
                                                                          "fontSize": "19px"}),
                                        ]
                                    )
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            html.Div(
                id="part_2_title",
                className="big-title",
                children=["Bot Performance by Outcomes"],
            ),
            html.Div(
                id="",
                className="basic-metrics",
                children=[
                    html.Div(
                        className="col-md-6",
                        children=[
                            html.Div(
                                id="no_outcome_bar",
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.P("Number of Outcomes")
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        className="col-md-6",
                        children=[
                            html.Div(
                                id="percent_outcome_pie ",
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.P("Percentages of Outcomes")
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                id="show_table_and_filter_outcome",
                children=[
                    html.Button('View detail', id='show_hide_table_outcome',
                                style={"borderRadius": "4px", "backgroundColor": "#448efc", "color": "white",
                                       "width": "213px", "height": "38px", "borderStyle": "hidden"}, ),
                ]
            ),

            html.Div(
                id="conversation_table_by_outcome",
                className="basic-metrics",
                children=[
                    html.Div(
                        className="col-md-12",
                        children=[
                            html.Div(
                                # id="table_content",
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.P("Chatlog Data")
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                ]
            ),

            html.Div(
                id="part_3_title",
                className="big-title",
                children=["Bot Performance by Use cases"],
            ),
            html.Div(
                id="",
                className="basic-metrics",
                children=[
                    html.Div(
                        className="col-md-6",
                        children=[
                            html.Div(
                                id="no_usecase_bar",
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.P("Number of Use cases")
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        className="col-md-6",
                        children=[
                            html.Div(
                                id="percent_usecase_pie ",
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.P("Percentages of Use cases")
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                id="show_table_and_filter_usecase",
                children=[
                    html.Button('View detail', id='show_hide_table_usecase',
                                style={"borderRadius": "4px", "backgroundColor": "#448efc", "color": "white",
                                       "width": "213px", "height": "38px", "borderStyle": "hidden"}, ),
                ]
            ),
            html.Div(
                id="conversation_table_by_usecase",
                className="basic-metrics",
                children=[
                    html.Div(
                        className="col-md-12",
                        children=[
                            html.Div(
                                # id="table_content",
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.P("Chatlog Data")
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                ]
            ),

            html.Div(
                id="part_4_title",
                className="big-title",
                children=["Outcome of Use cases"],
            ),

            html.Div(
                id="all_outcome_of_usecase",
                className="",
                children=[
                    html.Div(
                        id="first_2_uc",
                        className="basic-metrics",
                        children=[
                            html.Div(
                                className="col-md-6 basic-metrics",
                                children=[
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Number of outcomes")
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Percentages of outcomes")
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                ]
                            ),
                            html.Div(
                                className="col-md-6 basic-metrics",
                                children=[
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Number of outcomes")
                                                        ]
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Percentages of outcomes")
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    html.Div(
                        id="second_2_uc",
                        className="basic-metrics",
                        children=[
                            html.Div(
                                className="col-md-6 basic-metrics",
                                children=[
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Number of outcomes")
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Percentages of outcomes")
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                ]
                            ),
                            html.Div(
                                className="col-md-6 basic-metrics",
                                children=[
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Number of outcomes")
                                                        ]
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Percentages of outcomes")
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    html.Div(
                        id="third_2_uc",
                        className="basic-metrics",
                        children=[
                            html.Div(
                                className="col-md-6 basic-metrics",
                                children=[
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Number of outcomes")
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Percentages of outcomes")
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                ]
                            ),
                            html.Div(
                                className="col-md-6 basic-metrics",
                                children=[
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Number of outcomes")
                                                        ]
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Percentages of outcomes")
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    html.Div(
                        id="fourth_2_uc",
                        className="basic-metrics",
                        children=[
                            html.Div(
                                className="col-md-6 basic-metrics",
                                children=[
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Number of outcomes")
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Percentages of outcomes")
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                ]
                            ),
                            html.Div(
                                className="col-md-6 basic-metrics",
                                children=[
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Number of outcomes")
                                                        ]
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        className="col-md-6",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.P("Percentages of outcomes")
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),

            html.Div(
                id="space_at_the_end",
                style={"paddingBottom": "100px"},
            )
        ],
    ),

])

if __name__ == '__main__':
    app.run_server(debug=True)
