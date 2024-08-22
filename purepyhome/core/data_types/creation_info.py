from dataclasses import dataclass

ENTITY_DATA_TYPES = ["string", "numeric", "bool", "color", "time", "date", "trigger"]

ENTITY_DEVICE_TYPES = ["sensor", "actuator", "virtual"]

ENTITY_DATA_SOURCE_TYPES = ["mqtt", "none"]

ENTITY_DATA_SINK_TYPES = ["mqtt", "none"]

@dataclass
class EntityDataSourceInfo:
    source_type: str
    source_info: dict
    conversion_type: str
    conversion_str: str

@dataclass
class EntityDataSinkInfo:
    sink_type: str
    sink_info: dict
    conversion_type: str
    conversion_str: str


@dataclass
class EntityCreationInfo:
    entity_id: str

    device_type: str
    data_type: str
    history_depth: int

    data_source: EntityDataSourceInfo
    data_sink: EntityDataSinkInfo

    actions: dict