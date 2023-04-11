import time
import uuid
from flask_json import as_json
from flask import Blueprint, request
from .services import analyze_face, encode_app_token, verify_face, download_user_pics, authenticate_face

api = Blueprint(
    'deepface', __name__,
    url_prefix='/df'
)


@api.route('/analyze', methods=['POST'])
@as_json
def post_analyze_face():
    """Facial attribute analysis"""
    tic = time.time()
    trx_id = uuid.uuid4()

    resp_obj, status_code = analyze_face(request.json, trx_id)

    toc = time.time()

    resp_obj["trx_id"] = str(trx_id)
    resp_obj["seconds"] = toc-tic

    return resp_obj, status_code


@api.route('/verify', methods=['POST'])
@as_json
def post_verify_face():
    """Verify face similarity"""

    tic = time.time()
    trx_id = uuid.uuid4()

    resp_obj, status_code = verify_face(request.json, trx_id)

    toc = time.time()

    resp_obj["trx_id"] = str(trx_id)
    resp_obj["seconds"] = toc-tic

    return resp_obj, status_code


@api.route('/authenticate', methods=['POST'])
@as_json
def post_authenticate_face():
    """External face authenticator"""

    tic = time.time()
    trx_id = uuid.uuid4()

    pic_registry = download_user_pics(request.json["tokenUrl"])

    resp_obj, status_code = authenticate_face(
        request.json["userPic"],
        pic_registry,
        trx_id
    )

    toc = time.time()

    resp_obj["trx_id"] = str(trx_id)
    resp_obj["seconds"] = toc-tic
    resp_obj["token_url"] = encode_app_token(
        request.json["tokenUrl"]
    ) if resp_obj["authenticated"] else None

    return resp_obj, status_code
