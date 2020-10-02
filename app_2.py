import dash
from dash.dependencies import Input, Output, State

import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import numpy as np
from utils.helper_2 import *
from utils.draw_chart import *
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
metrics_in_period_text_style = {"display": "block", "paddingLeft": "7rem",
                                "fontSize": "27px", "fontWeight": "bold",
                                "marginTop": "-1rem"}

today = datetime.date.today()
monday = today - datetime.timedelta(days=today.weekday())
last_week_monday = str(monday - datetime.timedelta(days=7))
last_week_friday = str(monday - datetime.timedelta(days=3))

format_last_week_monday = str(datetime.datetime.strptime(last_week_monday, "%Y-%m-%d").strftime("%d/%m/%Y"))
format_last_week_friday = str(datetime.datetime.strptime(last_week_friday, "%Y-%m-%d").strftime("%d/%m/%Y"))

outcome_data_last_week_df = get_data_from_table("conversation_outcome", last_week_monday, last_week_friday)
last_week_conversations = get_number_of_conversation(outcome_data_last_week_df)
# last_week_user = get_number_of_user(outcome_data_last_week_df)
last_week_success_rate = get_success_rate(outcome_data_last_week_df)

outcome_data = get_data_from_table("conversation_outcome")
month_list, conversations_by_month, success_rate_over_month = get_number_of_conversation_every_month(outcome_data)

# BAR CHART CONVERSATION BY MONTH
conversation_by_month_fig = bar_conversation_by_month(month_list, conversations_by_month)

# LINE CHART SUCCESS RATE OVER MONTH
success_rate_over_month_fig = line_success_rate_over_month(month_list, success_rate_over_month)

