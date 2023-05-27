
# Grenzeit | Borders in time

A backend of the Grenzeit project

## Requirements

### System requirements

For shapely: [libgeos-dev ](https://libgeos.org/usage/install/)
I shall note that this is consistently one of the most irritating libraries to deal with,
issues with not being able to find geos on mac m1 are resolved with this:

```export DYLD_LIBRARY_PATH=/opt/homebrew/opt/geos/lib/```

For orjson: [cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html)

## Development

### Local environment

Setting up neo4j for local development

```shell
docker compose -f docker/docker-compose.yml up -d --build
```

### Run an api app locally

```shell
DYLD_LIBRARY_PATH='/opt/homebrew/opt/geos/lib/' python3 -m grenzeit.services.asgi 
```

### Running tests

```shell
 pytest tests -vvv
```

## API documentation

APi documentation can be found by using this route `/api/v1/docs`
http://0.0.0.0:8001/api/v1/docs