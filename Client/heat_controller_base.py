import config

class HeatControllerBase(object):
    """ Base class for the heat controllers """

    def set_heat(self, downstairs, upstairs):
        pass

    def correct_temperature(self, uncorrected_temp):
        if uncorrected_temp > config.HEAT_MAX:
            return config.HEAT_MAX
        elif uncorrected_temp < config.HEAT_MIN:
            return config.HEAT_MIN
        else:
            return uncorrected_temp
            
    def pulse_from_temp(self, corrected_temp):
        servo_range = config.SERVO_MAX - config.SERVO_MIN
        temp_percentage = (float(corrected_temp) - float(config.HEAT_MIN)) / (float(config.HEAT_MAX) - float(config.HEAT_MIN))

        return int(config.SERVO_MIN + (float(servo_range) * temp_percentage))