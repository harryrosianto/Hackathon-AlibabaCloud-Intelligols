from pydantic import BaseModel

from schemas.user import UserSch


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    user: UserSch


class TokenRead(BaseModel):
    access_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str