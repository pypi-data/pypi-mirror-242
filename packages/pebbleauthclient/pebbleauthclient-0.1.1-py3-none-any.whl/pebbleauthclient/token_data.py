from pebbleauthclient.datatypes.AuthenticatedLicenceObject import AuthenticatedLicenceObject
from pebbleauthclient.datatypes.PebbleTokenData import PebbleTokenData
from pebbleauthclient.datatypes.UserObject import UserObject
from pebbleauthclient.models.User import User


def get_licence_object_from_token_data(token_data: PebbleTokenData) -> AuthenticatedLicenceObject:
    user = User(
        UserObject(
            username=token_data.sub,
            roles=token_data.roles,
            level=token_data.lv,
            display_name=token_data.name
        )
    )

    return AuthenticatedLicenceObject(
        app=token_data.aud,
        id=token_data.iss,
        tenant_id=token_data.tid,
        user=user
    )


def get_token_data_from_jwt_payload(jwt_payload: dict, token: str) -> PebbleTokenData:

    claims = ('aud', 'iss', 'tid', 'sub', 'roles', 'lv', 'name', 'iat', 'exp')

    for claim in claims:
        if claim not in jwt_payload:
            jwt_payload[claim] = None

    return PebbleTokenData(
        aud=jwt_payload['aud'],
        iss=jwt_payload['iss'],
        tid=jwt_payload['tid'],
        sub=jwt_payload['sub'],
        roles=jwt_payload['roles'],
        lv=jwt_payload['lv'],
        name=jwt_payload['name'],
        iat=jwt_payload['iat'],
        exp=jwt_payload['exp'],
        token=token
    )
