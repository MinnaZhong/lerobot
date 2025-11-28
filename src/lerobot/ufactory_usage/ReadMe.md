# For UFACTORY data collection usage

Please first install additional dependencies into your environment by running:
```
$ pip install -r requirements_extra.txt
```
This would install gello and space mouse related modules. Also, make sure you have [`xArm-Python-SDK`](https://github.com/xArm-Developer/xArm-Python-SDK) installed.

## 1. GELLO for xArm7: 
By running the command above, `gello_software` package will be installed locally under `./src` folder. To ensure proper configuration of the dummy robot, dynamixel motor offset of each joint on the dummy robot must be confirmed from `gello_get_offset.py` script inside this repository. Please Study the usage of GELLO carefully before continue working with real xArm7. 

Note: Gello would also require additional dependencies running its scripts. Consider switching to another `conda env` (like `gello`) with gello offset check.

To get gello offset:   

Setup and power on the gello dummy robot, hold it with a **known real joint configuration** (use [`0, 0, 0, 90, 0, 90, 0`] degrees as example):

```
$ conda activate gello #(configured according to gello ReadMe installation requirements)
$ python gello_get_offset.py --port /dev/ttyUSB0 --start_joints 0 0 0 1.5708 0 1.5708 0 --joint_signs 1 1 1 1 1 1 1
```

Then the output result can be set to the `gello_xarm7` configuration. 


## 2. Space Mouse:

The space mouse currently is configured as 2D control (in XY plane) for Push T block task, if you need more freedom, check and edit the interface in `teleoperators/space_mouse/space_mouse.py`.  

## 3. Lerobot Data Recording with above devices:
Please use provided `record_uf_edit.py` script in this directory instead of lerobot_record.py in scripts folder. We have made modifications for space mouse data collection (delta command to absolute command) and enabled using external yaml file as flexible configuration. Check the two `*_record_config.yaml` files here and change the filename used in `record_uf_edit.py`.

## 4. Notices:
Users need to **study the whole codebase thoroughly**, and understand about relevant configuration parameters, since the configurations written in the code are not for all use cases and set-ups, it is the users job to study the code or theories to get good knowledge about them and modify/tune on their own.