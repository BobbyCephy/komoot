import glob
import sys
from pathlib import Path

import gpxpy
import simplekml


def convert(path):
    path = Path(path)
    with path.open(encoding="utf-8") as file:
        gpx = gpxpy.parse(file)

    kml = simplekml.Kml(name=path.name)
    default_name = path.name

    for track in gpx.tracks:
        placemark = kml.newmultigeometry(name=track.name or default_name)
        for segment in track.segments:
            placemark.newlinestring(
                coords=[
                    (point.longitude, point.latitude, point.elevation or 0)
                    for point in segment.points
                ]
            )

    for route in gpx.routes:
        kml.newlinestring(
            name=route.name or default_name,
            coords=[
                (point.longitude, point.latitude, point.elevation or 0)
                for point in route.points
            ],
        )

    for waypoint in gpx.waypoints:
        kml.newpoint(
            name=waypoint.name or "Waypoint",
            coords=[(waypoint.longitude, waypoint.latitude, waypoint.elevation or 0)],
        )

    root_dir = path.resolve().parent.parent
    kml_dir = root_dir / "kml"
    kmz_dir = root_dir / "kmz"
    kml_dir.mkdir(exist_ok=True)
    kmz_dir.mkdir(exist_ok=True)
    kml.save(kml_dir / f"{path.stem}.kml")
    kml.savekmz(kmz_dir / f"{path.stem}.kmz")


if __name__ == "__main__":
    for pattern in sys.argv[1:] or ["*.gpx"]:
        for filename in glob.glob(pattern) or [pattern]:
            convert(filename)
