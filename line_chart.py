from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

filepath = "/Users/melody/loreal_results/interactive_chart.csv"
df = pd.read_csv(filepath)

df["Coderre_pct"] = round(df["Coderre"] / df["total"] * 100, 2)
df["Joly_pct"] = round(df["Joly"] / df["total"] * 100, 2)
df["Bergeron_pct"] = round(df["Bergeron"] / df["total"] * 100, 2)

candidate_list = ["Coderre_pct", "Joly_pct", "Bergeron_pct"]

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(
            "ECDF of Vote Share (%) by District in Montreal's Municipal Elections, 2013",
            style={"textAlign": "center"},
        ),
        html.Div(
            [
                html.H3("Choose a candidate:"),
                dcc.Dropdown(
                    id="candidate-dropdown",
                    value="Joly_pct",
                    options=candidate_list,
                    multi=True,
                ),
            ],
            style={
                "width": "50%",
                "marginLeft": "5em",
            },
        ),
        dcc.Graph(id="graph"),
    ]
)


@app.callback(
    Output("graph", "figure"),
    Input("candidate-dropdown", "value"),
)
def update_graph(candidate):
    fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)