import glob
import os
import sys
from pathlib import Path

import gpxpy
import simplekml


def convert(path):
    path = Path(path)

    root_dir = path.resolve().parent.parent
    kml_dir = root_dir / "kml"
    kmz_dir = root_dir / "kmz"
    kml_dir.mkdir(exist_ok=True)
    kmz_dir.mkdir(exist_ok=True)
    kml_path = kml_dir / f"{path.stem}.kml"
    kmz_path = kmz_dir / f"{path.stem}.kmz"

    gpx_mtime = path.stat().st_mtime
    if (
        kml_path.exists()
        and kmz_path.exists()
        and kml_path.stat().st_mtime == gpx_mtime
        and kmz_path.stat().st_mtime == gpx_mtime
    ):
        return

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

    kml.save(kml_path)
    kml.savekmz(kmz_path)
    os.utime(kml_path, (gpx_mtime, gpx_mtime))
    os.utime(kmz_path, (gpx_mtime, gpx_mtime))


def sync_deletions(patterns):
    gpx_stems = set()
    root_dir = None
    for pattern in patterns:
        for filename in glob.glob(pattern) or [pattern]:
            path = Path(filename)
            gpx_stems.add(path.stem)
            root_dir = path.resolve().parent.parent

    if root_dir is None:
        return

    for dir_name, suffix in (("kml", ".kml"), ("kmz", ".kmz")):
        directory = root_dir / dir_name
        if not directory.exists():
            continue
        for existing in directory.glob(f"*{suffix}"):
            if existing.stem not in gpx_stems:
                existing.unlink()


if __name__ == "__main__":
    patterns = sys.argv[1:] or ["*.gpx"]
    for pattern in patterns:
        for filename in glob.glob(pattern) or [pattern]:
            convert(filename)
    sync_deletions(patterns)
