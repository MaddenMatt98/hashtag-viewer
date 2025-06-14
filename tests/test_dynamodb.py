from copy import deepcopy

import mock
import pytest

from tagsub.dynamodb import (
    get_dynamodb_client, get_dynamodb_type_serializer, serialize_dynamodb_items,
    get_dynamodb_type_deserializer, deserialize_dynamodb_items, query, put
)
from tests.dynamodb_utils import set_up_dynamodb_data


@pytest.mark.parametrize(
    'items,expected_result',
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
            ],
            [
                {
                    'Handle': {'S': '@TestUser'},
                    'Hashtag': {'S': '#DummyHT'}
                },
                {
                    'Handle': {'S': '@TestUser'},
                    'Hashtag': {'S': '#DummyHT2'}
                },
                {
                    'Handle': {'S': '@TestUser'},
                    'Hashtag': {'S': '#DummyHT3'}
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
                    'Handle': {'S': '@dummyuser'},
                    'Hashtag': {'S': '#DummyHT'}
                },
                {
                    'Handle': {'S': '@dummyuser2'},
                    'Hashtag': {'S': '#DummyHT2'}
                },
                {
                    'Handle': {'S': '@dummyuser3'},
                    'Hashtag': {'S': '#DummyHT3'}
                }
            ],
            [
                {
                    'Handle': '@dummyuser',
                    'Hashtag': '#DummyHT'
                },
                {
                    'Handle': '@dummyuser2',
                    'Hashtag': '#DummyHT2'
                },
                {
                    'Handle': '@dummyuser3',
                    'Hashtag': '#DummyHT3'
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
    'items,expected_result',
    [
        (
            [
                {
                    'Handle': {'S': '@TestUser'},
                    'Hashtag': {'S': '#DummyHT'}
                },
                {
                    'Handle': {'S': '@TestUser'},
                    'Hashtag': {'S': '#DummyHT2'}
                },
                {
                    'Handle': {'S': '@TestUser'},
                    'Hashtag': {'S': '#DummyHT3'}
                }
            ],
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
            [],
            []
        )
    ]
)
@mock.patch('tagsub.dynamodb.deserialize_dynamodb_items')
def test_query(mock_deserialize_dynamodb_items, items, expected_result, app, dynamodb_table):
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
                deepcopy(expected_result)
            )

        mock_deserialize_dynamodb_items.return_value = deepcopy(expected_result)
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
        mock_deserialize_dynamodb_items.assert_called_once_with(items)


@pytest.mark.parametrize(
    'item,expected_result',
    [
        (
            {
                'Handle': '@TestUser',
                'Hashtag': '#DummyHT'
            },
            {
                'Handle': {'S': '@TestUser'},
                'Hashtag': {'S': '#DummyHT'}
            }
        )
    ]
)
@mock.patch('tagsub.dynamodb.serialize_dynamodb_items')
def test_put(mock_serialize_dynamodb_items, item, expected_result, app, dynamodb_table):
    """
    Will include the tests for get_dynamodb_client()
    here since these functions are always used together.
    """
    with app.app_context():
        dynamodb_client = get_dynamodb_client()
        assert dynamodb_client == get_dynamodb_client()

        mock_serialize_dynamodb_items.return_value = [deepcopy(expected_result)]
        put(
            {
                'TableName': app.config.get('DYNAMODB_TABLE'),
                'Item': deepcopy(item)
            }
        )

        result = dynamodb_client.query(
            TableName=app.config.get('DYNAMODB_TABLE'),
            KeyConditionExpression='Handle = :Handle and Hashtag = :Hashtag',
            ExpressionAttributeValues={
                ':Handle': {'S': item.get('Handle')},
                ':Hashtag': {'S': item.get('Hashtag')}
            }
        )

        assert result.get('Items')[0] == expected_result
        mock_serialize_dynamodb_items.assert_called_once_with([item])
