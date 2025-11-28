#!/usr/bin/env python

from dataclasses import dataclass
from collections.abc import Sequence
from typing import Tuple
from lerobot.teleoperators import TeleoperatorConfig


@TeleoperatorConfig.register_subclass("gello_xarm7")
@dataclass
class GelloxArm7Config(TeleoperatorConfig):
    # Port to connect to the gello dummy arm
    port: str = "/dev/serial/by-id/usb-FTDI_USB__-__Serial_Converter_FTAJZYC7-if00-port0"

    # Others: Calibration angles, joint directions etc
    joint_ids: Sequence[int] = (1, 2, 3, 4, 5, 6, 7)
    joint_signs: Sequence[int] = (1, 1, 1, 1, 1, 1, 1) # if follow the original open-sourced gello xarm7 setup
    
    # Below: Can be decided by running gello/scripts/gello_get_offset.py
    # joint offsets as multiples of pi/2
    joint_offset_ints: Sequence[int] = (0, 0, 0, 0, 0, 0, 0)
    gripper_config: Tuple[int, int, int] = (8, 143, 71)
