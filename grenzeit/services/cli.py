import datetime

import click
import geopandas

from grenzeit.api.v1.schema import Country, Territory
from grenzeit.config import logger
from grenzeit.config import settings
from neomodel import config
from geojson_pydantic.geometries import Polygon, MultiPolygon

@click.group()
def main():
    config.DATABASE_URL = settings.DATABASE_URL
    pass


def geojson_structure(geojson: dict[str, any]):
    pass


@main.command()
@click.option("-p", "path", required=True, type=click.Path(), )
def geojson(path: str):
    logger.info(f"Reading a geojson file from {path}")
    gdf = geopandas.read_file(path)
    click.echo(gdf)
    for _, row in gdf.iterrows():
        c = Country(
            name_eng=row['name'],
            name_zeit=row['name'],
            founded_at=datetime.date(year=2000, month=1, day=1)
        )
        c.save()
        geometry = geopandas.GeoSeries([row.geometry]).__geo_interface__['features'][0]['geometry']

        t = Territory(geometry=geometry)
        t.save()
        rel = c.claims_territory.connect(t, {"date_start": datetime.date(year=2000, month=1, day=1)})
        rel.save()


if __name__ == "__main__":
    main()
