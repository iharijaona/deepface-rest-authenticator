from jwcrypto import jwt, jwk
from urllib.parse import urlparse, unquote
from deepface_rest.config import Config


def encode_app_token(tokenUrl: str):
    """Create token and Sign it with the shared HMAC sercret shared between 
    keycloak and this facial authenticator app
    """

    key = jwk.JWK(k=Config.KC_HMAC_SECRET, kty="oct")

    token = jwt.JWT(
        header={"alg": "HS256"},
        claims={"isAuthenticated": True}
    )
    token.make_signed_token(key)

    return unquote(urlparse(unquote(tokenUrl)).geturl()).replace(
        "{APP_TOKEN}", token.serialize()
    )
