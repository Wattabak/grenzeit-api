import datetime

import click
import geopandas
from neomodel import config
from shapely.geometry import shape

from grenzeit.api.v1.schema import Country, Territory, Cluster
from grenzeit.config import logger
from grenzeit.config import settings


@click.group()
def main():
    config.DATABASE_URL = settings.DATABASE_URL
    pass


def geojson_structure(geojson: dict[str, any]):
    pass


@main.command()
@click.option("-p", "path", required=True, type=click.Path(), )
def load_countries(path: str, ):
    logger.info(f"Reading a geojson file from {path}")
    gdf = geopandas.read_file(path)
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


@main.command()
@click.option("-p", "path", required=True, type=click.Path(), )
def load_cluster(path: str):
    logger.info(f"Reading a geojson file from {path}")
    gdf = geopandas.read_file(path)
    for _, row in gdf.iterrows():
        c = Cluster(
            name=row['CONTINENT'],
            geometry=geopandas.GeoSeries([row.geometry]).__geo_interface__['features'][0]['geometry']
        )
        c.save()


@main.command()
def clusterize_countries():
    cluster_gdf = geopandas.GeoDataFrame(
        data=[cluster.name for cluster in Cluster.nodes],
        geometry=[
            shape(cluster.geometry)
            for cluster in Cluster.nodes
        ]
    )

    for country in Country.nodes:
        logger.info(country.name_eng)
        if country.cluster:
            logger.info(f"{country.name_eng} already part of cluster {country.cluster[0].name}")
            continue
        territory = shape(country.claims_territory.get().geometry)
        cluster_gdf[country.uid] = cluster_gdf.centroid.distance(territory.centroid)
        closest_cluster = cluster_gdf.iloc[cluster_gdf[country.uid].argmin()][0]
        country.cluster.connect(Cluster.nodes.get(name=closest_cluster))



if __name__ == "__main__":
    main()
