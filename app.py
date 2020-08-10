import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
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

logging.basicConfig(filename="logging_data/rasa_chatlog_processor_log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

month_dict = {"1": "January", "2": "February", "3": "March", "4": "April", "5": "May", "6": "June", "7": "July",
              "8": "August",
              "9": "September", "10": "October", "11": "November", "12": "December"}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
suppress_callback_exceptions = True
app = dash.Dash(__name__,
                # external_stylesheets=external_stylesheets
                external_stylesheets=[dbc.themes.BOOTSTRAP]
                )
server = app.server
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
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=dt(2020, 1, 1),
            max_date_allowed=dt(2020, 12, 31),
            initial_visible_month=dt(2020, 7, 1),
            start_date=dt(2020, 7, 1).date(),
            end_date=dt(2020, 7, 31).date()
        ),
        html.Div(
            className="d-flex flex-wrap",
            children=[
                html.Div(id='outcome_proportion-in-conversations', className="col-md-12 h-50"),
            ]
        ),

        dcc.Tabs(
            id="tab_parent",
            value="shipping",
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
        html.Div(
            className="d-flex flex-wrap",
            children=[
                html.Div(id='uc-proportion-in-month', className="col-md-12 h-50"),
            ]
        ),
        dcc.Tabs(
            id="uc_tab_parent",
            value="uc_s1",
            children=[
                dcc.Tab(id="uc_s1", label='UC_S1', value="uc_s1", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='uc-s1'), ]
                        ),
                dcc.Tab(id="uc_s2", label='UC_S2', value="uc_s2", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='uc-s2'), ]
                        ),
                dcc.Tab(id="uc_s31", label='UC_S31', value="uc_s31", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='uc-s31'), ]
                        ),
                dcc.Tab(id="uc_s32", label='UC_S32', value="uc_s32", style=tab_style, selected_style=tab_selected_style,
                        children=[html.Div(id='uc-s32'), ]
                        ),
            ]
        ),
        html.Div(
            className="d-flex flex-wrap",
            children=[
                html.Div(id='outcome-uc1-pie', className="col-md-6 h-50"),
                html.Div(id='outcome-uc2-pie', className="col-md-6 h-50"),
            ]
        ),
        html.Div(
            className="d-flex flex-wrap",
            children=[
                html.Div(id='outcome-uc31-pie', className="col-md-6 h-50"),
                html.Div(id='outcome-uc32-pie', className="col-md-6 h-50"),
            ]
        ),
        html.Div(id='df-data', style={'display': 'none'}),
        html.P(id='custom-from-date-data', style={'display': 'none'}),
        html.P(id='custom-to-date-data', style={'display': 'none'}),

    ])


