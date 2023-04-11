from deepface import DeepFace
import logging

logger = logging.getLogger(__name__)

def analyze_face(req, trx_id=0):
    """Facial Attribute Analysis"""

    resp_obj = {'success': False}

    images = []
    if "images" in list(req.keys()):
        images = req["images"]  # list

    if len(images) == 0:
        return {'success': False, 'error': 'you must pass at least one img object in your request'}, 205

    logger.info(f"Analyzing {len(images)} images")

    # ---------------------------

    detector_backend = 'opencv'

    attributes = ['emotion', 'age', 'gender', 'race']

    if "attributes" in list(req.keys()):
        attributes = req["attributes"]

    if "backend" in list(req.keys()):
        detector_backend = req["backend"]

    # ---------------------------

    try:
        resp_obj = DeepFace.analyze(
            images,
            actions=attributes,
            detector_backend=detector_backend
        )
    except Exception as err:
        logger.warn(f"Exception: {str(err)}")
        return {'success': False, 'error': str(err)}, 205

    return resp_obj, 200
