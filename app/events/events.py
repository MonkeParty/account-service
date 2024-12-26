from enum import Enum

class EventType(Enum):
    Invalid = 'erro'

    SetUserRole = 'suro'


_event_type_members = EventType._member_map_.values()
class EventTypeConstants:
    event_type_to_prefix = {}
    prefix_to_event_type = {}

    for enum in _event_type_members:
        event_type_to_prefix[enum] = enum.value
        prefix_to_event_type[enum.value] = enum


class Event:
    def __init__(self, type: EventType, data):
        self.type = type
        self.data = data

    def __str__(self) -> str:
        return f'{EventTypeConstants.event_type_to_prefix[self.type]} {self.data}'
