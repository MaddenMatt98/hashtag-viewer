"""
Testing utilities for tests that need DynamoDB data
set up.
"""


def set_up_dynamodb_data(dynamodb_client, table_name, test_data):
    for item in test_data:
        dynamodb_client.put_item(
            TableName=table_name,
            Item={
                'Handle': {'S': item.get('Handle')},
                'Hashtag': {'S': item.get('Hashtag')}
            }
        )
