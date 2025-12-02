# For UFACTORY data collection usage

Please first install additional dependencies into your environment by running:
```
$ pip install -r requirements_extra.txt
```
This would install gello and space mouse related modules. Also, make sure you have [`xArm-Python-SDK`](https://github.com/xArm-Developer/xArm-Python-SDK) installed.

## 1. GELLO for xArm7: 
By running the command above, `gello_software` package will be installed locally under `./src` folder. To ensure proper configuration of the dummy robot, dynamixel motor offset of each joint on the dummy robot must be confirmed from `gello_get_offset.py` script inside this repository. Please Study the usage of GELLO carefully before continue working with real xArm7. 

**Note**: Gello would also require additional dependencies running its scripts. Consider switching to another `conda env` (like `gello`) with gello offset check.

To get gello offset (should go through this each time gello is powered on):   

Setup and power on the gello dummy robot, hold it with a **known real joint configuration** (use [`0, 0, 0, 90, 0, 90, 0`] degrees as example):

```
$ conda activate gello #(configured according to gello ReadMe installation requirements)
$ python gello_get_offset.py --port /dev/ttyUSB0 --start_joints 0 0 0 1.5708 0 1.5708 0 --joint_signs 1 1 1 1 1 1 1
```

Then the output result (joint offset and gripper offset) can be set to the `teleoperators/gello_xarm7` configuration. 


## 2. Space Mouse:

The space mouse currently is configured as **2D control** (in XY plane) for Push T block task, if you need more freedom, check and edit the interface in `teleoperators/space_mouse/space_mouse.py`.  

## 3. Lerobot Data Recording with above devices:
Please use provided `record_uf_edit.py` script in this directory instead of lerobot_record.py in scripts folder. We have made modifications for space mouse data collection (delta command to absolute command) and enabled using external yaml file as flexible configuration. Check the two `*_record_config.yaml` files here and change the filename used in `record_uf_edit.py`.

## 4. Example commandline instructions:

### 4.1 Dataset Recording:

Recording with gello_xarm7 (modify the config file with your correct OFFSET and PORT name first!):

```shell
python record_uf_edit.py --config xarm7_gello_record_config.yaml

```
Recording with xarm7 and space mouse (and **Resume** recording on existing dataset):
```shell
python record_uf_edit.py --config xarm7_gello_record_config.yaml --resume

```
### 4.2 Training

Use official script for training, here use `diffusion` model and resume training option as example, edit or remove arguments based on your case:
```shell
python -m lerobot.scripts.lerobot_train  --dataset.repo_id=ufactory/xarm7_pushT   --policy.type=diffusion   --output_dir=outputs/train/xarm7_pushT   --job_name=xarm7_pushT   --policy.device=cuda --policy.repo_id=ufactory/xarm7_pushT --steps=800000  --resume=true --config_path=<YOUR_LOCAL_PATH>/train/xarm7_pushT/checkpoints/last/pretrained_model/train_config.json --batch_size=16
```

### 4.3 Evaluation
Use official script for trained policy evaluation, for example:
```shell
python -m lerobot.scripts.lerobot_eval --policy.path=<YOUR_LOCAL_PATH>/outputs/train/xarm7_pushT/checkpoints/last/pretrained_model/
```

### 4.4 Others
For other LeRobot supported features like Dataset Visualization or Editting, please go through LeRobot Documentation for instructions.

## 5. Special Notices:
Users need to **study the whole codebase thoroughly**, and understand about relevant configuration parameters, since the configurations written in the code are not for all use cases and set-ups, it is the users job to study the code or theories to get good knowledge about them and modify/tune on their own. Especially for diffusion policy, default parameters from LeRobot may be targeted for simulation and not optimized for real robot scenarios.