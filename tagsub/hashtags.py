from flask import (
    Blueprint, render_template, request, current_app, redirect, url_for
)

from tagsub.dynamodb import query, put

bp = Blueprint('hashtags', __name__)


@bp.route('/hashtags', methods=('GET', 'POST'))
def hashtags() -> str:
    """Handles functionality for the hashtags view.

    If a POST method is made, the hashtag included in the form
        is inserted into DynamoDB and then redirects to the GET.
        A GET method returns the list of hashtags for the user.

    Returns:
        The rendered template containing the hashtags.
    """
    if request.method == 'POST':
        handle = current_app.config.get('USER_HANDLE')
        hashtag = request.form.get('hashtag')
        put(
            {
                'TableName': current_app.config.get('DYNAMODB_TABLE'),
                'Item': {
                    'Handle': handle,
                    'Hashtag': hashtag
                }
            }
        )
        return redirect(url_for('hashtags'))

    """
    TODO: Implement a way to get user handle based on their token
    rather than using a config value.
    """
    user_hashtags = query(
        {
            'TableName': current_app.config.get('DYNAMODB_TABLE'),
            'KeyConditionExpression': 'Handle = :Handle',
            'ExpressionAttributeValues': {
                ':Handle': {'S': current_app.config.get('USER_HANDLE')}
            }
        }
    )
    return render_template('hashtags/hashtags.html', user_hashtags=user_hashtags)
