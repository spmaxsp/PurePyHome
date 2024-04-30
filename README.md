![purepyhome_logo_wide_vector](https://github.com/spmaxsp/PurePyHome/assets/75380717/4b1a52f6-60a6-4490-89a1-3d815717f442)

# PurePy Home
This project attempts to create a simple smarthome system using only Python and HTML. 
The server runs on an eventlet server with a Flask application. 
The system is completely configured using YAML files.

*The project is currently in the prototype stage. 
While most of the functionality is implemented, it needs to be cleaned up, tested and documented. 
A lot of features are still missing to make it competitive with other smarthome systems.*

**Also Note:** *While the project aims to be a complete standalone system like Node-Red or Homeastistent, I recommend using it together with Node-Red (at least for the current state of development). Node-Red is a great addition to this project and offers many features like data conversion or other modules/sensors that are not implemented yet.*

## Motivation
The obvious question is why create another smarthome system, when there are already so many out there? Especially with competitors like Home Assistant, OpenHAB, or Node-Red, it seems like a waste of time to create another one.

The simple main reason is, that every solution out there somehow has something that I don't like.
- Home Assistant is a great system, but I don't like the way how its configured. My biggest problem is how its somehow moving away from the yaml configuration to a more gui based configuration, while giving the user no control over the entities.
Might be a personal preference and definitely something to argue about.
- Node-Red is a great tool. I especially like the way how the flows are created. Sadly it is not that easy to create a nice UI with it.

So the goal of this project is to create a smarthome system that can be easily configured using only yaml files. I also try to keep it as minimalist as possible.
This solution is definitely not for everybody. Especially the minimalistic and extremely flexible approach definitely makes for a steep learning curve.

The solution is definitely tailored to the "I want full control and configure everything myself" type of person.

## Overview
The server consists of e few modular parts:
- The UI web-interface written in plain HTML, CSS and JS
- A socket server for communication with the UI
- A MQTT client for communication with the devices
- A device manager for managing updating and controlling the devices
- A db for storing the devices and their states

The plan is to keep it as modular as possible, so that the different parts can be easily replaced or extended.

## Installation
This needs to be added later... The goal would be to have a docker image available for easy installation.

## Configuration
The configuration is done using only YAML files. The configuration files are located in the `./config` folder.

### Main Configuration
The main configuration is done trough the `config.yaml` file. This file contains the following fields:	
- `mqtt`: The configuration for the MQTT client
    - `broker_url`: The URL of the MQTT broker
    - `broker_port`: The port of the MQTT broker
    - `username`: The username for the MQTT broker
    - `password`: The password for the MQTT broker
    - `keepalive`: The keepalive time for the MQTT client
    - `tls_enabled`: If the connection should be encrypted
- `ui`: The configuration for the UI:
    here the different dashboards and ui-pages are defined
- `entities`: The configuration for the devices: 
    here the path to the entities files are listed. The entities files contain the configurations for the devices.

### Entities Configuration
TODO

### Dashboard Configuration
TODO

## Rodamap
Features planned for implementation in the near future are documented in the [ToDo](./ToDo.md) file.
As far as the far future is concerned, a proper roadmap will follow.

## License
This project is licensed under the MIT licence - see the [LICENSE](./LICENSE) file for details.
