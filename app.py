import dash

from dotenv import load_dotenv, find_dotenv
from dash.dependencies import Input, Output
from toolz import get_in

from layouts import squatchcast_layout
from plots import (
    squatchcast_map,
    squatchcast_score_distribution,
    squatchcast_temp_distribution,
    squatchcast_precip,
)
from loaders import load_squatchcast_data

load_dotenv(find_dotenv())


app = dash.Dash(
    "squatchcast",
    external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"],
)
# TODO: Heroku deployment stuff.

app.title = "SquatchCast"

squatchcast_data, dates, date_marks, layers = load_squatchcast_data(
    "data/squatchcast.csv.gz"
)

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
    return squatchcast_map(squatchcast_data.query(f"date==@date"), layers[day])


@app.callback(
    Output("squatchcast-hist", "figure"), [Input("day-slider", "value")]
)
def update_score_hist(day):
    date = dates[day]  # noqa
    return squatchcast_score_distribution(
        squatchcast_data.query("date==@date"), date_marks[day]
    )


@app.callback(
    Output("temperature-hist", "figure"), [Input("day-slider", "value")]
)
def update_temperature_hist(day):
    date = dates[day]  # noqa
    return squatchcast_temp_distribution(
        squatchcast_data.query("date==@date"), date_marks[day]
    )


@app.callback(Output("precip-bar", "figure"), [Input("day-slider", "value")])
def update_precip_bar(day):
    date = dates[day]  # noqa
    return squatchcast_precip(
        squatchcast_data.query("date==@date"), date_marks[day]
    )


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
