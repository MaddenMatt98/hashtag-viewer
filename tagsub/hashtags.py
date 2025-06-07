from flask import Blueprint, render_template

from tagsub.dynamodb import scan_dynamodb_table

bp = Blueprint('hashtags', __name__)


@bp.route('/hashtags')
def view_hashtags() -> str:
    """Lists all of the hashtags in the database.

    Retrieves a list of hashtags from the DynamoDB table and renders an
        HTML template using them.

    Returns:
        The rendered template containing the hashtags.
    """
    """
    TODO: change this to a query that fetches the user id from the
    Authorization header once authentication is implemented.  This
    will allow securely supporting multiple users.
    """
    hashtags = scan_dynamodb_table()
    return render_template('hashtags/hashtags.html', hashtags=hashtags)
