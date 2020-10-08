import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
from utils.helper_2 import *

layout = go.Layout(
    margin=go.layout.Margin(
        l=0,  # left margin
        r=0,  # right margin
        b=0,  # bottom margin
        t=0,  # top margin
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

outcome_list = ["thank", "shipping_order", "handover_to_inbox", "silence", "other"]
uc_list = ["uc_s1", "uc_s2", "uc_s3", "uc_s4", "uc_s5", "uc_s8", "uc_s9", "other"]


def bar_conversation_by_month(month_list, conversations_by_month):
    month_list = month_list[4:-1]
    conversations_by_month = conversations_by_month[4:-1]
    conversation_by_month_fig = go.Figure(
        data=[go.Bar(x=month_list, y=conversations_by_month, text=conversations_by_month)], layout=layout)
    conversation_by_month_fig.update_layout(width=320, height=215,
                                            yaxis=dict(range=[0, max(conversations_by_month) + 25], ticks="outside", tickcolor='white', ticklen=7, ),
                                            xaxis=dict(ticks="outside", tickcolor='white', ticklen=5, ))
    conversation_by_month_fig.update_traces(marker_color='#529af2', textposition='outside', textfont_size=10)
    conversation_by_month_fig.update_xaxes(showline=True, linewidth=2, linecolor='#959595', tickfont=dict(size=9))
    conversation_by_month_fig.update_yaxes(showline=True, linewidth=2, linecolor='#959595', gridcolor='#f3f3f3',
                                           tickfont=dict(size=9))
    return conversation_by_month_fig


def bar_user_by_month(month_list, users_by_month):
    month_list = month_list[4:-1]
    users_by_month = users_by_month[4:-1]
    bar_user_by_month_fig = go.Figure(
        data=[go.Bar(x=month_list, y=users_by_month, text=users_by_month)], layout=layout)
    bar_user_by_month_fig.update_layout(width=320, height=215,
                                            yaxis=dict(range=[0, max(users_by_month) + 25], ticks="outside", tickcolor='white', ticklen=7, ),
                                            xaxis=dict(ticks="outside", tickcolor='white', ticklen=5, ))
    bar_user_by_month_fig.update_traces(marker_color='#529af2', textposition='outside', textfont_size=10)
    bar_user_by_month_fig.update_xaxes(showline=True, linewidth=2, linecolor='#959595', tickfont=dict(size=9))
    bar_user_by_month_fig.update_yaxes(showline=True, linewidth=2, linecolor='#959595', gridcolor='#f3f3f3',
                                           tickfont=dict(size=9))
    return bar_user_by_month_fig


def line_success_rate_over_month(month_list, success_rate_over_month):
    month_list = month_list[4:-1]
    success_rate_over_month = success_rate_over_month[4:-1]
    success_rate_over_month_fig = go.Figure(layout=layout)
    success_rate_over_month_fig.add_trace(go.Scatter(x=month_list, y=success_rate_over_month,
                                                     text=[str(x) + "%" for x in success_rate_over_month],
                                                     marker=dict(
                                                         color='#ffffff',
                                                         size=6,
                                                         line=dict(
                                                             color='#529af2',
                                                             width=1
                                                         )
                                                     ),
                                                     line=dict(color="#529af2", width=1),
                                                     mode='lines+markers+text',
                                                     name='lines+markers+text'))

    success_rate_over_month_fig.update_traces(textposition='top center', textfont_size=10)

    success_rate_over_month_fig.update_layout(width=320, height=215,
                                              yaxis=dict(range=[-10, max(success_rate_over_month) + 25])
                                              )
    success_rate_over_month_fig.update_xaxes(showline=True, linewidth=2, linecolor='#959595', tickfont=dict(size=9))
    success_rate_over_month_fig.update_yaxes(showline=True, linewidth=2, linecolor='#959595', gridcolor='#f3f3f3',
                                             tickfont=dict(size=9))

    return success_rate_over_month_fig


def bar_bot_performance_by_outcome(outcomes_dict):
    outcome_value = [outcomes_dict[x] for x in outcome_list]
    bar_bot_performance_by_outcome_fig = go.Figure(layout=layout)
    bar_bot_performance_by_outcome_fig.add_trace(go.Bar(
        x=["Thanks", "Shipping/Order", "Handover", "Silence", "Other"],
        y=outcome_value,
        width=[0.6] * len(outcome_value),
        text=outcome_value))
    bar_bot_performance_by_outcome_fig.update_layout(width=300, height=150,
                                                     yaxis=dict(ticks="outside", tickcolor='white', ticklen=10,
                                                                range=[0, max(outcome_value) + 30, ]),
                                                     xaxis=dict(ticks="outside", tickcolor='white', ticklen=5, ))

    bar_bot_performance_by_outcome_fig.update_traces(marker_color='#529af2', textposition='outside', textfont_size=11)
    bar_bot_performance_by_outcome_fig.update_xaxes(showline=True, linewidth=2, linecolor='#959595',
                                                    tickfont=dict(size=11))
    bar_bot_performance_by_outcome_fig.update_yaxes(showline=True, linewidth=2, linecolor='#959595',
                                                    gridcolor='#f3f3f3', tickfont=dict(size=11))

    fig = dcc.Graph(
        id='bar_bot_performance_by_outcome_fig',
        figure=bar_bot_performance_by_outcome_fig,
        style={"height": "75%"},
        responsive=True
    )
    return fig


def pie_bot_performance_by_outcome(outcomes_dict):
    outcome_value = [outcomes_dict[x] for x in outcome_list]
    pie_bot_performance_by_outcome_fig = go.Figure(layout=layout)
    pie_bot_performance_by_outcome_fig.add_trace(go.Pie(
        labels=["Thanks", "Shipping/Order", "Handover", "Silence", "Other"],
        values=outcome_value,
        marker=dict(
            colors=["#7b92d0", "#34a853", "#ea4235", "#fabd03", "#ff6d00"],
            line=dict(color='#f9f9f9', width=1)
        ),
        direction="clockwise",
        sort=False,
        hoverinfo='label+value',
        textinfo='label+percent',
        text=outcome_value,
        textfont_size=11,
        insidetextorientation='horizontal',
    ))
    pie_bot_performance_by_outcome_fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=1.7,
        font=dict(
            size=11,
        ),
    ))

    pie_bot_performance_by_outcome_fig.update_layout(width=450, height=280)

    fig = dcc.Graph(
        id='pie_bot_performance_by_outcome_fig',
        figure=pie_bot_performance_by_outcome_fig,
        responsive=True,
        style={"height": "75%"},
    )
    return fig


