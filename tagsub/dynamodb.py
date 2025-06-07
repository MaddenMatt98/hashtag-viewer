import boto3
from boto3.dynamodb.types import TypeDeserializer

from flask import g, current_app


def get_dynamodb_client() -> boto3.client:
    """Creates a DynamoDB client using the configurations in the Flask app."""
    if 'dynamodb_client' not in g:
        g.dynamodb_client = boto3.client(
            'dynamodb',
            aws_access_key_id=current_app.config.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=current_app.config.get('AWS_SECRET_ACCESS_KEY'),
            aws_session_token=current_app.config.get('AWS_SESSION_TOKEN'),
            region_name=current_app.config.get('AWS_REGION')
        )

    return g.dynamodb_client


def get_dynamodb_type_deserializer() -> TypeDeserializer:
    """Creates a DynamoDB type deserializer."""
    if 'dynamodb_type_deserializer' not in g:
        g.dynamodb_type_deserializer = TypeDeserializer()

    return g.dynamodb_type_deserializer


def deserialize_dynamodb_results(results: list[dict[str,any]]) -> list[dict[str,any]]:
    """Deserializes the results from a DynamoDB query or scan.

    Args:
        results: The list of results returned by the DynamoDB operation.

    Returns:
        The list of results deserialized into their respective Python types.
    """
    dynamodb_type_deserializer = get_dynamodb_type_deserializer()
    return [
        {key: dynamodb_type_deserializer.deserialize(value) for key, value in result.items()}
        for result in results
    ]


def scan_dynamodb_table() -> list[dict[str,any]]:
    """Scans a DynamoDB table and returns there results."""
    dynamodb_client = get_dynamodb_client()
    scan_results = dynamodb_client.scan(
        TableName=current_app.config.get('DYNAMODB_TABLE')
    ).get('Items')

    return deserialize_dynamodb_results(scan_results)
