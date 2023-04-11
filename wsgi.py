"""The entry point for the App Server."""

import deepface_rest
from os import environ

#: The default app, exported to be used by gunicorn.
app = deepface_rest.create_app()

if __name__ == '__main__':

    environ['FLASK_ENV'] = 'development'

    app.run("0.0.0.0", deepface_rest.Config.APP_PORT, debug=True)