def bar_bot_performance_by_usecase(usecase_dict):
    usecase_value = [usecase_dict[x] for x in uc_list]
    bar_bot_performance_by_usecase_fig = go.Figure(layout=layout)
    bar_bot_performance_by_usecase_fig.add_trace(go.Bar(
        x=["UC-S1", "UC-S2", "UC-S3", "UC-S4", "UC-S5", "UC-S8", "UC-S9", "Other"],
        y=usecase_value,
        width=[0.6] * len(usecase_value),
        text=usecase_value))
    bar_bot_performance_by_usecase_fig.update_layout(width=410, height=240,
                                                     yaxis=dict(ticks="outside", tickcolor='white', ticklen=10,
                                                                range=[0, max(usecase_value) + 10]),
                                                     xaxis=dict(ticks="outside", tickcolor='white', ticklen=5, ))
    bar_bot_performance_by_usecase_fig.update_traces(marker_color='#529af2', textposition='outside', textfont_size=11)
    bar_bot_performance_by_usecase_fig.update_xaxes(showline=True, linewidth=2, linecolor='#959595',
                                                    tickfont=dict(size=11))
    bar_bot_performance_by_usecase_fig.update_yaxes(showline=True, linewidth=2, linecolor='#959595',
                                                    gridcolor='#f3f3f3', tickfont=dict(size=11))

    fig = dcc.Graph(
        id='bar_bot_performance_by_usecase_fig',
        figure=bar_bot_performance_by_usecase_fig,
        style={"height": "75%"},
        responsive=True,

    )
    return fig


def pie_bot_performance_by_usecase(usecase_dict):
    usecase_value = [usecase_dict[x] for x in uc_list]
    pie_bot_performance_by_usecase_fig = go.Figure(layout=layout)
    pie_bot_performance_by_usecase_fig.add_trace(go.Pie(
        labels=["UC-S1", "UC-S2", "UC-S3", "UC-S4", "UC-S5", "UC-S8", "UC-S9", "Other"],
        values=usecase_value,
        marker=dict(
            # colors=["#7b92d0", "#34a853", "#ea4235", "#fabd03", "#ff6d00"],
            line=dict(color='#f9f9f9', width=1)
        ),
        direction="clockwise",
        sort=False,
        hoverinfo='label+value',
        textinfo='label+percent',
        text=usecase_value,
        textfont_size=11,
        insidetextorientation='horizontal',
    ))
    pie_bot_performance_by_usecase_fig.update_traces(textposition='auto')

    pie_bot_performance_by_usecase_fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=1.7,
        font=dict(
            size=11,
        ),
    ))

    pie_bot_performance_by_usecase_fig.update_layout(width=450, height=280)

    fig = dcc.Graph(
        id='pie_bot_performance_by_usecase_fig',
        figure=pie_bot_performance_by_usecase_fig,
        responsive=True,
        style={"height": "75%"},
    )
    return fig


