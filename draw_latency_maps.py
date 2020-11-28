#!/usr/bin/env python3

from collections import defaultdict

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib import colors
from shapely import wkb
from shapely.geometry import MultiPoint
import psycopg2
import numpy as np

from cartopy.examples.waves import sample_data


query = """
SELECT
from_,
ST_AsBinary(from_cities.location),
avg,
to_,
ST_AsBinary(to_cities.location)
FROM
latencies
JOIN geocoded_cities as from_geocode
ON from_ = from_geocode.latency_city_name
JOIN geocoded_cities as to_geocode
ON to_ = to_geocode.latency_city_name
JOIN cities as from_cities
ON from_cities.geoname_id = from_geocode.geoname_id
JOIN cities as to_cities
ON to_cities.geoname_id = to_geocode.geoname_id
WHERE from_ = 'London'
ORDER BY to_ asc
"""

CLASSES = set(range(1, 6))


def decide_class(latency: float) -> int:
    if latency <= 15:
        return 1
    elif 15 < latency <= 50:
        return 2
    elif 50 < latency <= 100:
        return 3
    elif 100 < latency <= 150:
        return 4
    else:
        return 5


def main():
    conn = psycopg2.connect("dbname=latency")
    cursor = conn.cursor()
    cursor.execute(query)

    xs = []
    ys = []
    zs = []

    for from_, from_wkb, avg, to_, to_wkb in cursor:
        point = wkb.loads(to_wkb.tobytes())
        xs.append(point.x)
        ys.append(point.y)
        zs.append(avg)

    x = xs
    y = ys
    z = zs

    proj = ccrs.Robinson(
        central_longitude=51.5074
    )

    fig = plt.figure()

    ax = fig.add_subplot(
        1,
        1,
        1,
        projection=proj,
    )
    ax.set_global()
    ax.coastlines("110m")

    # Add colourful filled contours.
    filled_c = ax.tricontourf(
        x,
        y,
        z,
        levels=[min(xs), 15, 30, 60, 120, 240, 480, 1000],
        transform=ccrs.PlateCarree(),
        norm=colors.Normalize(vmin=0, vmax=480),
        cmap="RdYlGn_r",
        extend="max",
        alpha=0.5
    )


    # # And black line contours.
    # line_c = ax.tricontour(
    #     x,
    #     y,
    #     z,
    #     levels=filled_c.levels,
    #     colors=["black"],
    #     linestyles="dashed",
    #     transform=ccrs.PlateCarree(),
    #     alpha=0.5,
    # )

    # Uncomment to make the line contours invisible.
    # plt.setp(line_c.collections, visible=False)

    # Add a colorbar for the filled contour.
    fig.colorbar(filled_c, orientation="horizontal")

    # # Use the line contours to place contour labels.
    # ax.clabel(
    #     line_c,  # Typically best results when labelling line contours.
    #     colors=["black"],
    #     manual=False,  # Automatic placement vs manual placement.
    #     inline=True,  # Cut the line where the label will be placed.
    #     fmt=" {:.0f} ".format,  # Labes as integers, with some extra space.
    # )

    plt.show()


if __name__ == "__main__":
    main()
