from dataclasses import dataclass

@dataclass
class EntityStateInfo:
    entity_id: str                      # a unique string identifier for the entity

    data_type: str                      # the type of data: string, numeric, bool, color, time, date, trigger

    current_value: any                  # the current value of the entity
    last_value: any                     # the last value of the entity
    timestamp: int                      # the timestamp of the last value


@dataclass
class EntityHistoryInfo:
    entity_id: str                      # a unique string identifier for the entity

    data_type: str                      # the type of data: string, numeric, bool, color, time, date, trigger

    history: list                       # a list of historical values
    history_depth: int                  # the number of historical values to keep