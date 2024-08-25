
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
In the core folder the main extensions are created. This makes the core extensions available all over the project, by importing them from core. 

Also most of the core extensions put into wrappers, so that they can be easily extended and tailored to the needs of the project.

### Signals
This contains the signals that are used to communicate between the different modules.

### Utils
This contains some utility functions that are used throughout the project.

## Modules
This contains the main code that makes up the project. The code is split into different modules, that can be easily replaced or extended.

## Web
This contains the main flask application. 
In app.py the main flask application is created and initialized.

In ui.py the main UI is created. It provides the main routes and blueprints for the UI.