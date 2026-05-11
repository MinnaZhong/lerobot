# Copyright 2024 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import cast
from lerobot.utils.import_utils import make_device_from_device_class
from lerobot.robots.config import RobotConfig
from lerobot.robots.robot import Robot


def make_uf_robot_from_config(config: RobotConfig) -> Robot:
    if config.type == "uf::robot":
        from .uf_robot import UFRobot

        return UFRobot(config)
    else:
        try:
            return cast(Robot, make_device_from_device_class(config))
        except Exception as e:
            raise ValueError(f"Error creating robot with config {config}: {e}") from e

