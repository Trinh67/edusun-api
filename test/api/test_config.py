import pytest

from app.helper.enum import ConfigValueType
from app.model import Config
from test.faker.config import ConfigProvider

BASE_URL = 'api/v1/configs'

@pytest.mark.parametrize(
    "query, expect_http_code, expect_code",
    [
        (f"?types={ConfigValueType.COUNTRY.value}", 200, 200),
    ]
)
def test_get_selection_fields(session, client, query, expect_http_code, expect_code):
    """
       name: Test get selection fields
       objective: Test get selection fields
       precondition:
    """
    ConfigProvider.create_config(session, id=1, name="Han", type=ConfigValueType.COUNTRY.value,
                                 commit=True)

    resp = client.get(f'{BASE_URL}' + query)

    assert resp.status_code == expect_http_code
    assert resp.json().get('code') == expect_code

    if expect_http_code == 200:
        assert len(resp.json().get('data').get('configs')) > 0


@pytest.mark.parametrize(
    "query,expect_http_code,expected_data",
    [
        (
                "?types=country",
                200,
                {
                    'configs': [
                        {
                            'valueType': ConfigValueType.COUNTRY.value,
                            'values': [
                                {'id': 1, 'value': 'Han'}
                            ]
                        }
                    ]
                }
        ),
        (
                "",
                200,
                {'configs': []}
        ),
    ]
)
def test_get_list_selection_fields(session, client, query, expect_http_code, expected_data):
    """
        name: Test get list selection fields
        objective: Test get list selection fields
        precondition:
    """
    ConfigProvider.create_config(session, id=1, name="Han", type=ConfigValueType.COUNTRY.value,
                                 commit=True)

    resp = client.get(f'{BASE_URL}' + query)

    assert resp.status_code == expect_http_code
    assert resp.json().get('data') == expected_data


def test_create_selection_value(session, client):
    """
       name: Test create selection value
       objective: Test create selection value
       precondition:
    """
    resp = client.post(f'{BASE_URL}', json={
        "name": "Han",
        "type": ConfigValueType.COUNTRY.value,
        "value": "Han"
    })

    assert resp.status_code == 200
    assert resp.json().get('data').get('configId') > 0


def test_delete_selection_value(session, client):
    """
       name: Test delete selection value
       objective: Test delete selection value
       precondition:
    """
    ConfigProvider.create_config(session, id=1, name="Han", type=ConfigValueType.COUNTRY.value,
                                 commit=True)

    resp = client.delete(f'{BASE_URL}/1')

    assert resp.status_code == 200

    selection_value = Config.first(session, Config.id == 1)
    assert selection_value is None
