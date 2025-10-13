import numpy as np
import pandas as pd
from _plotly_utils.colors import sample_colorscale
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data = pd.read_csv("sens1_01_trajectory.csv")
data["colors"] = sample_colorscale("Reds", np.linspace(0.3, 1, len(data)))

app = Dash(__name__)

app.layout = html.Div([
    html.H2('3D Scatter Plot of Cartesian and Joint Coordinates', style={'textAlign': 'center'}),
    html.Label("Select index range", style={"font-weight": "bold", "margin-top": "20px"}),
    dcc.RangeSlider(
        id="row-range-slider",
        min=0,
        max=len(data) - 1,
        value=[0, len(data) - 1],
        marks={0: "0", len(data) - 1: str(len(data) - 1)},
        step=1,
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    dcc.Loading(
        dcc.Graph(id="graph", style={"width": "100vw", "height": "80vh"}),
        type="cube"
    )
], style={"backgroundColor": "white", "minHeight": "80vh", "margin": 0, "padding": 0})

ax_style = dict(
    showbackground=True,
    showgrid=True,
    zeroline=False,
    showline=True,
    linecolor='black',
    linewidth=4
)

@app.callback(
    Output("graph", "figure"),
    Input("row-range-slider", "value"))
def update_graph(row_range):
    row_min, row_max = row_range
    filtered = data.iloc[row_min:row_max + 1]
    indices = filtered.index.astype(str)
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'scene'}, {'type': 'scene'}]],
        subplot_titles=("Cartesian coord", "Joint coord"),
        horizontal_spacing=0.02
    )
    fig.add_trace(
        go.Scatter3d(
            x=filtered["x"],
            y=filtered["y"],
            z=filtered["z"],
            mode="markers",
            marker=dict(size=2, color=data["colors"]),
            text=indices,
            hovertemplate="Index: %{text}<br>x: %{x}<br>y: %{y}<br>z: %{z}<extra></extra>"
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter3d(
            x=filtered["qx"],
            y=filtered["qy"],
            z=filtered["qz"],
            mode="markers",
            marker=dict(size=2, color=data["colors"]),
            text=indices,
            hovertemplate="Index: %{text}<br>x: %{x}<br>y: %{y}<br>z: %{z}<extra></extra>"
        ),
        row=1, col=2
    )
    fig.update_layout(scene1=dict(xaxis=ax_style, yaxis=ax_style, zaxis=ax_style, aspectmode='data'),
    scene2=dict(xaxis=ax_style, yaxis=ax_style, zaxis=ax_style, aspectmode='data'),
    margin=dict(l=0, r=0, b=50, t=20),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False,
    uirevision="constant")
    return fig

if __name__ == "__main__":
    app.run(debug=True)