from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

app = Dash(__name__)
server = app.server

df = pd.read_csv('age_0921_for_interactivechart_new.csv')

category_choices = df['Category'].sort_values().unique()
term_choices = df['Term'].sort_values().unique()
cat_to_term = df.groupby('Category')['Term'].unique().transform(list).to_dict()

app.layout = html.Div([
    html.Div([
        html.Div([
            # Category Dropdown
            dcc.Dropdown(
                id='category_id',
                options=[{'label': i, 'value': i} for i in category_choices],
                value=category_choices[0]
            )
        ], style={'width': '20%', 'display': 'inline-block'}),
        html.Div([
            # Term Dropdown which is populated from state dropdown
            dcc.Dropdown(
                id='term_id',
                options=[{'label': i, 'value': i} for i in term_choices],
                value=[''],
                multi=True
            )
        ], style={'width': '20%', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic')

])


@app.callback(
    Output("term_id", "options"),
    Output("term_id", "value"),
    Input("category_id", "value")
)
def set_term_options(selected_cat):
    return (
        [{"label": i, "value": i} for i in cat_to_term[selected_cat]],
        [cat_to_term[selected_cat][0], cat_to_term[selected_cat][1]]
    )


@callback(
    Output('indicator-graphic', 'figure'),
    Input('term_id', 'value')
)
def update_graph(term_id):
    if type(term_id) is str:
        filtered_df = df[df.Term == term_id]

        fig = px.line(filtered_df, x='Age group', y='More Phrase Usage', color='Term', line_shape='spline')

        fig.update_layout(

            xaxis=dict(

                type='category'
            ),
            yaxis_range=[-1.5, 1.5]
        )
        fig.update_yaxes(visible=True, showticklabels=False, color='lightgrey',
                         gridcolor='lightgrey', zeroline=True, zerolinecolor='lightgrey')
        fig.update_xaxes(title="Age",
                         gridcolor='lightgrey', color='lightgrey')
        fig.update_layout(plot_bgcolor='white')
        fig.update_traces(line=dict(width=4))

        return fig

    filtered_df = df[df.Term.isin(term_id)]

    fig = px.line(filtered_df, x='Age group', y='More Phrase Usage', color='Term', line_shape='spline',
                  width=1000, height=750)

    fig.update_layout(
        xaxis=dict(
            type='category'
        ),
        yaxis_range=[-1.5, 1.5]
    )
    fig.update_yaxes(visible=True,
                     labelalias={0: "average", 0.5: '', "1": "85th Percentile", 1.5: '', "−0.5": '',
                                 "−1": "15th Percentile", "−1.5": ''},
                     ticklabelposition="outside top", gridcolor='lightgrey', zeroline=True,
                     zerolinecolor='lightgrey')
    fig.update_xaxes(title="Age", gridcolor='lightgrey')
    fig.update_layout(plot_bgcolor='white')
    fig.update_traces(line=dict(width=4))

    return fig


if __name__ == '__main__':
    app.run(debug=True, port=5001)
