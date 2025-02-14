from dataclasses import dataclass

@dataclass
class EntityUpdateInfo:
    entity_id: str                      # a unique string identifier for the entity

    data_type: str                      # the type of data: string, numeric, bool, color, time, date, trigger

    new_value: any                      # the new value of the entity

    sender: str                         # the sender that requests the update
    callstack: list

