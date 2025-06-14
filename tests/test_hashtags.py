from copy import deepcopy
from urllib.parse import quote
import mock
import pytest


@pytest.mark.parametrize(
    'hashtags',
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
@mock.patch('tagsub.hashtags.query')
def test_hashtags(mock_query, hashtags, client, app):
    mock_query.return_value = deepcopy(hashtags)

    response = client.get('/hashtags')

    assert response.status == '200 OK'
    assert response.request.path == '/hashtags'
    assert response.request.method == 'GET'
    assert app.config.get('USER_HANDLE').encode() in response.data
    if len(hashtags) > 0:
        for hashtag in hashtags:
            assert hashtag.get('Hashtag').encode() in response.data

    mock_query.assert_called_once_with(
        {
            'TableName': app.config.get('DYNAMODB_TABLE'),
            'KeyConditionExpression': 'Handle = :Handle',
            'ExpressionAttributeValues': {
                ':Handle': {'S': app.config.get('USER_HANDLE')}
            }
        }
    )


@pytest.mark.parametrize(
    'new_hashtag,hashtags',
    [
        (
            {
                'hashtag': '#DummyHT4'
            },
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
                },
                {
                    'Handle': '@TestUser',
                    'Hashtag': '#DummyHT4'
                }
            ]
        )
    ]
)
@mock.patch('tagsub.hashtags.query')
@mock.patch('tagsub.hashtags.put')
def test_create_hashtag(mock_put, mock_query, new_hashtag, hashtags, client, app):
    mock_query.return_value = deepcopy(hashtags)

    response = client.post('/hashtag', data=new_hashtag, follow_redirects=True)

    assert response.status == '200 OK'
    assert response.request.path == '/hashtags'
    assert response.request.method == 'GET'
    assert app.config.get('USER_HANDLE').encode() in response.data
    if len(hashtags) > 0:
        for hashtag in hashtags:
            assert hashtag.get('Hashtag').encode() in response.data

    mock_query.assert_called_once_with(
        {
            'TableName': app.config.get('DYNAMODB_TABLE'),
            'KeyConditionExpression': 'Handle = :Handle',
            'ExpressionAttributeValues': {
                ':Handle': {'S': app.config.get('USER_HANDLE')}
            }
        }
    )
    mock_put.assert_called_once_with(
        {
            'TableName': app.config.get('DYNAMODB_TABLE'),
            'Item': {
                'Handle': app.config.get('USER_HANDLE'),
                'Hashtag': new_hashtag.get('hashtag')
            }
        }
    )


@pytest.mark.parametrize(
    'hashtag_to_delete,hashtags',
    [
        (
            '#DummyHT4',
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
        )
    ]
)
@mock.patch('tagsub.hashtags.query')
@mock.patch('tagsub.hashtags.delete')
def test_delete_hashtag(mock_delete, mock_query, hashtag_to_delete, hashtags, client, app):
    mock_query.return_value = deepcopy(hashtags)

    response = client.post(
        f'/hashtag/{quote(hashtag_to_delete)}/delete',
        follow_redirects=True
    )

    assert response.status == '200 OK'
    assert response.request.path == '/hashtags'
    assert response.request.method == 'GET'
    assert app.config.get('USER_HANDLE').encode() in response.data
    if len(hashtags) > 0:
        for hashtag in hashtags:
            assert hashtag.get('Hashtag').encode() in response.data

    mock_query.assert_called_once_with(
        {
            'TableName': app.config.get('DYNAMODB_TABLE'),
            'KeyConditionExpression': 'Handle = :Handle',
            'ExpressionAttributeValues': {
                ':Handle': {'S': app.config.get('USER_HANDLE')}
            }
        }
    )
    mock_delete.assert_called_once_with(
        {
            'TableName': app.config.get('DYNAMODB_TABLE'),
            'Key': {
                'Handle': app.config.get('USER_HANDLE'),
                'Hashtag': hashtag_to_delete
            }
        }
    )
