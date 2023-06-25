from typing import TypedDict, NamedTuple


class User(TypedDict):
    email: str


class NotificationPattern(NamedTuple):
    id: str
    pattern_file: str
    actual_time: int
    settings_: dict
