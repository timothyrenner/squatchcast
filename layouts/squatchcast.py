import dash_html_components as html
import dash_core_components as dcc


def squatchcast_layout(date_marks):
    return html.Div(
        children=[
            html.H1(
                "SquatchCast",
                style={
                    "textAlign": "center",
                    "gridColumn": "3/4",
                    "gridRow": "1/2",
                },
            ),
            html.Div(
                children=[
                    dcc.Slider(
                        id="day-slider",
                        min=0,
                        max=len(date_marks) - 1,
                        value=0,
                        marks=date_marks,
                        included=False,
                    )
                ],
                style={
                    "gridRow": "2/3",
                    "gridColumn": "1/6",
                    "padding-left": "25px",
                    "padding-right": "25px",
                },
            ),
            dcc.Graph(
                id="squatchcast-map",
                style={"gridRow": "3/11", "gridColumn": "1/5"},
                config={"displayModeBar": False},
            ),
            dcc.Graph(
                id="squatchcast-hist",
                style={"gridRow": "11/15", "gridColumn": "1/3"},
                config={"displayModeBar": False},
            ),
            dcc.Graph(
                id="temperature-hist",
                style={"gridRow": "11/15", "gridColumn": "3/5"},
                config={"displayModeBar": False},
            ),
            dcc.Graph(
                id="precip-bar",
                style={"gridRow": "11/15", "gridColumn": "5/6"},
                config={"displayModeBar": False},
            ),
            html.Div(
                children=[
                    html.H2("", id="weather", style={"textAlign": "center"}),
                    html.H3("Weather", style={"textAlign": "center"}),
                ],
                style={"gridRow": "4/6", "gridColumn": "5/6"},
            ),
            html.Div(
                children=[
                    html.H2(
                        "",
                        id="historical-sightings",
                        style={"textAlign": "center"},
                    ),
                    html.H3(
                        "Historical Sightings", style={"textAlign": "center"}
                    ),
                ],
                style={"gridRow": "6/8", "gridColumn": "5/6"},
            ),
            html.Div(
                children=[
                    html.H2(
                        "",
                        id="squatchcast-score",
                        style={"textAlign": "center"},
                    ),
                    html.H3(
                        "Squatchcast Score", style={"textAlign": "center"}
                    ),
                ],
                style={"gridRow": "8/10", "gridColumn": "5/6"},
            ),
        ],
        style={
            "display": "grid",
            "gridTemplateRows": "repeat(15, minmax(100px, 1fr))",
            "gridTemplateColumns": "repeat(5, minmax(250px, 1fr))",
        },
    )


# TODO: Footer, including dark sky attribution.
