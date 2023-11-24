from pebbleauthclient.models.AuthenticatedLicence import AuthenticatedLicence
from pebbleauthclient.datatypes.PebbleTokenData import PebbleTokenData
from pebbleauthclient.models.User import User
from pebbleauthclient.token_data import get_licence_object_from_token_data


class PebbleAuthToken(PebbleTokenData):

    def __init__(self, token_data: PebbleTokenData):
        self.aud = token_data.aud
        self.exp = token_data.exp
        self.iat = token_data.iat
        self.iss = token_data.iss
        self.lv = token_data.lv
        self.name = token_data.name
        self.roles = token_data.roles
        self.sub = token_data.sub
        self.tid = token_data.tid
        self.token = token_data.token

    def get_authenticated_licence(self) -> AuthenticatedLicence:
        licence = AuthenticatedLicence(get_licence_object_from_token_data(self))
        return licence

    def get_user(self) -> User:
        return self.get_authenticated_licence().get_user()
