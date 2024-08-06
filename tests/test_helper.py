from unittest.mock import patch

import pytest
from freezegun import freeze_time

from url_shortener.helper import decode, encode, generate_unique_id


@pytest.mark.parametrize(
    ('number', 'expected'),
    [
        (0, '0'),
        (1, '1'),
        (9, '9'),
        (10, 'A'),
        (35, 'Z'),
        (36, 'a'),
        (61, 'z'),
        (62, '10'),
        (123, '1z'),
        (3844, '100'),
        (238327, 'zzz'),
        (172194050517130, 'mtZVvg5a'),
    ],
)
def test_encode(number, expected):
    assert encode(number) == expected


@pytest.mark.parametrize(
    ('string', 'expected'),
    [
        ('0', 0),
        ('1', 1),
        ('9', 9),
        ('A', 10),
        ('Z', 35),
        ('a', 36),
        ('z', 61),
        ('10', 62),
        ('1z', 123),
        ('100', 3844),
        ('zzz', 238327),
        ('mtZVvg5a', 172194050517130),
    ],
)
def test_decode(string, expected):
    assert decode(string) == expected


@pytest.mark.xfail(raises=ValueError, strict=True)
@pytest.mark.parametrize('string', ['!@#', 'foo$', 'bar*'])
def test_decode_invalid_character(string):
    decode(string)


@freeze_time('2024-08-01 10:00:00')
@patch('url_shortener.helper.random.randint', return_value=32)
def test_generate_unique_id(mock_random):
    expected = 172250640000032
    assert generate_unique_id() == expected
