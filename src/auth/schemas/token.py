from pydantic import BaseModel


class TokenData(BaseModel):
    exp: int | None = None
    iat: int
    jti: str
    sub: str
    type: str
