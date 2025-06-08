import pytest

from tagsub.dynamodb import (
    get_dynamodb_client, get_dynamodb_type_serializer, serialize_dynamodb_items,
    get_dynamodb_type_deserializer, deserialize_dynamodb_items, query
)
from tests.dynamodb_utils import set_up_dynamodb_data


@pytest.mark.parametrize(
    'items,expected_result',
    [
        (
            [
                {
                    'handle': '@dummyuser',
                    'hashtag': '#DummyHT'
                },
                {
                    'handle': '@dummyuser2',
                    'hashtag': '#DummyHT2'
                },
                {
                    'handle': '@dummyuser3',
                    'hashtag': '#DummyHT3'
                }
            ],
            [
                {
                    'handle': {'S': '@dummyuser'},
                    'hashtag': {'S': '#DummyHT'}
                },
                {
                    'handle': {'S': '@dummyuser2'},
                    'hashtag': {'S': '#DummyHT2'}
                },
                {
                    'handle': {'S': '@dummyuser3'},
                    'hashtag': {'S': '#DummyHT3'}
                }
            ]
        ),
        (
            [],
            []
        )
    ]
)
def test_serialize_dynamodb_items(items, expected_result, app):
    """
    Will include the tests for get_dynamodb_type_serializer()
    here since these functions are always used together.
    """
    with app.app_context():
        dynamodb_type_serializer = get_dynamodb_type_serializer()
        assert dynamodb_type_serializer == get_dynamodb_type_serializer()

        result = serialize_dynamodb_items(items)

    assert result == expected_result


@pytest.mark.parametrize(
    'items,expected_result',
    [
        (
            [
                {
                    'handle': {'S': '@dummyuser'},
                    'hashtag': {'S': '#DummyHT'}
                },
                {
                    'handle': {'S': '@dummyuser2'},
                    'hashtag': {'S': '#DummyHT2'}
                },
                {
                    'handle': {'S': '@dummyuser3'},
                    'hashtag': {'S': '#DummyHT3'}
                }
            ],
            [
                {
                    'handle': '@dummyuser',
                    'hashtag': '#DummyHT'
                },
                {
                    'handle': '@dummyuser2',
                    'hashtag': '#DummyHT2'
                },
                {
                    'handle': '@dummyuser3',
                    'hashtag': '#DummyHT3'
                }
            ]
        ),
        (
            [],
            []
        )
    ]
)
def test_deserialize_dynamodb_items(items, expected_result, app):
    """
    Will include the tests for get_dynamodb_type_deserializer()
    here since these functions are always used together.
    """
    with app.app_context():
        dynamodb_type_deserializer = get_dynamodb_type_deserializer()
        assert dynamodb_type_deserializer == get_dynamodb_type_deserializer()

        result = deserialize_dynamodb_items(items)

    assert result == expected_result


@pytest.mark.parametrize(
    'expected_result',
    [
        (
            [
                {
                    'Handle': '@TestUser',
                    'Hashtag': '#DummyHT'
                },
                {
                    'Handle': '@TestUser',
                    'Hashtag': '#DummyHT2'
                },
                {
                    'Handle': '@TestUser',
                    'Hashtag': '#DummyHT3'
                }
            ]
        ),
        (
            []
        )
    ]
)
def test_query(expected_result, app, dynamodb_table):
    """
    Will include the tests for get_dynamodb_client()
    here since these functions are always used together.
    """
    with app.app_context():
        dynamodb_client = get_dynamodb_client()
        assert dynamodb_client == get_dynamodb_client()

        if len(expected_result) > 0:
            set_up_dynamodb_data(
                dynamodb_client,
                app.config.get('DYNAMODB_TABLE'),
                expected_result
            )

        result = query(
            {
                'TableName': app.config.get('DYNAMODB_TABLE'),
                'KeyConditionExpression': 'Handle = :Handle',
                'ExpressionAttributeValues': {
                    ':Handle': {'S': app.config.get('USER_HANDLE')}
                }
            }
        )

        assert result == expected_result
