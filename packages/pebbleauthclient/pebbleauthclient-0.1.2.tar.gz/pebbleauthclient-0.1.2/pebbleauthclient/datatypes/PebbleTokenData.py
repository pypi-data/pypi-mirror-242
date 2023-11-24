import dataclasses
from typing import Sequence


@dataclasses.dataclass
class PebbleTokenData:
    aud: str
    exp: int
    iat: int
    iss: str
    lv: int
    name: str
    roles: Sequence[str];
    sub: str
    tid: str
    token: str
