from logging import config

import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from src.auth.graphql.mutations import AuthMutation
from src.events.graphql.mutations import (
    EventMutation,
    RegistrationMutation,
    ResourceMutation,
    ScheduleMutation,
)
from src.events.graphql.queries import EventQuery, ResgistrationQuery, ResourceQuery, ScheduleQuery
from src.healthcheck.graphql.queries import HealthCheckQuery
from src.users.graphql.mutations import UserMutation
from src.users.graphql.queries import UserQuery

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
    EventQuery,
    HealthCheckQuery,
    ResgistrationQuery,
    ResourceQuery,
    ScheduleQuery,
    UserQuery,
): ...


@strawberry.type
class Mutation(
    AuthMutation,
    EventMutation,
    RegistrationMutation,
    ResourceMutation,
    ScheduleMutation,
    UserMutation,
): ...


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
graphql_app = GraphQLRouter[object, object](
    schema=schema,
)


app.include_router(router=graphql_app, prefix="/graphql")
