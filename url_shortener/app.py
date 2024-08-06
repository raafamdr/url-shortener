from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session

from url_shortener.database import get_session
from url_shortener.helper import decode, encode, generate_unique_id
from url_shortener.models import URL
from url_shortener.schemas import Message, UrlResponse, UrlSchema

app = FastAPI()


@app.post(
    '/api/urls/shorten',
    status_code=HTTPStatus.CREATED,
    response_model=UrlResponse,
    responses={HTTPStatus.BAD_REQUEST: {'model': Message}},
)
def shortening_service(
    url: UrlSchema, session: Session = Depends(get_session)
):
    mapped_url = session.scalar(
        select(URL).where(URL.original_url == str(url.long_url))
    )

    if mapped_url:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='URL already shortened.',
        )

    unique_id = generate_unique_id()
    shortened_url = encode(unique_id)

    mapped_url = URL(
        id=unique_id, short_url=shortened_url, original_url=str(url.long_url)
    )

    session.add(mapped_url)
    session.commit()
    session.refresh(mapped_url)

    return UrlResponse(
        short_url=f'http://127.0.0.1:8000/api/urls/{shortened_url}'
    )


@app.get(
    '/api/urls/{short_url}',
    response_class=RedirectResponse,
    status_code=HTTPStatus.FOUND,
    responses={
        HTTPStatus.BAD_REQUEST: {'model': Message},
        HTTPStatus.NOT_FOUND: {'model': Message},
    },
)
def redirection_service(
    short_url: str,
    session: Session = Depends(get_session),
):
    try:
        id = decode(short_url)
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Invalid request.'
        )

    try:
        url = session.scalar(select(URL).where(URL.id == id))
    except DataError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Invalid request.'
        )

    if not url:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='URL not found.'
        )

    url.access_count += 1
    session.commit()
    session.refresh(url)

    return url.original_url


@app.delete(
    '/api/urls/{short_url}',
    response_model=Message,
    responses={
        HTTPStatus.BAD_REQUEST: {'model': Message},
        HTTPStatus.NOT_FOUND: {'model': Message},
    },
)
def delete_service(short_url: str, session: Session = Depends(get_session)):
    try:
        id = decode(short_url)
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Invalid request.'
        )

    try:
        url = session.scalar(select(URL).where(URL.id == id))
    except DataError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Invalid request.'
        )

    if not url:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='URL not found.'
        )

    session.delete(url)
    session.commit()

    return {'message': 'URL has been deleted successfully.'}
