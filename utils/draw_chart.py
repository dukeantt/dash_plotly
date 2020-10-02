import plotly.graph_objects as go
import dash_core_components as dcc

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
    conversation_by_month_fig = go.Figure(
        data=[go.Bar(x=month_list, y=conversations_by_month, text=conversations_by_month)], layout=layout)
    conversation_by_month_fig.update_layout(width=320, height=215,
                                            yaxis=dict(range=[0, max(conversations_by_month) + 25]))
    conversation_by_month_fig.update_traces(marker_color='#529af2', textposition='outside', textfont_size=10)
    conversation_by_month_fig.update_xaxes(showline=True, linewidth=2, linecolor='#959595', tickfont=dict(size=9))
    conversation_by_month_fig.update_yaxes(showline=True, linewidth=2, linecolor='#959595', gridcolor='#f3f3f3',
                                           tickfont=dict(size=9))
    return conversation_by_month_fig


def line_success_rate_over_month(month_list, success_rate_over_month):
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
                                              yaxis=dict(range=[-0.9, max(success_rate_over_month) + 25])
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
    bar_bot_performance_by_outcome_fig.update_layout(width=410, height=240,
                                                     yaxis=dict(ticks="outside", tickcolor='white', ticklen=10, range=[0, max(outcome_value) + 10, ]),
                                                     xaxis=dict(ticks="outside", tickcolor='white', ticklen=5, ))

    bar_bot_performance_by_outcome_fig.update_traces(marker_color='#529af2', textposition='outside', textfont_size=11)
    bar_bot_performance_by_outcome_fig.update_xaxes(showline=True, linewidth=2, linecolor='#959595',
                                                    tickfont=dict(size=11))
    bar_bot_performance_by_outcome_fig.update_yaxes(showline=True, linewidth=2, linecolor='#959595',
                                                    gridcolor='#f3f3f3', tickfont=dict(size=11))

    fig = dcc.Graph(
        id='bar_bot_performance_by_outcome_fig',
        figure=bar_bot_performance_by_outcome_fig
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
        x=1.5,
        font=dict(
            size=11,
        ),
    ))

    pie_bot_performance_by_outcome_fig.update_layout(width=500, height=300)

    fig = dcc.Graph(
        id='pie_bot_performance_by_outcome_fig',
        figure=pie_bot_performance_by_outcome_fig
    )
    return fig


def bar_bot_performance_by_usecase(usecase_dict):
    usecase_value = [usecase_dict[x] for x in uc_list]
    bar_bot_performance_by_usecase_fig = go.Figure(layout=layout)
    bar_bot_performance_by_usecase_fig.add_trace(go.Bar(
        x=["UC-S1", "UC-S2", "UC-S3", "UC-S4", "UC-S5", "UC-S8","UC-S9", "Other"],
        y=usecase_value,
        width=[0.6] * len(usecase_value),
        text=usecase_value))
    bar_bot_performance_by_usecase_fig.update_layout(width=410, height=240,
                                                     yaxis=dict(ticks="outside", tickcolor='white', ticklen=10, range=[0, max(usecase_value) + 10]),
                                                     xaxis=dict(ticks="outside", tickcolor='white', ticklen=5,))
    bar_bot_performance_by_usecase_fig.update_traces(marker_color='#529af2', textposition='outside', textfont_size=11)
    bar_bot_performance_by_usecase_fig.update_xaxes(showline=True, linewidth=2, linecolor='#959595',
                                                    tickfont=dict(size=11))
    bar_bot_performance_by_usecase_fig.update_yaxes(showline=True, linewidth=2, linecolor='#959595',
                                                    gridcolor='#f3f3f3', tickfont=dict(size=11))

    fig = dcc.Graph(
        id='bar_bot_performance_by_usecase_fig',
        figure=bar_bot_performance_by_usecase_fig
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
        x=1.5,
        font=dict(
            size=11,
        ),
    ))

    pie_bot_performance_by_usecase_fig.update_layout(width=500, height=300)

    fig = dcc.Graph(
        id='pie_bot_performance_by_usecase_fig',
        figure=pie_bot_performance_by_usecase_fig
    )
    return fig