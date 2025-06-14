from copy import deepcopy

import mock
import pytest


@pytest.mark.parametrize(
    'method,new_hashtag,hashtags',
    [
        (
            'GET',
            None,
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
            'GET',
            None,
            []
        ),
        (
            'POST',
            {
                'Hashtag': '#DummyHT4'
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
def test_hashtags(mock_put, mock_query, method, new_hashtag, hashtags, client, app):
    mock_query.return_value = deepcopy(hashtags)

    if method == 'POST':
        response = client.post('/hashtags', data=new_hashtag, follow_redirects=True)
    else:
        response = client.get('/hashtags')

    assert response.status == '200 OK'
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
    if method == 'POST':
        mock_put.assert_called_once_with(
            {
                'TableName': app.config.get('DYNAMODB_TABLE'),
                'Item': {
                    'Handle': app.config.get('USER_HANDLE'),
                    'Hashtag': new_hashtag.get('Hashtag')
                }
            }
        )
    else:
        mock_put.assert_not_called()
