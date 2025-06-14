from flask import (
    Blueprint, render_template, request, current_app, redirect, url_for
)

from tagsub.dynamodb import query, put, delete

bp = Blueprint('hashtags', __name__)


@bp.route('/hashtags', methods=['GET'])
def hashtags() -> str:
    """Handles functionality for the hashtags view.

    GETs the list of hashtags for the current user.

    Returns:
        The rendered template containing the hashtags.
    """
    """
    TODO: Implement a way to get user handle based on their token
    rather than using a config value.
    """
    handle = current_app.config.get('USER_HANDLE')
    user_hashtags = query(
        {
            'TableName': current_app.config.get('DYNAMODB_TABLE'),
            'KeyConditionExpression': 'Handle = :Handle',
            'ExpressionAttributeValues': {
                ':Handle': {'S': handle}
            }
        }
    )
    return render_template(
        'hashtags/hashtags.html',
        user_handle=handle,
        user_hashtags=user_hashtags
    )


@bp.route('/hashtag', methods=['POST'])
def create_hashtag():
    """Adds new hashtags to the database.

    Puts the entered hashtag into the DynamoDB table.

    Returns:
        Redirects back to GET /hashtags.
    """
    put(
        {
            'TableName': current_app.config.get('DYNAMODB_TABLE'),
            'Item': {
                'Handle': current_app.config.get('USER_HANDLE'),
                'Hashtag': request.form.get('hashtag')
            }
        }
    )
    return redirect(url_for('hashtags'))


@bp.route('/hashtag/<string:hashtag>/delete', methods=['POST'])
def delete_hashtag(hashtag):
    """Deletes the specified hashtag from the database.

    Deletes the specified hashtag from the database.

    Returns:
        Redirects back to GET /hashtags.
    """
    delete(
        {
            'TableName': current_app.config.get('DYNAMODB_TABLE'),
            'Key': {
                'Handle': current_app.config.get('USER_HANDLE'),
                'Hashtag': hashtag
            }
        }
    )
    return redirect(url_for('hashtags'))
