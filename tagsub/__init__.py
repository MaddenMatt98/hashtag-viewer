from flask import Flask


def create_app(test_config=None):
    """App factory for a simple Flask app.

    Args:
        test_config: Optional.  Can be provided to control configurations
            during testing.

    Returns:
        The created Flask app.  
    """
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load testing config if it is passed in.
        app.config.from_mapping(test_config)

    from . import hashtags
    app.register_blueprint(hashtags.bp)
    app.add_url_rule('/', endpoint='hashtags')

    return app
