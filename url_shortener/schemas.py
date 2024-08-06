from pydantic import BaseModel, HttpUrl


class UrlSchema(BaseModel):
    long_url: HttpUrl


class UrlResponse(BaseModel):
    short_url: HttpUrl


class Message(BaseModel):
    message: str
