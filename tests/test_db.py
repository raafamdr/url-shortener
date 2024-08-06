from sqlalchemy import select

from url_shortener.models import URL


def test_create_url(session):
    new_url = URL(
        id=1, short_url='urlCurta', original_url='https://example.com/'
    )

    session.add(new_url)
    session.commit()

    url = session.scalar(
        select(URL).where(URL.original_url == 'https://example.com/')
    )

    assert url.id == 1
