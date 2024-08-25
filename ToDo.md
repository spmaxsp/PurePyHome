# ToDo

**This is a list of stuff that needs to be done, to get the project to a first usable release.**

the list is not in any particular order, and definitely needs to be replaced by a proper roadmap.

## General
- [ ] Move Configuration to a separate folder
- [ ] Make Config folder mountable in Docker
- [x] Move the project to a python-virtualenv and add a requirements.txt
- [x] Push the project to a git repository
- [x] Move project into a Docker container
- [ ] Ability to run without MQTT server (handle connection error)
- [ ] Do a first test of the project on a real server and mqtt network

## Clean up
- [ ] Clean up the folder structure
- [ ] Properly define the functions parameters and return values
- [ ] Add proper error handling

## Features
- [ ] HTTP Request handling for entities
- [ ] Add more ui elements
- [ ] Somehow implement "trigger entities" 

## Documentation
- [ ] Add a proper license
- [ ] Add a proper installation guide
- [ ] Add a proper configuration guide for the entities
- [ ] Add a proper configuration guide for the dashboards
- [ ] Add a proper configuration guide for the main configuration


## Temporary Tasks
- [ ] Node Red integration ideas (using MQTT with purepyhome.nodered.$entityname)
- [ ] Enforce sensor and actor differentiation
- [ ] Look over dashboard code and clean up
- [ ] Get running non docker
- [ ] Looging for the Siganls (make losgs more compact -> loglevel)
- [ ] Clean up this ToDo list
- [ ] Mqtt reconnect?
- [ ] Improve Style of the Dashboard
- [ ] Style of dashboard in config?
- [ ] Read config in seperate file
