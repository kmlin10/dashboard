import plotly.graph_objects as go
import numpy as np

fig = go.Figure(go.Scatter(
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    y = np.random.randint(-20,20,12)
))
#fig.update_layout(yaxis_tickformat='$,')#yaxis_tickprefix='$',
fig.update_yaxes(visible=True,
                     labelalias={0: "average", 0.5: '', "5": "85th Percentile", 15: '', -5:'', -10: "15th Percentile"},
                     ticklabelposition="outside top", gridcolor='lightgrey')#, showticklabels=False)

fig.show()
