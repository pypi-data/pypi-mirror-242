# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This repository is a part of opsys automation infrastructure
* This repository is motorized stage controller implementation for motorized stage device

### How do I get set up? ###

* pip install opsys-motorized-stage

### Unit Testing

* python -m unittest -v

### Reference Links

* https://github.com/freespace/pySMC100
* https://www.newport.com/mam/celum/celum_assets/resources/SMC100CC_and_SMC100PP_-_User_Manual.pdf?3
* https://www.newport.com/mam/celum/celum_assets/resources/SMC100_-_Command_Interface_Manual.pdf?3

### Usage Example
```
### SMC100PP motorized stage controller

from opsys_motorized_stage.motor_stage_controller import MotorStageController

smc100_conn = MotorStageController()

smc100_conn.connect_stage()
smc100_conn.set_stage_home()
smc100_conn.move_abs(15, 'mm')
smc100_conn.disconnect_stage()
```