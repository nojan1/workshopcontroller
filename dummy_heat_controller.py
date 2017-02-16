"""Dummy implementation for the heat controller"""

from heat_controller_base import HeatControllerBase

class DummyHeatController(HeatControllerBase):
    """Dummy implementation for the heat controller"""

    def set_heat(self, downstairs, upstairs):
        print("Setting downstairs to: " + downstairs)
        print("Setting upstarts to: " + upstairs)
