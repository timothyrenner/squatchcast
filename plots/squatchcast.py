import os


def squatchcast_map(squatchcast_data, layers, zoom=4, center=None):
    """ Builds the data structure required for a map of the squatchcast.
    """
    # TODO: This resets the zoom level and center of the map.
    # TODO: Let's not do that.
    if center is None:
        center = [
            squatchcast_data.latitude.mean(),
            squatchcast_data.longitude.mean(),
        ]
    return {
        "data": [
            {
                "type": "scattermapbox",
                "lat": squatchcast_data.latitude.tolist(),
                "lon": squatchcast_data.longitude.tolist(),
                "text": squatchcast_data.text.tolist(),
                "mode": "markers",
                "marker": {
                    "size": 1,
                    "color": squatchcast_data.color.tolist(),
                },
                "hoverinfo": "text",
                "customdata": squatchcast_data[
                    [
                        "temperature_high",
                        "squatchcast",
                        "precip_type",
                        "historical_sightings",
                    ]
                ].to_dict(orient="records"),
            }
        ],
        "layout": {
            "mapbox": {
                "accesstoken": os.getenv("MAPBOX_KEY"),
                "layers": layers,
                "center": {"lat": center[0], "lon": center[1]},
                "zoom": zoom,
                "style": "mapbox://styles/mapbox/light-v9",
            },
            "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
        },
    }


def squatchcast_score_distribution(squatchcast_data, date):
    """ Builds the histogram for the squatchast scores.
    """
    return {
        "data": [
            {"type": "histogram", "x": squatchcast_data.squatchcast.tolist()}
        ],
        "layout": {
            "title": f"Squatchcast Scores: {date}",
            "xaxis": {"title": "Squatchcast Score"},
            "bargap": 0.05,
        },
    }


def squatchcast_temp_distribution(squatchcast_data, date):
    """ Builds the histogram for the squatchcast temperatures.
    """
    return {
        "data": [
            {
                "type": "histogram",
                "x": squatchcast_data.temperature_high.tolist(),
            }
        ],
        "layout": {
            "title": f"High Temperatures: {date}",
            "xaxis": {"title": "High Temperature"},
            "bargap": 0.05,
        },
    }


def squatchcast_precip(squatchcast_data, date):
    """ Builds the bar chart for the squatchcast precipitation types.
    """
    grouped_data = squatchcast_data.groupby("precip_type").agg(
        {"precip_type": "count"}
    )
    return {
        "data": [
            {
                "type": "bar",
                "x": grouped_data.index.tolist(),
                "y": grouped_data.precip_type.tolist(),
            }
        ],
        "layout": {
            "title": f"Precip Type: {date}",
            "xaxis": {"title": "Precipitation Type"},
            "yaxis": {"title": "Number of Locations"},
        },
    }
