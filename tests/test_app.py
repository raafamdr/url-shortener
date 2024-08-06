from http import HTTPStatus
from unittest.mock import patch

import pytest


@patch('url_shortener.app.generate_unique_id', return_value=172194050517130)
@patch('url_shortener.app.encode', return_value='mtZVvg5a')
def test_create_url(mock_encode, mock_generate_unique_id, client):
    response = client.post(
        '/api/urls/shorten',
        json={
            'long_url': 'https://example.com/',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'short_url': 'http://127.0.0.1:8000/api/urls/mtZVvg5a'
    }


def test_create_url_already_shortened(client, url):
    response = client.post(
        '/api/urls/shorten',
        json={
            'long_url': 'https://example.com/',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'URL already shortened.'}


def test_get_url(client, url, session):
    initial_access_count = url.access_count

    response = client.get(f'/api/urls/{url.short_url}', follow_redirects=False)

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers['Location'] == url.original_url

    session.refresh(url)

    assert url.access_count == initial_access_count + 1


@pytest.mark.parametrize(
    ('short_url', 'expected_status', 'expected_response'),
    [
        ('foo$', HTTPStatus.BAD_REQUEST, {'detail': 'Invalid request.'}),
        (
            'mtZVvg5asdas',
            HTTPStatus.BAD_REQUEST,
            {'detail': 'Invalid request.'},
        ),
        ('bar', HTTPStatus.NOT_FOUND, {'detail': 'URL not found.'}),
    ],
)
def test_get_invalid_urls(
    client, short_url, expected_status, expected_response
):
    response = client.get(f'/api/urls/{short_url}')

    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_delete_url(client, url):
    response = client.delete(f'/api/urls/{url.short_url}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'URL has been deleted successfully.'}


@pytest.mark.parametrize(
    ('short_url', 'expected_status', 'expected_response'),
    [
        ('foo$', HTTPStatus.BAD_REQUEST, {'detail': 'Invalid request.'}),
        (
            'mtZVvg5asdas',
            HTTPStatus.BAD_REQUEST,
            {'detail': 'Invalid request.'},
        ),
        ('bar', HTTPStatus.NOT_FOUND, {'detail': 'URL not found.'}),
    ],
)
def test_delete_invalid_urls(
    client, short_url, expected_status, expected_response
):
    response = client.delete(f'/api/urls/{short_url}')

    assert response.status_code == expected_status
    assert response.json() == expected_response