def create_trace_uc_propotion_in_month(total: int, uc1: int, uc2: int, uc31: int, uc32: int):
    logger.info("Create trace uc proportion in month")

    not_uc1_uc2 = total - uc1 - uc2 - uc31 - uc32
    colors = ['mediumturquoise', 'darkorange', 'lightgreen']
    trace = go.Pie(
        labels=['Other', 'UC S1', 'UC S2', "UC S31", "UC S32"],
        values=[not_uc1_uc2, uc1, uc2, uc31, uc32],
        hoverinfo='label+percent',
        textinfo='label+value+percent',
        textfont_size=15,
        marker=dict(
            colors=plotly.colors.diverging.Portland,
            line=dict(color='#000000', width=1))
    )
    first_pie = html.Div(
        className="six columns chart_div pretty_container",
        children=[
            html.P("Usecases proportion in month"),
            dcc.Graph(
                figure={"data": [trace]},
                style={"height": "90%", "width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return first_pie


def create_trace_outcome_proportion_in_all_conversation(uc_outcome: dict):
    logger.info("Create trace ourcome proportion in all conversation")

    outcome_uc1 = uc_outcome["uc_s1"]
    outcome_uc2 = uc_outcome["uc_s2"]
    outcome_uc31 = uc_outcome["uc_s31"]
    outcome_uc32 = uc_outcome["uc_s32"]
    outcome_other = uc_outcome["other"]

    uc_s1_values = [value for index, value in outcome_uc1.items()]
    uc_s2_values = [value for index, value in outcome_uc2.items()]
    uc_s31_values = [value for index, value in outcome_uc31.items()]
    uc_s32_values = [value for index, value in outcome_uc32.items()]
    uc_other_values = [value for index, value in outcome_other.items()]

    values = [sum(x) for x in zip(uc_s1_values, uc_s2_values, uc_s31_values, uc_s32_values, uc_other_values)]
    trace = go.Pie(
        labels=['thanks', 'shipping', 'handover', "silence", "other", "agree"],
        values=values,
        direction="clockwise",
        sort=False,
        rotation=120,
        hoverinfo='label+percent',
        textinfo='label+value',
        textfont_size=15,
        marker=dict(line=dict(
            color=plotly.colors.diverging.Portland,
            width=1)))
    second_pie = html.Div(
        className="six columns chart_div pretty_container",
        children=[
            html.P("Outcomes proportion in all conversations"),
            dcc.Graph(
                figure={"data": [trace]},
                style={"height": "90%", "width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return second_pie


def create_trace_outcome_uc(uc_outcome: dict, key: str, name: str, title: str):
    logger.info("Create trace ourcome proportion in each use_case")

    outcome_uc = uc_outcome[key]
    values = [value for index, value in outcome_uc.items()]
    labels = ['thanks', 'shipping', 'handover', "silence", "other", "agree"]
    trace_2 = go.Pie(labels=labels, values=values, scalegroup='one',
                     name=name, direction="clockwise", sort=False, rotation=120, hoverinfo='label+percent',
                     textinfo='label+value', textfont_size=15,
                     marker=dict(line=dict(
                         color=plotly.colors.diverging.Portland,
                         width=1)))
    pie = html.Div(
        className="six columns chart_div pretty_container",
        children=[
            html.P(title),
            dcc.Graph(
                figure={"data": [trace_2]},
                style={"height": "90%", "width": "98%"},
                config=dict(displayModeBar=False),
            ),
        ],
    ),
    return pie


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
    logger.info("Generate table")

    df.insert(list(df.columns).index("created_time") + 1, "created_time_bot", "")
    info_dict = {x: [] for x in list(df.columns)}
    info_dict.pop('turn', None)
    info_dict.pop('message_id', None)
    info_dict.pop('sender', None)
    info_dict.pop('attachments', None)

    user_counter = 0
    bot_counter = 0
    counter = 0
    for row in df.itertuples():
        counter += 1
        user_message = row.user_message
        bot_message = row.bot_message
        if user_message is None or user_message == "None":
            user_message = np.NaN
        if bot_message is None or bot_message == "None":
            bot_message = np.NaN
        if user_message == "user":
            user_counter = 0
            bot_counter += 1
            info_dict["bot_message"].append(bot_message)
            info_dict["created_time_bot"].append(row.created_time)
            use_case = row.use_case
            if "outcome" in info_dict:
                outcome = row.outcome
                if outcome != '':
                    if bot_counter <= 1:
                        info_dict["outcome"].remove('')
                    info_dict["outcome"].append(row.outcome)

            if bot_counter > 1:
                info_dict["conversation_id"].append(row.conversation_id)
                info_dict["user_message"].append(np.NaN)
                info_dict["created_time"].append("")
                info_dict["intent"].append("")
                info_dict["entities"].append("")
                if "outcome" in info_dict and row.outcome == '':
                    info_dict["outcome"].append(row.outcome)

                info_dict["use_case"].append(use_case)
                info_dict["sender_id"].append(row.sender_id)

        elif user_message != "user":
            user_counter += 1
            bot_counter = 0
            info_dict["conversation_id"].append(row.conversation_id)
            info_dict["user_message"].append(user_message)
            info_dict["created_time"].append(row.created_time)
            info_dict["intent"].append(row.intent)
            info_dict["entities"].append(row.entities)
            info_dict["use_case"].append(row.use_case)
            info_dict["sender_id"].append(row.sender_id)
            if "outcome" in info_dict:
                info_dict["outcome"].append(row.outcome)

            if user_counter > 1 or counter == len(df):
                info_dict["bot_message"].append(np.NaN)
                info_dict["created_time_bot"].append("")

            if counter == len(df) and user_counter > 1:
                info_dict["bot_message"].append(np.NaN)
                info_dict["created_time_bot"].append("")

    df = pd.DataFrame.from_dict(info_dict)
    df = df.dropna(subset=["user_message", "bot_message"], how="all")
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
    logger.info("Count each usecase")

    total = len(list(dict.fromkeys(list(df["conversation_id"]))))
    uc_s1 = len(df[df["use_case"] == "uc_s1"])
    uc_s2 = len(df[df["use_case"] == "uc_s2"])
    uc_s31 = len(df[df["use_case"] == "uc_s31"])
    uc_s32 = len(df[df["use_case"] == "uc_s32"])
    return total, uc_s1, uc_s2, uc_s31, uc_s32


def get_number_of_each_outcome_each_uc(df: pd.DataFrame):
    logger.info("Count outcome each use_case")

    """ thank -> shipping -> handover -> silence ->  other -> agree"""
    uc_outcome = {
        "uc_s1": {"thank": 0, "shipping_order": 0, "handover_to_inbox": 0, "silence": 0, "other": 0, "agree": 0},
        "uc_s2": {"thank": 0, "shipping_order": 0, "handover_to_inbox": 0, "silence": 0, "other": 0, "agree": 0},
        "uc_s31": {"thank": 0, "shipping_order": 0, "handover_to_inbox": 0, "silence": 0, "other": 0, "agree": 0},
        "uc_s32": {"thank": 0, "shipping_order": 0, "handover_to_inbox": 0, "silence": 0, "other": 0, "agree": 0},
        "other": {"thank": 0, "shipping_order": 0, "handover_to_inbox": 0, "silence": 0, "other": 0, "agree": 0},
    }
    uc1_uc_2_conversation_id = list(df[(df["use_case"] == "uc_s1") | (df["use_case"] == "uc_s2")]["conversation_id"])
    uc1_uc_2_conversation_id = list(dict.fromkeys(uc1_uc_2_conversation_id))

    conversation_id = list(df["conversation_id"])
    conversation_id = list(dict.fromkeys(conversation_id))

    # for id in uc1_uc_2_conversation_id:
    for id in conversation_id:
        sub_df = df[df["conversation_id"] == id]
        use_case = list(filter(lambda x: x != "", list(sub_df["use_case"])))
        if len(use_case) > 0:
            use_case = use_case[0]
        else:
            use_case = "other"
        outcome = list(filter(lambda x: x != "", list(sub_df["outcome"])))[0]
        uc_outcome[use_case][outcome] += 1
    return uc_outcome


def get_conversation_each_outcome(df: pd.DataFrame):
    logger.info("Get conversation for each outcome")

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


def get_conversation_each_usecase(df: pd.DataFrame):
    logger.info("Get conversation for each use_case")

    column_list = ["conversation_id", "use_case", "outcome", "sender_id", "user_message", "bot_message", "created_time",
                   "intent",
                   "entities"]
    uc1_df = df[df["conversation_id"].isin(list(df[df["use_case"] == "uc_s1"]["conversation_id"]))][column_list]
    uc2_df = df[df["conversation_id"].isin(list(df[df["use_case"] == "uc_s2"]["conversation_id"]))][column_list]
    uc31_df = df[df["conversation_id"].isin(list(df[df["use_case"] == "uc_s31"]["conversation_id"]))][column_list]
    uc32_df = df[df["conversation_id"].isin(list(df[df["use_case"] == "uc_s32"]["conversation_id"]))][column_list]

    # uc1_df.to_csv("output_data/chatlog_rasa/uc1_df.csv", index=False)
    # uc2_df.to_csv("output_data/chatlog_rasa/uc2_df.csv", index=False)
    # uc31_df.to_csv("output_data/chatlog_rasa/uc31_df.csv", index=False)
    # uc32_df.to_csv("output_data/chatlog_rasa/uc32_df.csv", index=False)
    return uc1_df, uc2_df, uc31_df, uc32_df


@app.callback(
    [
        Output(component_id='loading-div', component_property='children'),
        Output(component_id='loading-div-2', component_property='children'),
        Output(component_id='custom-from-date-data', component_property='children'),
        Output(component_id='custom-to-date-data', component_property='children'),

    ],
    [
        Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date'),
        # Input('loading-div', 'style'),
    ],
    [
        State('loading-div', 'style'),
        State('loading-div-2', 'style')
    ]
)
def show_loading(start_date, end_date, loading1, loading2):
    if start_date is not None and end_date is not None:
        loading_child = html.Div(style={
            'display': 'block',
            'position': 'fixed',
            'top': '0',
            'bottom': '0',
            'left': '0',
            'right': '0',
            'backgroundColor': '#fff',
            'opacity': '0.8',
            'zIndex': '1002',
        },
            children=[html.Img(id="cat_loading_spinner", src="assets/cat-spinner.png")]
        )
        display_loading_1 = loading1["display"]
        display_loading_2 = loading2["display"]
        if display_loading_1 != "none":
            loading_1_child = loading_child
            loading_2_child = ""
            return loading_1_child, loading_2_child, start_date, end_date
        elif display_loading_2 != "none":
            loading_1_child = ""
            loading_2_child = loading_child
            return loading_1_child, loading_2_child, start_date, end_date
    else:
        return {'display': 'none'}


@app.callback(
    Output('df-data', 'children'),
    [
        # Input('my-date-picker-range', 'start_date'),
        # Input('my-date-picker-range', 'end_date'),
        Input('custom-from-date-data', 'children'),
        Input('custom-to-date-data', 'children'),
    ],
)
def handle_df(start_date, end_date):
    if start_date is not None and end_date is not None:
        df = get_chatloag_from_db(from_date=start_date, to_date=end_date)
        processor = RasaChalogProcessor()
        df = processor.process_rasa_chatlog("06", "abc", df)
        return df.to_json(date_format='iso', orient='split')
    else:
        return None


@app.callback(
    [
        Output('uc-proportion-in-month', 'children'),
        Output('outcome_proportion-in-conversations', 'children'),
        Output('outcome-uc1-pie', 'children'),
        Output('outcome-uc2-pie', 'children'),
        Output('outcome-uc31-pie', 'children'),
        Output('outcome-uc32-pie', 'children'),
        Output('thank-table', 'children'),
        Output('shipping-table', 'children'),
        Output('handover-table', 'children'),
        Output('silence-table', 'children'),
        Output('other-table', 'children'),
        Output('agree-table', 'children'),
        Output('uc-s1', 'children'),
        Output('uc-s2', 'children'),
        Output('uc-s31', 'children'),
        Output('uc-s32', 'children'),
        Output(component_id='loading-div', component_property='style'),
        Output(component_id='loading-div-2', component_property='style'),
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

        total, uc1, uc2, uc31, uc32 = get_number_of_each_uc(df[["conversation_id", "use_case"]])
        uc_outcome = get_number_of_each_outcome_each_uc(df[["conversation_id", "use_case", "outcome"]])

        uc_proportion_in_month = create_trace_uc_propotion_in_month(total, uc1, uc2, uc31, uc32)
        outcome_proportion_in_conversations = create_trace_outcome_proportion_in_all_conversation(uc_outcome)
        outcome_uc1_pie = create_trace_outcome_uc(uc_outcome, "uc_s1", "UC S1", "Outcomes of UC-S1")
        outcome_uc2_pie = create_trace_outcome_uc(uc_outcome, "uc_s2", "UC S2", "Outcomes of UC-S2")
        outcome_uc31_pie = create_trace_outcome_uc(uc_outcome, "uc_s31", "UC S31", "Outcomes of UC-S31")
        outcome_uc32_pie = create_trace_outcome_uc(uc_outcome, "uc_s32", "UC S32", "Outcomes of UC-S32")
        # fifth_pie =

        thank_df, shipping_order_df, handover_df, silence_df, other_df, agree_df = get_conversation_each_outcome(df[[
            "conversation_id", "use_case", "outcome", "sender_id", "user_message", "bot_message", "created_time",
            "intent", "entities"]])
        thank_df = generate_table(thank_df)
        shipping_order_df = generate_table(shipping_order_df)
        handover_df = generate_table(handover_df)
        silence_df = generate_table(silence_df)
        other_df = generate_table(other_df)
        agree_df = generate_table(agree_df)

        uc1_df, uc2_df, uc31_df, uc32_df = get_conversation_each_usecase(
            df[["conversation_id", "use_case", "outcome", "sender_id", "user_message",
                "bot_message", "created_time", "intent", "entities"]])
        uc1_df = generate_table(uc1_df)
        uc2_df = generate_table(uc2_df)
        uc31_df = generate_table(uc31_df)
        uc32_df = generate_table(uc32_df)

        loading_1_display = ""
        loading_2_display = ""
        if loading1["display"] == "none":
            loading_1_display = {'display': 'block'}
            loading_2_display = {'display': 'none'}
        elif loading2["display"] == "none":
            loading_1_display = {'display': 'none'}
            loading_2_display = {'display': 'block'}

        return uc_proportion_in_month, outcome_proportion_in_conversations, outcome_uc1_pie, outcome_uc2_pie, outcome_uc31_pie, outcome_uc32_pie, \
               thank_df, shipping_order_df, handover_df, silence_df, other_df, agree_df, uc1_df, uc2_df, uc31_df, uc32_df, loading_1_display, loading_2_display
    else:
        return "", "", "", "", "", "", \
               "", "", "", "", "", "", "", "", "", "", {'display': loading1["display"]}, {'display': loading2["display"]}


if __name__ == '__main__':
    app.run_server(debug=True)
