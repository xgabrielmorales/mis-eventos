from logging import config

import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from src.healthcheck.graphql.queries import HealthCheckQuery

config.fileConfig(
    fname="logging.ini",
    disable_existing_loggers=False,
)

app = FastAPI(
    title="Mis Eventos",
    description="Service responsible for event management and process automation.",
    version="0.1.0",
)


@strawberry.type
class Query(
    HealthCheckQuery,
): ...


@strawberry.type
class Mutation: ...


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
graphql_app = GraphQLRouter[object, object](
    schema=schema,
)


app.include_router(router=graphql_app, prefix="/graphql")
