import dash
import requests
from dash import dcc, html, Output, Input, State
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)

lat_grid = np.linspace(48.5, 51.2, 100)
lon_grid = np.linspace(12, 19, 100)
lat_points, lon_points = np.meshgrid(lat_grid, lon_grid)
lat_flat = lat_points.flatten()
lon_flat = lon_points.flatten()

def create_map_fig(selected_lat=None, selected_lon=None):
    fig = go.Figure(go.Scattergeo(
        lat=lat_flat,
        lon=lon_flat,
        mode="markers",
        marker=dict(opacity=0, size=8),
        showlegend=False,
        hoverinfo="lat+lon"
    ))
    if selected_lat is not None and selected_lon is not None:
        fig.add_trace(go.Scattergeo(
            lat=[selected_lat],
            lon=[selected_lon],
            mode="markers",
            marker=dict(color="red", size=12, opacity=1),
            name="Selected Point",
            showlegend=False
        ))
    fig.update_geos(
        center={"lat": 49.8175, "lon": 15.4730},
        projection_type="natural earth",
        scope="europe",
        projection_scale=8
    )
    fig.update_layout(clickmode="event+select")
    return fig

app.layout = html.Div([
    dcc.Graph(id="geo-map", config={"scrollZoom": True}, style={"height": "700px"}),
    html.Div(id="output"),
    dcc.Graph(id="temp-plot"),
    dcc.Graph(id="precip-plot"),
    dcc.Graph(id="prob-plot"),
])

@app.callback(
    [Output("geo-map", "figure"),
     Output("output", "children"),
     Output("temp-plot", "figure"),
     Output("precip-plot", "figure"),
     Output("prob-plot", "figure")],
    Input("geo-map", "clickData")
)
def display_click(clickData):
    selected_lat = selected_lon = None
    if clickData and "lat" in clickData["points"][0] and "lon" in clickData["points"][0]:
        selected_lat = clickData["points"][0]["lat"]
        selected_lon = clickData["points"][0]["lon"]
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={selected_lat}&longitude={selected_lon}&hourly=temperature_2m,precipitation,precipitation_probability"
        )
        try:
            resp = requests.get(url, timeout=5)
            data = resp.json()
            times = data["hourly"]["time"]
            temp = data["hourly"]["temperature_2m"]
            precip = data["hourly"]["precipitation"]
            prob = data["hourly"]["precipitation_probability"]

            temp_fig = go.Figure(go.Scatter(x=times, y=temp, name="Temperature (°C)"))
            temp_fig.update_layout(title="Temperature", yaxis_title="°C")

            precip_fig = go.Figure(go.Scatter(x=times, y=precip, name="Precipitation (mm)"))
            precip_fig.update_layout(title="Precipitation", yaxis_title="mm")

            prob_fig = go.Figure(go.Scatter(x=times, y=prob, name="Precipitation Probability (%)"))
            prob_fig.update_layout(title="Precipitation Probability", yaxis_title="%")

            output_text = (
                f"Selected coordinates: Latitude {selected_lat:.3f}, Longitude {selected_lon:.3f}"
            )
            map_fig = create_map_fig(selected_lat, selected_lon)
            return map_fig, output_text, temp_fig, precip_fig, prob_fig
        except Exception as e:
            map_fig = create_map_fig()
            return map_fig, f"Error fetching weather: {e}", go.Figure(), go.Figure(), go.Figure()
    map_fig = create_map_fig()
    return map_fig, "Click anywhere on the map to get coordinates.", go.Figure(), go.Figure(), go.Figure()

if __name__ == "__main__":
    app.run(debug=True)