from moto import mock_aws
import pytest

import boto3

from tagsub import create_app


TEST_CONFIG = {
    'TESTING': True,
    'SECRET_KEY': 'TEST',
    'AWS_ACCESS_KEY_ID': 'DUMMYVALUEFORACCESSKEYID',
    'AWS_SECRET_ACCESS_KEY': 'DUMMYVALUEFORSECRETACCESSKEY',
    'AWS_SESSION_TOKEN': 'DUMMYVALUEFORSESSIONTOKEN',
    'AWS_REGION': 'us-east-2',
    'DYNAMODB_TABLE': 'DummyDynamoTable',
    'USER_HANDLE': '@TestUser'
}

TEST_HASHTAGS = ['#TestHashtag1', '#TestHashtag2', '#TestHashtag3']


@pytest.fixture
def app():
    """
    Create app for testing, containing dummy values since any
    integrations should be mocked.
    """
    test_app = create_app(TEST_CONFIG)
    yield test_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def dynamodb_table():
    """Sets up a mocked DynamoDB table that can be used by tests."""
    with mock_aws():
        dynamodb_client = boto3.client(
            'dynamodb',
            region_name=TEST_CONFIG.get('AWS_REGION')
        )

        dynamodb_client.create_table(
            TableName=TEST_CONFIG.get('DYNAMODB_TABLE'),
            KeySchema=[
                {
                    'AttributeName': 'Handle',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'Hashtag',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'Handle',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Hashtag',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        yield
