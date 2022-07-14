
# Grenzeit | Borders in time

A backend of the Grenzeit project


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

### Running tests

```shell
 pytest tests -vvv
```


