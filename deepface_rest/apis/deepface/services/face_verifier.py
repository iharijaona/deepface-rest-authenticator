
from deepface import DeepFace
import logging

logger = logging.getLogger(__name__)

def verify_face(req, trx_id=0):
    """Verify face similarity"""

    resp_obj = {'success': False}

    model_name = "VGG-Face"
    distance_metric = "cosine"
    detector_backend = "retinaface"

    if "model" in list(req.keys()):
        model_name = req["model"]

    if "metric" in list(req.keys()):
        distance_metric = req["metric"]

    if "backend" in list(req.keys()):
        detector_backend = req["backend"]

    # ----------------------

    images = []

    if "images" in list(req.keys()):

        raw_content = req["images"]  # list

        for item in raw_content:  # item is in type of dict
            img1 = item["img_a"]
            img2 = item["img_b"]

            validate_img1 = False
            if len(img1) > 11 and img1[0:11] == "data:image/":
                validate_img1 = True

            validate_img2 = False
            if len(img2) > 11 and img2[0:11] == "data:image/":
                validate_img2 = True

            if validate_img1 != True or validate_img2 != True:
                return {'success': False, 'error': 'you must pass both img1 and img2 as base64 encoded string'}, 205

            images.append([img1, img2])

    # --------------------------

    if len(images) == 0:
        return {'success': False, 'error': 'you must pass at least one img object in your request'}, 205

    logger.info(f"Input request of {trx_id}, has {len(images)} pairs to verify")

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

    except Exception as err:
        logger.warn(f"Exception: {str(err)}")
        return {'success': False, 'error': str(err)}, 205

    return resp_obj, 200