def bar_number_of_outcome_of_usecase(number_of_outcome_of_each_usecase_dict, uc):
    outcome_of_uc = number_of_outcome_of_each_usecase_dict[uc]
    outcome_value = [outcome_of_uc[x] for x in outcome_list]
    bar_number_of_outcome_of_usecase_fig = go.Figure(layout=layout)

    bar_number_of_outcome_of_usecase_fig.add_trace(go.Bar(
        x=["Thanks", "Shipping/Order", "Handover", "Silence", "Other"],
        y=outcome_value,
        # width=[0.6] * len(outcome_value),
        text=outcome_value))

    bar_number_of_outcome_of_usecase_fig.update_layout(width=220, height=125,
                                                       yaxis=dict(ticks="outside", tickcolor='white', ticklen=10,
                                                                  range=[0, max(outcome_value) + 10, ]),
                                                       xaxis=dict(ticks="outside", tickcolor='white', ticklen=5, ))

    bar_number_of_outcome_of_usecase_fig.update_traces(marker_color='#529af2', textposition='outside', textfont_size=9)
    bar_number_of_outcome_of_usecase_fig.update_xaxes(showline=True, linewidth=2, linecolor='#959595',
                                                      tickfont=dict(size=6.5))
    bar_number_of_outcome_of_usecase_fig.update_yaxes(showline=True, linewidth=2, linecolor='#959595',
                                                      gridcolor='#f3f3f3', tickfont=dict(size=6.5))

    fig = dcc.Graph(
        id='bar_number_of_outcome_of_' + str(uc) + '_fig',
        figure=bar_number_of_outcome_of_usecase_fig,
        responsive=True,
        style={"height": "75%"},
    )
    return fig


def pie_percent_of_outcome_of_usecase(number_of_outcome_of_each_usecase_dict, uc):
    outcome_of_uc = number_of_outcome_of_each_usecase_dict[uc]
    outcome_value = [outcome_of_uc[x] for x in outcome_list]

    pie_percent_of_outcome_of_usecase_fig = go.Figure(layout=layout)
    pie_percent_of_outcome_of_usecase_fig.add_trace(go.Pie(
        labels=["Thanks", "Shipping/Order", "Handover", "Silence", "Other"],
        values=outcome_value,
        marker=dict(
            colors=["#7b92d0", "#34a853", "#ea4235", "#fabd03", "#ff6d00"],
            line=dict(color='#f9f9f9', width=1)
        ),
        direction="clockwise",
        sort=False,
        hoverinfo='label+value',
        textinfo='label+percent',
        text=outcome_value,
        textfont_size=8,
        insidetextorientation='horizontal',
    ))

    pie_percent_of_outcome_of_usecase_fig.update_layout(legend=dict(

        yanchor="top",
        y=0.99,
        xanchor="right",
        x=2.5,
        font=dict(
            size=5,
        ),
    ))
    pie_percent_of_outcome_of_usecase_fig.update_layout(width=210, height=150)

    fig = dcc.Graph(
        id='pie_percent_of_outcome_of_' + str(uc) + '_fig',
        figure=pie_percent_of_outcome_of_usecase_fig,
        responsive=True,
        style={"height": "104%"},
    )
    return fig


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


def generate_table(db_name, conv_id_list):
    if len(conv_id_list) == 0:
        return ""
    df = get_data_from_table_by_conv_id(db_name, conv_id_list)
    # df.insert(list(df.columns).index("created_time") + 1, "created_time_bot", "")
    # df = reformat_df_output_for_table(df)

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
            id='table',
            # page_action="native",

            style_header={
                'backgroundColor': '#448efc',
                'color': 'white',
                'fontWeight': 'bold',
                'font_size': '0.7rem',
                'minHeight': '2.7rem', 'height': '2.7rem', 'maxHeight': "2.7rem",
            },

            style_data={  # style cho ca header va cell
                'whiteSpace': 'normal',
                # 'height': 'auto',
            },
            style_cell={
                'textAlign': 'left',
                'minWidth': '0.5rem', 'width': '0.5rem', 'maxWidth': "0.5rem",
                'font_size': '0.6rem',
                'minHeight': '2.9rem', 'height': '2.9rem', 'maxHeight': "2.9rem",

            },

            tooltip_data=[  # hover  data
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('rows')
            ],
            tooltip_duration=None,

            style_table={
                'overflowY': 'auto',
                'minHeight': '23rem', 'height': '23rem', 'maxHeight': "23rem",
            },
            style_cell_conditional=
            [
                {
                    'if': {'column_id': c},
                    'minWidth': '3.75rem',
                    'width': '3.75rem',
                    'maxWidth': '3.75rem',
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
                    'minWidth': '7rem',
                    'width': '7rem',
                    'maxWidth': '7rem'
                } for x in ["timestamp"]
            ] +
            [
                {
                    'if': {'column_id': x},
                    'minWidth': '6rem',
                    'width': '6rem',
                    'maxWidth': '6rem'
                } for x in ["conv_id"]
            ] +
            [
                {
                    'if': {'column_id': x},
                    'minWidth': '13rem',
                    'width': '13rem',
                    'maxWidth': '13rem',
                } for x in ["input_text", "bot_text"]
            ] +
            [
                {
                    'if': {'column_id': x},
                    'minWidth': '7rem',
                    'width': '7rem',
                    'maxWidth': '7rem',

                } for x in ["intent", "entities"]
            ] +
            [
                {
                    'if': {'column_id': x},
                    'minWidth': '80px',
                    'width': '80px',
                    'maxWidth': '80px',

                } for x in ["outcome"]
            ],
            fixed_rows={'headers': True},
            style_as_list_view=True,
            data=df.to_dict('records'),

            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
    ])
