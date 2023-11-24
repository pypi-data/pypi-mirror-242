from typing import Sequence
from pebbleauthclient.datatypes.UserObject import UserObject


class User(UserObject):

    def __init__(self, user: UserObject):
        self.username: str = user.username
        self.display_name: str = user.display_name
        self.level: int = user.level
        self.roles: Sequence[str] = user.roles

    def has_role(self, role: str) -> bool:
        """
        Check if the user has the argument specified role.
        :param role: str
        :return: bool
        """
        if self.roles:
            return role in self.roles
        return False
