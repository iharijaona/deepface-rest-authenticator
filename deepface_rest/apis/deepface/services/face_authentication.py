
from deepface import DeepFace
import logging

logger = logging.getLogger(__name__)

def authenticate_face(user_pic, pic_registry, trx_id=0):
    """Authenticate user face"""

    resp_obj = {'success': False}

    model_name = "Facenet512"
    distance_metric = "euclidean_l2"
    detector_backend = "retinaface"

    # ----------------------

    if len(user_pic) <= 11 or user_pic[0:11] != "data:image/":
        return {'success': False, 'error': 'you must pass userPic as base64 encoded string'}, 205

    # --------------------------

    images = [[user_pic, pic_path] for pic_path in pic_registry]

    if len(images) == 0:
        return {'success': False, 'error': 'User must has at least one picture in the facial registry'}, 205

    logger.info(f"[{trx_id}] User has {len(images)} pairs to verify")

    # --------------------------

    try:
        resp_obj = DeepFace.verify(
            images,
            model_name=model_name,
            distance_metric=distance_metric,
            detector_backend=detector_backend
        )

        if model_name == "Ensemble":  # issue 198.
            for key in resp_obj:  # issue 198.
                resp_obj[key]['verified'] = bool(resp_obj[key]['verified'])

        authImgs = [*filter(
            lambda itemRes: itemRes.get("verified"), resp_obj.values()
        )]

        distance_avg = sum([resItm["distance"]
                           for resItm in authImgs]) / len(authImgs)

        resp_obj = {
            'authenticated': bool(len(authImgs) >= 2 and distance_avg <= 0.8),
            "distance": distance_avg,
        }

    except Exception as err:
        logger.warn(f"Exception: {str(err)}")
        return {'success': False, 'error': str(err)}, 205

    return resp_obj, 200
