
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px

import pandas as pd

app = Dash(__name__)

df = pd.read_csv('/Users/melody/loreal_results/age_0921_for_interactivechart_new.csv')


category_choices = df['Category'].sort_values().unique()
term_choices = df['Term'].sort_values().unique()
cat_to_term = df.groupby('Category')['Term'].unique().agg(list).to_dict()

app.layout = html.Div([
    html.Div([
        html.Div([
            #Category Dropdown
            dcc.Dropdown(
                id='category_id',
                options=[{'label': i, 'value': i} for i in category_choices],
                value=category_choices[0]
            )
        ], style={'width': '20%', 'display': 'inline-block'}),
        html.Div([
            #Term Dropdown which is populated from state dropdown
            dcc.Dropdown(
                id='term_id',
                options=[{'label': i, 'value': i} for i in term_choices],
                value=['"added bonus" (1.80%)'],
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
    # dff = df[df.Category == selected_cat]
    # counties_of_state = [{"label": i, "value": i} for i in cat_to_term[selected_cat]]
    # values_selected = [x['value'] for x in counties_of_state]
    # return counties_of_state, values_selected

    print([{"label": i, "value": i} for i in cat_to_term[selected_cat]])
    print(cat_to_term[selected_cat][0])
    return (
        [{"label": i, "value": i} for i in cat_to_term[selected_cat]],
        cat_to_term[selected_cat][0],
    )

@callback(
    Output('indicator-graphic', 'figure'),
    Input('term_id', 'value')
    )


def update_graph(term_id):
    filtered_df = df[df.Term.isin(term_id)]

    # fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
    #                  size="pop", color="continent", hover_name="country",
    #                  log_x=True, size_max=55)

    fig = px.line(filtered_df, x='Age group', y='Freq', color='Term')

    fig.update_layout(
        yaxis=dict(
            tickmode='array',
            tickvals=[-1.7, -1, -0.5, 0, 0.5, 1, 1.7]
        )
    )

    fig.update_xaxes(title="Age")

    return fig


if __name__ == '__main__':
    app.run(debug=True)
