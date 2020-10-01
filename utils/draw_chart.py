import plotly.graph_objects as go

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


def bar_conversation_by_month(month_list, conversations_by_month):
    conversation_by_month_fig = go.Figure(
        data=[go.Bar(x=month_list, y=conversations_by_month, text=conversations_by_month)], layout=layout)
    conversation_by_month_fig.update_layout(width=320, height=215,
                                            yaxis=dict(range=[0, max(conversations_by_month) + 25]))
    conversation_by_month_fig.update_traces(marker_color='#529af2', textposition='outside', textfont_size=10)
    conversation_by_month_fig.update_xaxes(showline=True, linewidth=2, linecolor='#959595', tickfont=dict(size=9))
    conversation_by_month_fig.update_yaxes(showline=True, linewidth=2, linecolor='#959595', gridcolor='#f3f3f3', tickfont=dict(size=9))
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
    success_rate_over_month_fig.update_yaxes(showline=True, linewidth=2, linecolor='#959595', gridcolor='#f3f3f3', tickfont=dict(size=9))

    return success_rate_over_month_fig
