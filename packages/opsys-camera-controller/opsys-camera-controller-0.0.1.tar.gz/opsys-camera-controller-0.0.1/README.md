# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This repository is a part of opsys automation infrastructure
* This repository is camera controller implementation for Allied/IDS cameras

### How do I get set up? ###

* pip install opsys-camera-controller

### Unit Testing

* python -m unittest -v

### Reference Links

* Allied Vision - R:\Lidar\Dima\camera\Vimba Python Manual.pdf
* R:\Lidar\Dima\Software\Vimba_v6.0_Windows.exe
* https://www.1stvision.com/cameras/IDS/IDS-manuals/uEye_Manual/index.html
* https://cdn.graftek.com/system/files/16087/original/AVT_Alvium_Features_Reference.pdf
* R:\Lidar\Dima\Software\ids-software-suite-win-4.96.1.zip
* R:\Lidar\Dima\Software\ids-peak-win-2.3.0.0.zip

### Specifications

* IDS "ImportError: could not find any library for ueye_api (DLL_PATH: unset)" resolution: copy "ueye_api_64.dll" to "C:\Windows\System32" directory

### Usage Example
```
from opsys_camera_controller.camera_controller import CameraController

camera = CameraController(camera_type='Allied')

camera.connect()
image = camera.get_image()
camera.save_image()
camera.set_parameter('gain', 20.0)
camera.record(record_time=30)
```