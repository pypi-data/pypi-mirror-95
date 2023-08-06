import os
from tempfile import TemporaryDirectory

from ocds_babel.extract import extract_codelist, extract_extension_metadata, extract_schema

options = {
    'headers': 'Title,Description,Extension',
    'ignore': 'currency.csv',
}

codelist = b"""Code,Title,Description,Extension,Category
  foo  ,  bar  ,  baz  ,  bzz  ,  zzz  
  bar  ,       ,  bzz  ,  zzz  ,  foo  
  baz  ,  bzz  ,       ,  foo  ,  bar  
  bzz  ,  zzz  ,  foo  ,       ,  baz  
"""  # noqa: W291

schema = b"""{
    "title": {
        "oneOf": [{
            "title": "  foo  ",
            "description": "  bar  "
        }, {
            "title": "  baz  ",
            "description": "  bzz  "
        }]
    },
    "description": {
        "title": "  zzz  ",
        "description": "    "
    }
}"""

metadata_language_map = b"""{
    "name": {
        "en": "  foo  "
    },
    "description": {
        "en": "  bar  "
    }
}"""


metadata = b"""{
    "name": "  foo  ",
    "description": "  bar  "
}"""


def assert_result(filename, content, method, options, expected):
    with TemporaryDirectory() as d:
        with open(os.path.join(d, filename), 'wb') as f:
            f.write(content)

        with open(os.path.join(d, filename), 'rb') as f:
            assert list(method(f, None, None, options)) == expected


def test_extract_codelist():
    assert_result('test.csv', codelist, extract_codelist, options, [
        (0, '', 'Code', ''),
        (0, '', 'Title', ''),
        (0, '', 'Description', ''),
        (0, '', 'Extension', ''),
        (0, '', 'Category', ''),
        (1, '', 'bar', ['Title']),
        (1, '', 'baz', ['Description']),
        (1, '', 'bzz', ['Extension']),
        (2, '', 'bzz', ['Description']),
        (2, '', 'zzz', ['Extension']),
        (3, '', 'bzz', ['Title']),
        (3, '', 'foo', ['Extension']),
        (4, '', 'zzz', ['Title']),
        (4, '', 'foo', ['Description']),
    ])


def test_extract_codelist_currency():
    assert_result('currency.csv', codelist, extract_codelist, options, [
        (0, '', 'Code', ''),
        (0, '', 'Title', ''),
        (0, '', 'Description', ''),
        (0, '', 'Extension', ''),
        (0, '', 'Category', ''),
    ])


def test_extract_codelist_fieldname():
    assert_result('test.csv', b'Code,', extract_codelist, options, [
        (0, '', 'Code', ''),
    ])


def test_extract_codelist_newline():
    assert_result('test.csv', b'Code\rfoo', extract_codelist, options, [
        (0, '', 'Code', ''),
    ])


def test_extract_schema():
    assert_result('schema.json', schema, extract_schema, None, [
        (1, '', 'foo', ['/title/oneOf/0/title']),
        (1, '', 'bar', ['/title/oneOf/0/description']),
        (1, '', 'baz', ['/title/oneOf/1/title']),
        (1, '', 'bzz', ['/title/oneOf/1/description']),
        (1, '', 'zzz', ['/description/title']),
    ])


def test_extract_extension_metadata():
    assert_result('extension.json', metadata, extract_extension_metadata, None, [
        (1, '', 'foo', ['/name']),
        (1, '', 'bar', ['/description']),
    ])


def test_extract_extension_metadata_language_map():
    assert_result('extension.json', metadata_language_map, extract_extension_metadata, None, [
        (1, '', 'foo', ['/name/en']),
        (1, '', 'bar', ['/description/en']),
    ])


def test_extract_extension_metadata_empty():
    assert_result('extension.json', b'{}', extract_extension_metadata, None, [])
