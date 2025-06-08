import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

from flask import g, current_app


def get_dynamodb_client() -> boto3.client:
    """Creates a DynamoDB client using the configurations in the Flask app."""
    if 'dynamodb_client' not in g:
        g.dynamodb_client = boto3.client(
            'dynamodb',
            aws_access_key_id=current_app.config.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=current_app.config.get('AWS_SECRET_ACCESS_KEY'),
            region_name=current_app.config.get('AWS_REGION')
        )

    return g.dynamodb_client


def get_dynamodb_type_serializer() -> TypeSerializer:
    """Creates a DynamoDB type serializer."""
    if 'dynamodb_type_serializer' not in g:
        g.dynamodb_type_serializer = TypeSerializer()

    return g.dynamodb_type_serializer


def get_dynamodb_type_deserializer() -> TypeDeserializer:
    """Creates a DynamoDB type deserializer."""
    if 'dynamodb_type_deserializer' not in g:
        g.dynamodb_type_deserializer = TypeDeserializer()

    return g.dynamodb_type_deserializer


def serialize_dynamodb_items(items: list[dict[str,any]]) -> list[dict[str,any]]:
    """Serializes the specified items into DynamoDB types.

    Args:
        items: A list[dict[str,any]] to be serialized into DynamoDB types.

    Returns:
        The list of items serialized into their respective DynamoDB types.
    """
    dynamodb_type_serializer = get_dynamodb_type_serializer()
    return [
        {key: dynamodb_type_serializer.serialize(value) for key, value in attribute.items()}
        for attribute in items
    ]


def deserialize_dynamodb_items(items: list[dict[str,any]]) -> list[dict[str,any]]:
    """Deserializes the items in a DynamoDB query or scan.

    Args:
        items: The list of items returned by the DynamoDB operation.

    Returns:
        The list of items deserialized into their respective Python types.
    """
    dynamodb_type_deserializer = get_dynamodb_type_deserializer()
    return [
        {key: dynamodb_type_deserializer.deserialize(value) for key, value in attribute.items()}
        for attribute in items
    ]


def query(parameters) -> list[dict[str,any]]:
    """Queries a DynamoDB table using the specified parameters.

    Mainly acts as a passthrough to the DynamoDB client.query() method,
        but abstracts the deserialization of results so that we don't
        have to handle that in every view function that queries DynamoDB.

    Args:
        parameters: The parameters that should be used when calling
        the DynamoDB boto3 client.

    Returns:
        The list of results deserialized into their respective Python types.
    """
    dynamodb_client = get_dynamodb_client()
    query_results = dynamodb_client.query(**parameters).get('Items')

    return deserialize_dynamodb_items(query_results)


def put(parameters):
    """Puts an object to a DynamoDB table.

    Mainly acts as a passthrough to the DynamoDB client.put_item() method,
        but abstracts the serialization of the item so that we don't
        have to handle that in every view function that puts an item to DynamoDB.

    Args:
        parameters: The parameters that should be used when calling
        the DynamoDB boto3 client.
    """
    dynamodb_client = get_dynamodb_client()

    parameters['Item'] = serialize_dynamodb_items([parameters.get('Item')])[0]

    dynamodb_client.put_item(**parameters)
