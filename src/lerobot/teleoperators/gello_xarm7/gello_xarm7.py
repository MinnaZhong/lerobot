#!/usr/bin/env python
import os
import sys
import logging
import time
import numpy as np

from lerobot.teleoperators import Teleoperator
from .config_gello_xarm7 import GelloxArm7Config
from gello.agents.gello_agent import GelloAgent, DynamixelRobotConfig
from lerobot.utils.errors import DeviceAlreadyConnectedError, DeviceNotConnectedError


logger = logging.getLogger(__name__)

class GelloxArm7(Teleoperator):
    """
    GELLO for xArm7 tele-op, ref: https://wuphilipp.github.io/gello_site/
    """

    config_class = GelloxArm7Config
    name = "gello_xarm7"

    def __init__(self, config: GelloxArm7Config):
        super().__init__(config)
        self.config = config
        self._is_connected = False
        self._is_calibrated = True # CHECK!!
        param_dict = {
                "joint_ids": self.config.joint_ids,
                "joint_signs": self.config.joint_signs,
                "joint_offsets": list(x*(np.pi / 2) for x in self.config.joint_offset_ints),
                "gripper_config": self.config.gripper_config
        }
        self._dynamixel_robo_config = DynamixelRobotConfig(**param_dict)
        print(self._dynamixel_robo_config)

    @property
    def action_features(self) -> dict:
        # Add one more dof for gripper
        act_ft = {
            "joint_position": {
            "dtype": "float",
            "shape": (8,)
            }
        }
        return act_ft

    @property
    def feedback_features(self) -> dict:
        fbk_ft = {
            "joint_position": {
            "dtype": "float",
            "shape": (8,)
            }
        }
        return fbk_ft

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    def connect(self, calibrate: bool = True) -> None:
        if self._is_connected:
            raise DeviceAlreadyConnectedError(f"{self} already connected")

        self.gello_agent = GelloAgent(port=self.config.port, dynamixel_config=self._dynamixel_robo_config)
        if not self._is_calibrated and calibrate:
            logger.info(
                "Mismatch between calibration values in the motor and the calibration file or no calibration file found"
            )
            self.calibrate()

        self.configure()
        self._is_connected = True
        logger.info(f"{self} connected.")

    @property
    def is_calibrated(self) -> bool:
        return self._is_calibrated

    def calibrate(self) -> None:
        pass

    def configure(self) -> None:
        # TODO: Go to sync position slowly? Can not 
        pass

    def get_action(self) -> dict[str, np.ndarray]:
        start = time.perf_counter()
        fake_obs = dict({"joint_state": np.array([0.0]*8)}) # for agent.act() argument, actually no use
        action_array = self.gello_agent.act(fake_obs) # current gello joint pos as np.ndarray
        dt_ms = (time.perf_counter() - start) * 1e3
        logger.debug(f"{self} read action: {dt_ms:.1f}ms")

        action = {}
        for i in range(7):
            action.update({f"J{i+1}.pos": action_array[i]})
        action.update({"gripper.pos": action_array[7]})
        return action

    def send_feedback(self, feedback: dict[str, float]) -> None:
        raise NotImplementedError

    def disconnect(self) -> None:
        if not self._is_connected:
            DeviceNotConnectedError(f"{self} is not connected.")

        self._is_connected = False
        logger.info(f"{self} disconnected.")
