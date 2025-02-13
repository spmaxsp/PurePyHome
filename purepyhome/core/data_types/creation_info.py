from dataclasses import dataclass

ENTITY_DATA_TYPES = ["string", "numeric", "bool", "color", "time", "date", "trigger"]

ENTITY_DEVICE_TYPES = ["sensor", "actor", "virtual"]

ENTITY_DATA_SOURCE_TYPES = ["mqtt", "none"]

ENTITY_DATA_SINK_TYPES = ["mqtt", "none"]

@dataclass
class EntityDataSourceInfo:
    source_type: str
    source_info: dict
    converter_name: str
    converter_info: dict

@dataclass
class EntityDataSinkInfo:
    sink_type: str
    sink_info: dict
    converter_name: str
    converter_info: dict


@dataclass
class EntityCreationInfo:
    entity_id: str                      # a unique string identifier for the entity

    device_type: str                    # the type of device: sensor, actuator, virtual
    data_type: str                      # the type of data: string, numeric, bool, color, time, date, trigger
    history_depth: int                  # the number of historical values to keep

    data_source: EntityDataSourceInfo   # the data source information
    data_sink: EntityDataSinkInfo       # the data sink information

    node_red_mqtt_link: bool            # whether to link the entity to Node-RED via a MQTT topic (eg. purepyhome.node-link.<entity_id>.<write/read>)

    actions: dict


def check_entity_creation_info(entity_creation_info: EntityCreationInfo):

    if entity_creation_info.entity_id is None or entity_creation_info.device_type is None or entity_creation_info.data_type is None or entity_creation_info.history_depth is None or entity_creation_info.data_source is None or entity_creation_info.data_sink is None or entity_creation_info.node_red_mqtt_link is None or entity_creation_info.actions is None:
        raise ValueError(f'Invalid entity creation info: {entity_creation_info} Value cannot be None')

    if not isinstance(entity_creation_info.entity_id, str):
        raise ValueError(f'Invalid entity id: {entity_creation_info.entity_id}')

    if len(entity_creation_info.entity_id) == 0:
        raise ValueError(f'Invalid entity id: {entity_creation_info.entity_id}')

    if entity_creation_info.device_type not in ENTITY_DEVICE_TYPES:
        raise ValueError(f'Invalid device type: {entity_creation_info.device_type}')

    if entity_creation_info.data_type not in ENTITY_DATA_TYPES:
        raise ValueError(f'Invalid data type: {entity_creation_info.data_type}')

    if not isinstance(entity_creation_info.history_depth, int):
        raise ValueError(f'Invalid history depth: {entity_creation_info.history_depth}')

    if entity_creation_info.history_depth < 0:
        raise ValueError(f'Invalid history depth: {entity_creation_info.history_depth}')
    
    if entity_creation_info.data_source.source_type not in ENTITY_DATA_SOURCE_TYPES:
        raise ValueError(f'Invalid data source type: {entity_creation_info.data_source.source_type}')
    
    if entity_creation_info.data_sink.sink_type not in ENTITY_DATA_SINK_TYPES:
        raise ValueError(f'Invalid data sink type: {entity_creation_info.data_sink.sink_type}')

    # Sensor entity must have a data source and cannot have a data sink
    if entity_creation_info.device_type == 'sensor':
        if entity_creation_info.data_source.source_type == 'none':
            raise ValueError(f'Sensor entity must have a data source')
        if entity_creation_info.data_sink.sink_type != 'none':
            raise ValueError(f'Sensor entity cannot have a data sink')
        
    # Actuator entity must have a data sink and can have a data source
    if entity_creation_info.device_type == 'actuator':
        if entity_creation_info.data_sink.sink_type == 'none':
            raise ValueError(f'Actuator entity must have a data sink')
        
    # Virtual entity cannot have a data source or data sink
    if entity_creation_info.device_type == 'virtual':
        if entity_creation_info.data_source.source_type != 'none':
            raise ValueError(f'Virtual entity cannot have a data source')
        if entity_creation_info.data_sink.sink_type != 'none':
            raise ValueError(f'Virtual entity cannot have a data sink')
