# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This repository is a part of opsys automation infrastructure
* This repository is gimbal controller implementation for Newmark/Thorlabs gimbals with ATEN RS-232 to USB adapter

### How do I get set up? ###

* pip install opsys-gimbal-controller

### Unit Testing

* python -m unittest -v

### Usage Example
```
from opsys_gimbal_controller.gimbal_controller import GimbalController

gimbal = GimbalController(motor_type="Newmark")

gimbal.connect_gimbal()
gimbal.setup_configs()
gimbal.set_gimbal_home()
gimbal.move_gimbal_abs(axis='X', angle=-30)
gimbal.disconnect_gimbal()
```