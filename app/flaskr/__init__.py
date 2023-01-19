import os
from flask import Flask


def create_app():
    """Create and configure app."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        HOST=os.environ.get('HOST'),
        FLASK_DEBUG=os.environ.get('DEBUG'))
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from .views import view

        app.register_blueprint(view, url_prefix="/")

    return app
