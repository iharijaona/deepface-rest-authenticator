from jwcrypto import jwt
import requests
import json
from deepface_rest.config import Config
from urllib.parse import urlparse, unquote, parse_qsl
import os
from os import path


def download_user_pics(tokenUrl: str):
    """Download user's pics from S3"""

    #: Decode the user id from the key token
    keyToken = dict(parse_qsl(urlparse(unquote(tokenUrl)).query)).get('key')
    userId = json.loads(
        jwt.JWT(jwt=keyToken).token.objects["payload"]
    ).get("sub")

    #: Get user pics list
    picsResp = requests.get(
        f'{Config.IAM_SERVER_URL}/users/{userId}/pics',
        headers={
            "Authorization": f'Bearer {Config.IAM_ACCESS_TOKEN}'
        }
    )

    #: create dir
    user_dir = os.path.join(Config.FACIAL_REGISTRY, userId)
    if not path.exists(user_dir) and not path.isdir(user_dir):
        os.makedirs(user_dir, exist_ok=True)

    #: Download the pics
    pics_path = []
    for pic_item in picsResp.json():

        picStream = requests.get(pic_item["getUrl"], stream=True)

        if picStream.status_code == 200:
            pic_item_path = path.join(
                Config.FACIAL_REGISTRY, pic_item["objectKey"]
            )
            if not path.exists(pic_item_path) or not path.isfile(pic_item_path):
                with open(pic_item_path, "wb") as pic_tmp:
                    pic_tmp.write(picStream.content)
            pics_path.append(pic_item_path)

    return pics_path
