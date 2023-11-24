from dataclasses import dataclass
from pebbleauthclient.models.User import User


@dataclass
class AuthenticatedLicenceObject:
    app: str
    id: str
    tenant_id: str
    user: User
