from dataclasses import dataclass
from pebbleauthclient import models as UserModel


@dataclass
class AuthenticatedLicenceObject:
    app: str
    id: str
    tenant_id: str
    user: UserModel.User
