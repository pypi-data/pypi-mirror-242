import dataclasses
from typing import Sequence


@dataclasses.dataclass
class UserObject:
    username: str
    display_name: str
    level: int
    roles: Sequence[str]
