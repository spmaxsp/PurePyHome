
# Project Structure
This gives a brief overview of the project structure.


```plaintext
.
├── main.py
├── Dockerfile
├── README.md
├── LICENSE
├── requirements.txt
├── config/
│   ├── config.yaml
│   ├── entities/
│   │   ├── entities1.yaml
│   │   └── entities2.yaml
│   └── layouts/
│       ├── layout1.yaml
│       └── layout2.yaml
├── env/
│   └── ...
└── purepyhome/
    ├── core/
    │   ├── db/
    │   │   ├── sqlalchemy/
    │   │   │   ├── core.py
    │   │   │   └── __init__.py
    │   │   └── __init.py
    │   ├── mqtt.py
    │   ├── socketio.py
    │   ├── signals.py
    │   ├── utils.py
    |   ├── logger.py
    │   └── __init__.py
    ├── modules/
    │   ├── mqtt/
    │   │   ├── subscriber.py
    │   │   ├── publicher.py
    │   │   └── __init__.py
    │   ├── ui/
    │   │   ├── emitter.py
    │   │   ├── receiver.py
    │   │   └── __init__.py
    │   ├── entity_db/
    │   │   ├── entity_db.py
    │   │   ├── model.py
    │   │   └── __init__.py
    │   ├── action_phraser/
    │   │   ├── handler.py
    │   │   └── __init__.py
    │   └── __init__.py
    ├── web/
    │   ├── static/
    │   │   └── ...
    │   ├── templates/
    │   │   └── ...
    │   ├── app.py
    │   ├── ui.py
    │   └── __init__.py
    └── __init__.py`
```

## Core
This provides the main functionality of the PurePyHome project. It contains all used flask extensions and all code that the modules and web application use.

It provides the following extensions, functions and signals for managing entities:

### Extensions
- db: flask_sqlalchemy (should not be used directly - only via the core functions)
- mqtt flask-mqtt
- socketio flask-socketio

### Functions

- create_entity: Function to create an entity in the database (fires register_entity signal)
- update_entity: Function to update an entity in the database (fires update_entity signal)
- remove_entity: Function to remove an entity from the database (fires remove_entity signal)
- get_entity: Function to get an entity from the database
- get_entity_history: Function to get the history of an entity from the database

### Signals

- register_entity: Signal to register entities all over the application
- remove_entity: Signal to remove entities all over the application
- update_entity: Signal used to update entities all over the application in a standardized way

Signals are should not be fired directly. They should be used via the core functions.

## Modules
This contains the main modules that makes up the project. Modules integrate using the core functions and signals.

## Web
This contains the main flask application. 
In app.py the main flask application is created and initialized.

# Config Structures

## Entities

```yaml
<Group>:
	<Device>:
		<Device-ID>:
			Device-Type: [sensor|actor|virtual]
			Data-Type: [string|numeric|bool|color|time|date|trigger|<user_defined>]
			Keep_history: <depth>
			Data_sink:
				Mqtt:
					Topic: <Topic>
					Key: <Key>
				Conversion: [auto|replace|<user-defined>]
				Conversion_String: [on:true; off:false]
			Data_source:
				Mqtt:
					Topic: <Topic>
					Key: <Key>
				Conversion: [auto|replace|<user-defined>]
				Conversion_String: [on:true; off:false]
			Actions:
				On_change:
					…
				On_update:
					…
```	

# DB Structures

## DB-Entity

```python
id = db.Column(db.Integer, primary_key=True)
entity_id = db.Column(db.String(80), unique=True, nullable=False)
data_type = db.Column(db.String(80), nullable=False)
value = db.Column(db.String(80), nullable=True)
last_value = db.Column(db.String(80), nullable=True)
max_historic_values = db.Column(db.Integer, nullable=False)

timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
```

## DB-History

```python
id = db.Column(db.Integer, primary_key=True)
entity_id = db.Column(db.String(80), unique=True, nullable=False)
value = db.Column(db.String(80), nullable=True)
timestamp = db.Column(db.DateTime(timezone=True),  server_default=func.now())
```




