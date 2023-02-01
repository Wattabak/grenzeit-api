
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
 docker run \          
    --name neo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/test \
    neo4j:latest
```
### Run an api app locally

```commandline
export DYLD_LIBRARY_PATH=/opt/homebrew/opt/geos/lib/ && python3 -m grenzeit.services.asgi 
```

### Running tests

```shell
 pytest tests -vvv
```


