"""Configuration file."""
import tensorflow as tf
from dotenv import load_dotenv
from os import environ, path
import os
import warnings
import logging

load_dotenv()

tf_version = int(tf.__version__.split(".")[0])

tf.get_logger().setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class Config(object):
    """Config class."""

    # development or production
    FLASK_ENV = environ.get('DEBUG', 'development')

    TESTING = False if environ.get('TESTING') == 'False' else True

    #: DEBUG flag.
    DEBUG = False if environ.get('DEBUG') == 'False' else True

    #: Flask app name.
    APP_NAME = 'Deepface REST'

    APP_DESC = 'REST API for Face Matching, Analysis and Verification.'

    #: Flask app port
    APP_PORT = int(environ.get('APP_PORT', 8888))

    #: Flask app secret key.
    SECRET_KEY = environ.get('FLASK_SECRET_KEY', '4e0ea1bb-6702-4e74-a514-bc12bcd4810e')

    #: Face recognition models
    MODELS = ["VGG-Face", "Facenet", "Facenet512", "OpenFace",
              "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace", "Ensemble"]

    #: Similarity metrics
    METRICS = ["cosine", "euclidean", "euclidean_l2"]

    #: Face detection and alignment backend
    BACKENDS = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']

    #: Facial attributes
    ATTRIBUTES = ['emotion', 'age', 'gender', 'race']

    #: IAM API URL
    IAM_SERVER_URL = environ.get('IAM_SERVER_URL', None)

    #: IAM API URL Access Token
    IAM_ACCESS_TOKEN = environ.get('IAM_ACCESS_TOKEN', None)

    #: Token Secret
    KC_HMAC_SECRET = environ.get('KC_HMAC_SECRET', None)

    #: Token Secret
    FACIAL_REGISTRY = path.join(
        path.dirname(__file__),
        '..',
        'facial_registry'
    )
