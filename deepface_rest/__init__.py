# pylint: disable=missing-docstring


from .config import Config


def create_app():
    """Instantiation of the flask application"""

    from flask import Flask, request
    from flask_cors import CORS
    import logging
    # import eventlet

    logging.getLogger('flask_cors').level = logging.DEBUG

    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['ERROR_404_HELP'] = False
    app.url_map.strict_slashes = False

    #: Configure app extensions
    from .ext.fjson import fjson
    fjson.init_app(app)

    #: Enable CORS
    CORS(app, resources={r'.*': {'origins': '*'}}, origins="*")

    from .apis.deepface import api as api_deepface

    app.register_blueprint(api_deepface)

    @app.before_request
    def before_request():
        _address = request.environ.get(
            'HTTP_X_FORWARDED_FOR') or request.remote_addr
        app.logger.info(f'{_address} -> {request.method} {request.path}')

    @app.after_request
    def after_request(response):
        headers = {
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Headers',
             'User-Agent,Cache-Control,Content-Type,Authorization'),
            ('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS'),
            ('Access-Control-Expose-Headers',
             'Content-Length,Content-Disposition,Content-Range')
        }
        [response.headers.add(*header) for header in headers]
        return response

    return app
