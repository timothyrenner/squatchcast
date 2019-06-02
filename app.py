import dash
import pandas as pd
import numpy as np
import json

from dotenv import load_dotenv, find_dotenv
from palettable.colorbrewer.sequential import YlOrRd_9 as colors
from math import floor
from datetime import datetime
from dash.dependencies import Input, Output
from toolz import get_in

from layouts import squatchcast_layout
from plots import (
    squatchcast_map,
    squatchcast_score_distribution,
    squatchcast_temp_distribution,
    squatchcast_precip,
)

load_dotenv(find_dotenv())


def make_layers(data):
    layers = []
    # We want one layer per color group.
    for color, group in data.groupby("color"):
        # Each layer is a multipolygon of all hexagons with the same color.
        geojson = {"type": "MultiPolygon", "coordinates": []}
        for _, row in group.iterrows():
            geojson["coordinates"].append([json.loads(row.hex_geojson)])
        layers.append(
            {
                "sourcetype": "geojson",
                "source": geojson,
                "color": color,
                "below": "water",
                "opacity": 0.5,
                "type": "fill",
            }
        )
    return layers


app = dash.Dash(
    "squatchcast",
    external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"],
)
# TODO: Heroku deployment stuff.

app.title = "SquatchCast"

data = pd.read_csv("data/squatchcast.csv.gz").assign(
    color=lambda frame: frame.squatchcast.apply(
        lambda x: colors.hex_colors[
            (floor(x * 10) - 1) if floor(x * 10) > 0 else 0
        ]
    ),
    text=lambda frame: frame.squatchcast.apply(
        lambda x: f"Squatchcast: {x:.3f}"
    ),
    precip_type=lambda frame: np.where(
        frame.precip_probability < 0.4, "no_precipitation", frame.precip_type
    ),
)

dates = {ii: d for ii, d in enumerate(sorted(data.date.unique()))}
date_marks = {
    ii: datetime.strptime(d, "%Y-%m-%d").strftime("%m/%d")
    for ii, d in dates.items()
}
layers = {
    ii: make_layers(data.query(f"date=='{dates[ii]}'")) for ii in dates.keys()
}

###############################################################################
# LAYOUT
###############################################################################

app.layout = squatchcast_layout(date_marks)

###############################################################################
# CALLBACKS
###############################################################################


@app.callback(
    Output("squatchcast-map", "figure"), [Input("day-slider", "value")]
)
def update_map(day):
    date = dates[day]  # noqa
    return squatchcast_map(data.query(f"date==@date"), layers[day])


@app.callback(
    Output("squatchcast-hist", "figure"), [Input("day-slider", "value")]
)
def update_score_hist(day):
    date = dates[day]  # noqa
    return squatchcast_score_distribution(
        data.query("date==@date"), date_marks[day]
    )


@app.callback(
    Output("temperature-hist", "figure"), [Input("day-slider", "value")]
)
def update_temperature_hist(day):
    date = dates[day]  # noqa
    return squatchcast_temp_distribution(
        data.query("date==@date"), date_marks[day]
    )


@app.callback(Output("precip-bar", "figure"), [Input("day-slider", "value")])
def update_precip_bar(day):
    date = dates[day]  # noqa
    return squatchcast_precip(data.query("date==@date"), date_marks[day])


@app.callback(
    Output("weather", "children"), [Input("squatchcast-map", "hoverData")]
)
def update_high_temperature(map_hover_data):
    if map_hover_data:
        high_temp = get_in(
            ["points", 0, "customdata", "temperature_high"], map_hover_data, ""
        )
        precipitation = get_in(
            ["points", 0, "customdata", "precip_type"], map_hover_data, ""
        )
        if (not precipitation) or (precipitation == "no_precipitation"):
            precipitation = "clear"
        return f"{int(high_temp)}\xb0F, {precipitation}"
    else:
        return "\n"


@app.callback(
    Output("historical-sightings", "children"),
    [Input("squatchcast-map", "hoverData")],
)
def update_historical_sightings(map_hover_data):
    if map_hover_data:
        historical_sightings = get_in(
            ["points", 0, "customdata", "historical_sightings"],
            map_hover_data,
            "",
        )
        return historical_sightings
    else:
        return "\n"


@app.callback(
    Output("squatchcast-score", "children"),
    [Input("squatchcast-map", "hoverData")],
)
def update_squatchcast_score(map_hover_data):
    if map_hover_data:
        score = get_in(
            ["points", 0, "customdata", "squatchcast"], map_hover_data
        )
        return f"{score:.3f}"
    else:
        return "\n"


if __name__ == "__main__":
    app.run_server()
