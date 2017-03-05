"""Dummy implementation for the heat controller"""

from heat_controller_base import HeatControllerBase

class DummyHeatController(HeatControllerBase):
    """Dummy implementation for the heat controller"""

    def set_heat(self, downstairs, upstairs):
        corrected_downstairs = self.correct_temperature(downstairs)
        corrected_upstairs = self.correct_temperature(upstairs)
        
        pulse_downstairs = self.pulse_from_temp(corrected_downstairs)
        pulse_upstairs = self.pulse_from_temp(corrected_upstairs)

        print("Setting downstairs to: {0}, pulse: {1}".format(corrected_downstairs, pulse_downstairs))
        print("Setting upstarts to: {0}, pulse: {1}".format(corrected_upstairs, pulse_upstairs))

        return corrected_downstairs, corrected_upstairs
