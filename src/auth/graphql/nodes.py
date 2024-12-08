import strawberry


@strawberry.input
class AuthDataType:
    username: str
    password: str


@strawberry.type
class AuthGrantedDataType:
    access_token: str
    refresh_token: str
