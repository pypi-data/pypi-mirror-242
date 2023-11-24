import jwt
import json

from errors import NotFoundJWKError, NoAlgorithmProvidedError
from key import get_jwk_set
from models.PebbleAuthToken import PebbleAuthToken
from token_data import get_token_data_from_jwt_payload


def auth(token: str) -> PebbleAuthToken:
    """
    Authenticate a provided token into and return a valid PebbleAuthToken object
    :param token: str
    :return: PebbleAuthToken
    """
    jwks = get_jwk_set()

    kid = jwt.get_unverified_header(token).get('kid')

    key = None
    jwk = None

    for j in jwks['keys']:
        if j['kid'] == kid:
            key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(j))
            jwk = j
            break

    if not key:
        raise NotFoundJWKError(kid)

    if "alg" not in jwk:
        raise NoAlgorithmProvidedError(kid)

    data = jwt.decode(
        jwt=token,
        key=key,
        algorithms=[jwk['alg']],
        options={
            "verify_aud": False,
            "verify_iss": False
        }
    )

    token_data = get_token_data_from_jwt_payload(data, token)

    return PebbleAuthToken(token_data)