app.layout = html.Div(children=[
    html.Div(
        id="sidebar",
        className="sidebar",
        children=[
            html.H5(
                style={"color": "white"},
                children=["SALESBOT"]
            ),
            html.A(id="a1_title_sidebar", href="#part_1_title", className="title_sidebar",
                   children=["Overall Performance"]),
            html.A(id="a2_title_sidebar", href="#part_2_title", className="title_sidebar",
                   children=["Bot performance by Outcomes"]),
            html.A(id="a3_title_sidebar", href="#part_3_title", className="title_sidebar",
                   children=["Bot performance by Use cases"]),
            html.A(id="a4_title_sidebar", href="#part_4_title", className="title_sidebar",
                   children=["Outcome of each Use case"]),
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
                children=["Statistics by last week: " + format_last_week_monday + " - " + format_last_week_friday],
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
                                            html.P("Conversations", style={"display": "block", "paddingLeft": "7rem",
                                                                           "fontSize": "19px", "marginTop": "-4rem"}),
                                            html.P(str(last_week_conversations),
                                                   style={"display": "block", "paddingLeft": "7rem",
                                                          "fontSize": "27px", "fontWeight": "bold",
                                                          "marginTop": "-1rem"}),
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
                                                     className="sub_basic_metrics_img",
                                                     style={"padding-top": "2.5rem"}),
                                            html.P("Users", style={"display": "block", "paddingLeft": "7rem",
                                                                   "fontSize": "19px", "marginTop": "-4rem"}),
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
                                            html.P("Success Rate", style={"display": "block", "paddingLeft": "7rem",
                                                                          "fontSize": "19px", "marginTop": "-4rem"}),
                                            html.P(last_week_success_rate,
                                                   style={"display": "block", "paddingLeft": "7rem",
                                                          "fontSize": "27px", "fontWeight": "bold",
                                                          "marginTop": "-1rem"}),
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
                                className="sub_basic_metrics metrics-graph",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            # html.Img(src="assets/icon/conversation_icon.png", className="sub_basic_metrics_img"),
                                            html.Div(
                                                style={"position": "relative", "top": "0.6rem"},
                                                children=[html.P("Conversations by month"), ],
                                            ),
                                            html.Hr(),
                                            html.Div(
                                                className="line-3-graph",
                                                children=[
                                                    dcc.Graph(
                                                        id='conversation_by_month_fig',
                                                        figure=conversation_by_month_fig
                                                    )
                                                ]
                                            ),

                                        ]
                                    )
                                ]
                            ),
                        ]
                    ),
                    html.Div(
                        className="col-md-4",
                        # style={"marginLeft": "-0.3rem"},
                        children=[
                            html.Div(
                                id="no_users_by_month",
                                # style={"marginRight": "-8px", "marginLeft": "-4px"},
                                className="sub_basic_metrics metrics-graph",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.Div(
                                                style={"position": "relative", "top": "0.6rem"},
                                                children=[html.P("Users by month"), ],
                                            ),
                                            html.Hr(),

                                        ]
                                    )
                                ]
                            ),
                        ]
                    ),
                    html.Div(
                        className="col-md-4",
                        # style={"marginLeft": "-0.3rem"},
                        children=[
                            html.Div(
                                id="success_rate_by_month",
                                className="sub_basic_metrics metrics-graph",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.Div(
                                                style={"position": "relative", "top": "0.6rem"},
                                                children=[html.P("Success rate by month"), ],
                                            ),
                                            html.Hr(),
                                            html.Div(
                                                className="line-3-graph",
                                                children=[
                                                    dcc.Graph(
                                                        id='success_rate_over_month_fig',
                                                        figure=success_rate_over_month_fig
                                                    )
                                                ]
                                            ),

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
                        initial_visible_month=dt(2020, 8, 1),
                        display_format='D/M/Y',
                        placeholder='Start date',
                    ),
                    dcc.DatePickerSingle(
                        style={"paddingLeft": "0.8%", "paddingRight": "1%"},
                        id='my_date_picker_end',
                        min_date_allowed=dt(2020, 1, 1),
                        max_date_allowed=dt(2021, 12, 31),
                        initial_visible_month=dt(2020, 8, 31),
                        display_format='D/M/Y',
                        placeholder='End date',
                    ),
                    html.Button('Run', id='run-analytics',
                                style={"borderRadius": "4px", "backgroundColor": "#448efc", "color": "white",
                                       "width": "3%", "height": "2rem", "borderStyle": "hidden", "fontSize": "12px"}, ),
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
                                            html.P("Conversations", style={"display": "block", "paddingLeft": "7rem",
                                                                           "fontSize": "19px", "marginTop": "-4rem"}),
                                            html.Div(id="no_conversations_in_period_text", ),
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
                                                     className="sub_basic_metrics_img",
                                                     style={"padding-top": "2.5rem"}),
                                            html.P("Users", style={"display": "block", "paddingLeft": "7rem",
                                                                   "fontSize": "19px", "marginTop": "-4rem"}),
                                            html.Div(id="no_users_in_period_text", ),
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
                                            html.P("Success Rate", style={"display": "block", "paddingLeft": "7rem",
                                                                          "fontSize": "19px", "marginTop": "-4rem"}),
                                            html.Div(id="success_rate_in_period_text", ),
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
                                        style={"position": "relative", "top": "1.1rem", "left": "1.25rem",
                                               "fontSize": "19px", "marginBottom": "1.5rem"},
                                        children=[
                                            html.P("Number of Outcomes")
                                        ]
                                    ),
                                    html.Hr(),
                                    html.Div(
                                        className="line-2-graph",
                                        id="no_outcome_bar_fig"
                                    ),
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        className="col-md-6",
                        children=[
                            html.Div(
                                id="percent_outcome_pie",
                                style={"marginLeft": "3%"},
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        style={"position": "relative", "top": "1.1rem", "left": "1.25rem",
                                               "fontSize": "19px", "marginBottom": "1.5rem"},
                                        children=[
                                            html.P("Percentages of Outcomes")
                                        ]
                                    ),
                                    html.Hr(),
                                    html.Div(
                                        className="line-2-graph",
                                        id="percent_outcome_pie_fig"
                                    ),
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
                                            html.Div(
                                                className="col-md-12",
                                                style={"position": "relative", "top": "1.1rem", "left": "1.25rem",
                                                       "fontSize": "19px", "marginBottom": "1.5rem"},
                                                children=[
                                                    html.P("Number of Use cases")
                                                ]
                                            ),
                                            html.Hr(),
                                            html.Div(
                                                className="line-2-graph",
                                                id="no_usecase_bar_fig"
                                            ),
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
                                id="percent_usecase_pie",
                                style={"marginLeft": "3%"},
                                className="sub_basic_metrics",
                                children=[
                                    html.Div(
                                        className="col-md-12",
                                        children=[
                                            html.Div(
                                                className="col-md-12",
                                                style={"position": "relative", "top": "1.1rem", "left": "1.25rem",
                                                       "fontSize": "19px", "marginBottom": "1.5rem"},
                                                children=[
                                                    html.P("Percentages of Use cases")
                                                ]
                                            ),
                                            html.Hr(),
                                            html.Div(
                                                className="line-2-graph",
                                                id="percent_usecase_pie_fig"
                                            ),
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
                        # className="outcome-of-usecase-text",
                        children=[
                            html.Div(
                                id="outcome_of_usecase_1_text",
                                children=["Use case S1"],
                            ),
                            html.Div(
                                id="outcome_of_usecase_2_text",
                                children=["Use case S2"],
                            ),
                        ]
                    ),

                    html.Div(
                        id="first_2_uc",
                        className="basic-metrics",
                        children=[
                            html.Div(
                                className="col-md-6 basic-metrics",
                                children=[
                                    html.Div(
                                        className="col-md-6 first-col",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.Div(
                                                                className='outcome_of_uc_sub_title',
                                                                children=[html.P("Number of outcomes"), ],
                                                            ),
                                                            html.Hr(),
                                                            html.Div(
                                                                id="no_outcome_of_uc1_bar"
                                                            ),
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        className="col-md-6 second-col",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.Div(
                                                                className='outcome_of_uc_sub_title',
                                                                children=[html.P("Percentages of outcomes"), ],
                                                            ),
                                                            html.Hr(),
                                                            html.Div(
                                                                id="percent_outcome_of_uc1_pie",
                                                                className="percent-outcome-of-uc-pie"
                                                            ),
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
                                        className="col-md-6 third-col",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.Div(
                                                                className='outcome_of_uc_sub_title',
                                                                children=[html.P("Number of outcomes"), ],
                                                            ),
                                                            html.Hr(),
                                                            html.Div(
                                                                id="no_outcome_of_uc2_bar"
                                                            ),
                                                        ]
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        className="col-md-6 fourth-col",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.Div(
                                                                className='outcome_of_uc_sub_title',
                                                                children=[html.P("Percentages of outcomes"), ],
                                                            ),
                                                            html.Hr(),
                                                            html.Div(
                                                                id="percent_outcome_of_uc2_pie",
                                                                className="percent-outcome-of-uc-pie"
                                                            ),
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
                        className="outcome-of-usecase-text",
                        children=[
                            html.Div(
                                className="big-column-1-text",
                                children=["Use case S3"],
                            ),
                            html.Div(
                                className="big-column-2-text",
                                children=["Use case S4"],
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
                                        className="col-md-6 first-col",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.Div(
                                                                className='outcome_of_uc_sub_title',
                                                                children=[html.P("Number of outcomes"), ],
                                                            ),
                                                            html.Hr(),
                                                            html.Div(
                                                                id="no_outcome_of_uc3_bar"
                                                            ),
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        className="col-md-6 second-col",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.Div(
                                                                className='outcome_of_uc_sub_title',
                                                                children=[html.P("Percentages of outcomes"), ],
                                                            ),
                                                            html.Hr(),
                                                            html.Div(
                                                                id="percent_outcome_of_uc3_pie",
                                                                className="percent-outcome-of-uc-pie"
                                                            ),
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
                                        className="col-md-6 third-col",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.Div(
                                                                className='outcome_of_uc_sub_title',
                                                                children=[html.P("Number of outcomes"), ],
                                                            ),
                                                            html.Hr(),
                                                            html.Div(
                                                                id="no_outcome_of_uc4_bar"
                                                            ),
                                                        ]
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        className="col-md-6 fourth-col",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.Div(
                                                                className='outcome_of_uc_sub_title',
                                                                children=[html.P("Percentages of outcomes"), ],
                                                            ),
                                                            html.Hr(),
                                                            html.Div(
                                                                id="percent_outcome_of_uc4_pie",
                                                                className="percent-outcome-of-uc-pie"
                                                            ),
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
                        className="outcome-of-usecase-text-2",
                        children=[
                            html.Div(
                                className="big-column-1-text",
                                children=["Use case S5"],
                            ),
                            html.Div(
                                className="big-column-2-text",
                                children=["Use case S8"],
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
                                        className="col-md-6 first-col",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.Div(
                                                                className='outcome_of_uc_sub_title',
                                                                children=[html.P("Number of outcomes"), ],
                                                            ),
                                                            html.Hr(),
                                                            html.Div(
                                                                id="no_outcome_of_uc5_bar"
                                                            ),
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        className="col-md-6 second-col",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.Div(
                                                                className='outcome_of_uc_sub_title',
                                                                children=[html.P("Percentages of outcomes"), ],
                                                            ),
                                                            html.Hr(),
                                                            html.Div(
                                                                id="percent_outcome_of_uc5_pie",
                                                                className="percent-outcome-of-uc-pie"
                                                            ),
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
                                        className="col-md-6 third-col",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.Div(
                                                                className='outcome_of_uc_sub_title',
                                                                children=[html.P("Number of outcomes"), ],
                                                            ),
                                                            html.Hr(),
                                                            html.Div(
                                                                id="no_outcome_of_uc8_bar"
                                                            ),
                                                        ]
                                                    )
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        className="col-md-6 fourth-col",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.Div(
                                                                className='outcome_of_uc_sub_title',
                                                                children=[html.P("Percentages of outcomes"), ],
                                                            ),
                                                            html.Hr(),
                                                            html.Div(
                                                                id="percent_outcome_of_uc8_pie",
                                                                className="percent-outcome-of-uc-pie"
                                                            ),
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
                        className="outcome-of-usecase-text-3",
                        children=[
                            html.Div(
                                className="big-column-1-text",
                                children=["Use case S9"],
                            ),
                            # html.Div(
                            #     children=["Use case S2"],
                            # ),
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
                                        className="col-md-6 first-col",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.Div(
                                                                className='outcome_of_uc_sub_title',
                                                                children=[html.P("Number of outcomes"), ],
                                                            ),
                                                            html.Hr(),
                                                            html.Div(
                                                                id="no_outcome_of_uc9_bar"
                                                            ),
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        className="col-md-6 second-col",
                                        children=[
                                            html.Div(
                                                className="sub_basic_metrics",
                                                children=[
                                                    html.Div(
                                                        className="col-md-12",
                                                        children=[
                                                            html.Div(
                                                                className='outcome_of_uc_sub_title',
                                                                children=[html.P("Percentages of outcomes"), ],
                                                            ),
                                                            html.Hr(),
                                                            html.Div(
                                                                id="percent_outcome_of_uc9_pie",
                                                                className="percent-outcome-of-uc-pie"
                                                            ),
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                ]
                            ),
                            # html.Div(
                            #     className="col-md-6 basic-metrics",
                            #     children=[
                            #         html.Div(
                            #             className="col-md-6 third-col",
                            #             children=[
                            #                 html.Div(
                            #                     className="sub_basic_metrics",
                            #                     children=[
                            #                         html.Div(
                            #                             className="col-md-12",
                            #                             children=[
                            #                                 html.P("Number of outcomes")
                            #                             ]
                            #                         )
                            #                     ]
                            #                 ),
                            #             ]
                            #         ),
                            #         html.Div(
                            #             className="col-md-6 fourth-col",
                            #             children=[
                            #                 html.Div(
                            #                     className="sub_basic_metrics",
                            #                     children=[
                            #                         html.Div(
                            #                             className="col-md-12",
                            #                             children=[
                            #                                 html.P("Percentages of outcomes")
                            #                             ]
                            #                         )
                            #                     ]
                            #                 )
                            #             ]
                            #         ),
                            #     ]
                            # ),
                        ]
                    ),
                ]
            ),

            html.Div(id='df-data-outcome', style={'display': 'none'}),
            html.Div(id='df-data-usecase', style={'display': 'none'}),
            html.P(id='custom_from_date_data', style={'display': 'none'}),
            html.P(id='custom_to_date_data', style={'display': 'none'}),
            html.P(id='is-click', style={'display': 'none'}, children=["0"]),

            html.Div(
                id="space_at_the_end",
                style={"paddingBottom": "10px"},
            ),
        ],
    ),

])


# Xu ly kho chon ngay
@app.callback(
    [
        Output(component_id='custom_from_date_data', component_property='children'),
        Output(component_id='custom_to_date_data', component_property='children'),

    ],
    [
        Input('my_date_picker_start', 'date'),
        Input('my_date_picker_end', 'date'),
    ],
)
def set_date_data(start_date, end_date):
    if start_date is not None and end_date is not None:
        return start_date, end_date
    else:
        return "", ""


# Xu ly khi an button Run
@app.callback(
    # [
    # Output(component_id='loading-div', component_property='children'),
    # Output(component_id='loading-div-2', component_property='children'),
    # Output(component_id='is-click', component_property='children'),
    # ],
    Output(component_id='is-click', component_property='children'),

    [
        Input(component_id='run-analytics', component_property='n_clicks')
    ],
    [
        State('custom_from_date_data', 'children'),
        State('custom_to_date_data', 'children'),
        # State('loading-div', 'style'),
        # State('loading-div-2', 'style'),
    ]
)
def show_loading(n_clicks, start_date, end_date):
    if start_date is not None and end_date is not None:
        # spinner = randrange(2)
        # loading_child = html.Div(style={
        #     'display': 'block',
        #     'position': 'fixed',
        #     'top': '0',
        #     'bottom': '0',
        #     'left': '-200',
        #     'right': '-100',
        #     'backgroundColor': '#f9f9f9',
        #     'opacity': '0.8',
        #     'zIndex': '1002',
        #     'width': '2000px',
        # },
        #     children=[html.Img(id="cat_loading_spinner", src=spinner_list[spinner], style={"position": "sticky"})]
        # )
        # display_loading_1 = loading1["display"]
        # display_loading_2 = loading2["display"]
        # if display_loading_1 != "none":
        #     loading_1_child = loading_child
        #     loading_2_child = ""
        #     return loading_1_child, loading_2_child, "1"
        # elif display_loading_2 != "none":
        #     loading_1_child = ""
        #     loading_2_child = loading_child
        #     return loading_1_child, loading_2_child, "1"
        return "1"
    else:
        # return html.Div(style={'display': 'none'}), html.Div(style={'display': 'none'}), "0"
        return "0"


@app.callback(
    [
        Output('df-data-outcome', 'children'),
        Output('df-data-usecase', 'children'),
    ],
    [
        Input('is-click', 'children'),
    ],
    [
        State('custom_from_date_data', 'children'),
        State('custom_to_date_data', 'children'),
    ],
)
def handle_df(is_click, start_date, end_date):
    if is_click == "1" and start_date is not None and end_date is not None:
        df_outcome = get_data_from_table("conversation_outcome", from_date=start_date, to_date=end_date)
        df_usecase = get_data_from_table("conversation_usecase", from_date=start_date, to_date=end_date)
        if len(df_outcome) == 0:
            return None, None
        df_outcome = df_outcome.drop(columns=["_id"])
        df_usecase = df_usecase.drop(columns=["_id"])
        return df_outcome.to_json(date_format='iso', orient='split'), df_usecase.to_json(date_format='iso',
                                                                                         orient='split')
    else:
        return None, None


@app.callback(
    [
        Output("no_conversations_in_period_text", 'children'),
        Output("no_users_in_period_text", 'children'),
        Output("success_rate_in_period_text", 'children'),
        Output("no_outcome_bar_fig", 'children'),
        Output("percent_outcome_pie_fig", 'children'),
        Output("no_usecase_bar_fig", 'children'),
        Output("percent_usecase_pie_fig", 'children'),
        Output("no_outcome_of_uc1_bar", 'children'),
        Output("percent_outcome_of_uc1_pie", 'children'),
        Output("no_outcome_of_uc2_bar", 'children'),
        Output("percent_outcome_of_uc2_pie", 'children'),
        Output("no_outcome_of_uc3_bar", 'children'),
        Output("percent_outcome_of_uc3_pie", 'children'),
        Output("no_outcome_of_uc4_bar", 'children'),
        Output("percent_outcome_of_uc4_pie", 'children'),
        Output("no_outcome_of_uc5_bar", 'children'),
        Output("percent_outcome_of_uc5_pie", 'children'),
        Output("no_outcome_of_uc8_bar", 'children'),
        Output("percent_outcome_of_uc8_pie", 'children'),
        Output("no_outcome_of_uc9_bar", 'children'),
        Output("percent_outcome_of_uc9_pie", 'children'),

    ],

    [
        Input('df-data-outcome', 'children'),
        Input('df-data-usecase', 'children')
    ],
    # [
    #     State('loading-div', 'style'),
    #     State('loading-div-2', 'style')
    # ]
)
def update_output(df_outcome, df_usecase):
    if df_outcome is not None:
        df_outcome = pd.read_json(df_outcome, orient="split")
        df_usecase = pd.read_json(df_usecase, orient="split")

        # no_conversation, users, success rate in period
        no_conversations_in_period = get_number_of_conversation(df_outcome)
        # no_users_in_period = get_number_of_user(df)
        success_rate_in_period = get_success_rate(df_outcome)

        no_conversations_in_period_text = html.P(str(no_conversations_in_period), style=metrics_in_period_text_style)
        no_users_in_period_text = html.P("2", style=metrics_in_period_text_style)
        success_rate_in_period_text = html.P(str(success_rate_in_period), style=metrics_in_period_text_style)

        # NUMBER OF EACH OUTCOME IN PERIOD
        number_of_outcome_dict = get_number_of_each_outcome(df_outcome)
        bar_bot_performance_by_outcome_fig = bar_bot_performance_by_outcome(number_of_outcome_dict)
        pie_bot_performance_by_outcome_fig = pie_bot_performance_by_outcome(number_of_outcome_dict)

        # NUMBER OF EACH USECASE IN PERIOD
        number_of_usecase_dict = get_number_of_each_usecase(df_usecase)
        bar_bot_performance_by_usecase_fig = bar_bot_performance_by_usecase(number_of_usecase_dict)
        pie_bot_performance_by_usecase_fig = pie_bot_performance_by_usecase(number_of_usecase_dict)

        # NUMBER OF OUTCOME OF EACH USECASE
        graph_list = []
        number_of_outcome_of_each_usecase_dict = get_number_of_outcome_of_each_usecase(df_outcome, df_usecase)
        for uc in uc_list[:-1]:
            bar_number_of_outcome_of_uc_fig = bar_number_of_outcome_of_usecase(number_of_outcome_of_each_usecase_dict,
                                                                               uc)
            pie_percent_of_outcome_of_uc_fig = pie_percent_of_outcome_of_usecase(number_of_outcome_of_each_usecase_dict,
                                                                                 uc)
            graph_list.append(bar_number_of_outcome_of_uc_fig)
            graph_list.append(pie_percent_of_outcome_of_uc_fig)

        return [no_conversations_in_period_text, no_users_in_period_text, success_rate_in_period_text,
                bar_bot_performance_by_outcome_fig, pie_bot_performance_by_outcome_fig,
                bar_bot_performance_by_usecase_fig, pie_bot_performance_by_usecase_fig] + graph_list
    else:
        no_conversations_in_period_text = html.P("'", style=metrics_in_period_text_style)
        no_users_in_period_text = html.P("'", style=metrics_in_period_text_style)
        success_rate_in_period_text = html.P("'", style=metrics_in_period_text_style)
        return [no_conversations_in_period_text, no_users_in_period_text, success_rate_in_period_text,
                "", "",
                "", ""] + [""] * len(uc_list[:-1]) * 2


if __name__ == '__main__':
    app.run_server(debug=True)
