
from flask_restx import Model, fields
from deepface_rest.config import Config

EmotionData = Model('EmotionData', {
    "angry": fields.Float(required=True),
    "disgust": fields.Float(required=True),
    "fear": fields.Float(required=True),
    "happy": fields.Float(required=True),
    "sad": fields.Float(required=True),
    "surprise": fields.Float(required=True),
    "neutral": fields.Float(required=True),
})

RegionRect = Model('RegionRect', {
    "x": fields.Integer(required=True),
    "y": fields.Integer(required=True),
    "w": fields.Integer(required=True),
    "h": fields.Integer(required=True),
})

PersonRace = Model('PersonRace', {
    "asian": fields.Float(required=True),
    "indian": fields.Float(required=True),
    "black": fields.Float(required=True),
    "white": fields.Float(required=True),
    "middle eastern": fields.Float(required=True),
    "latino hispanic": fields.Float(required=True),
})

AnalysisAttribute = Model('AnalysisAttribute', {
    "emotion": fields.Nested(EmotionData, required=False),
    "dominant_emotion": fields.String(required=False),
    "region": fields.Nested(RegionRect, required=True),
    "age": fields.Integer(required=False),
    "gender": fields.String(required=False),
    "race": fields.Nested(PersonRace, required=False),
    "dominant_race": fields.String(required=False)
})

AnalysisReponse = Model('AnalysisReponse', {
    'instance_*':  fields.Wildcard(fields.Nested(AnalysisAttribute), required=True),
    'seconds': fields.Float(required=True),
    'trx_id': fields.String(required=True),
})

AnalysisInput = Model('AnalysisInput', {
    'images': fields.List(fields.String, required=True, description="Base64 encoded images"),
    'backend': fields.String(required=False, description="Face detection and alignment backend, one of " + str(Config.BACKENDS)),
    'attributes': fields.List(fields.String, required=False, description="Facial attributes " + str(Config.ATTRIBUTES)),
})

ImagePair = Model('ImagePair', {
    'img_a': fields.String(required=True, description="Base64 encoded image"),
    'img_b': fields.String(required=True, description="Base64 encoded image")
})

VerificationInput = Model('VerificationInput', {
    'images': fields.List(fields.Nested(ImagePair), required=True, description="Base64 encoded images"),
    'model': fields.String(required=False, description="Face detection and alignment backend, one of " + str(Config.MODELS)),
    'metric': fields.String(required=False, description="Face detection and alignment backend, one of " + str(Config.METRICS)),
    'backend': fields.String(required=False, description="Face detection and alignment backend, one of " + str(Config.BACKENDS)),
})

VerificationAttribute = Model('VerificationAttribute', {
    "verified": fields.Boolean(required=True),
    "distance": fields.Float(required=True),
    "threshold": fields.Float(required=True),
    "model": fields.String(required=True),
    "backend": fields.String(required=True, attribute='detector_backend'),
    "metric": fields.String(required=True, attribute='similarity_metric')
})

VerificationReponse = Model('VerificationReponse', {
    'pair_*':  fields.Wildcard(fields.Nested(VerificationAttribute), required=True),
    'seconds': fields.Float(required=True),
    'trx_id': fields.String(required=True),
    'token_url': fields.String(required=False),
})

AuthenticationInput = Model('AuthenticationInput', {
    'userPic': fields.String(required=True, description="Base64 encoded image"),
    'tokenUrl': fields.String(required=True, description="Encrypted redirect URL, where to redirect after successful authentication."),
})

AuthenticationReponse = Model('AuthenticationReponse', {
    'authenticated': fields.Boolean(required=True),
    'seconds': fields.Float(required=True),
    'trx_id': fields.String(required=True),
    'token_url': fields.String(required=False),
})

ErrorReponse = Model('ErrorReponse', {
    'success': fields.Boolean(required=True),
    'error': fields.String(required=True),
})
