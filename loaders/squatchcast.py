import pandas as pd
import numpy as np
import json

from math import floor
from palettable.colorbrewer.sequential import YlOrRd_9 as colors
from datetime import datetime


def _make_layers(data):
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


def load_squatchcast_data(squatchcast_file):
    squatchcast_data = pd.read_csv("data/squatchcast.csv.gz").assign(
        color=lambda frame: frame.squatchcast.apply(
            lambda x: colors.hex_colors[
                (floor(x * 10) - 1) if floor(x * 10) > 0 else 0
            ]
        ),
        text=lambda frame: frame.squatchcast.apply(
            lambda x: f"Squatchcast: {x:.3f}"
        ),
        precip_type=lambda frame: np.where(
            frame.precip_probability < 0.4,
            "no_precipitation",
            frame.precip_type,
        ),
    )
    dates = {
        ii: d for ii, d in enumerate(sorted(squatchcast_data.date.unique()))
    }
    date_marks = {
        ii: datetime.strptime(d, "%Y-%m-%d").strftime("%m/%d")
        for ii, d in dates.items()
    }
    layers = {
        ii: _make_layers(squatchcast_data.query(f"date=='{dates[ii]}'"))
        for ii in dates.keys()
    }

    return squatchcast_data, dates, date_marks, layers
