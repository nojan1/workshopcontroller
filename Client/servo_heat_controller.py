import config
from heat_controller_base import HeatControllerBase
from Adafruit_PCA9685 import PCA9685

# Configure min and max servo pulse lengths
SERVO_MIN = 150  # Min pulse length out of 4096
SERVO_MAX = 600  # Max pulse length out of 4096

class ServoHeatController(HeatControllerBase):
    def __init__(self):
        HeatControllerBase.__init__(self)

        self.pwm = PCA9685(address=config.SERVO_I2C_ADDRESS, busnum=config.SERVO_I2C_BUSNUM)
        self.pwm.set_pwm_freq(60)

    def set_heat(self, downstairs, upstairs):
        tempDownstairs = self.correct_temperature(downstairs)
        tempUpstairs = self.correct_temperature(upstairs)

        self.set_servo_pulse(1, self.pulse_from_temp(tempDownstairs))
        self.set_servo_pulse(2, self.pulse_from_temp(tempUpstairs))

        return tempDownstairs, tempUpstairs
    
    def correct_temperature(self, uncorrected_temp):
        if uncorrected_temp > config.HEAT_MAX:
            return config.HEAT_MAX
        elif uncorrected_temp < config.HEAT_MIN:
            return config.HEAT_MIN
        else:
            return uncorrected_temp

    def pulse_from_temp(self, corrected_temp):
        servo_range = SERVO_MAX - SERVO_MIN
        temp_percentage = (corrected_temp - config.HEAT_MIN) / (config.HEAT_MAX - config.HEAT_MIN)

        return SERVO_MIN + (servo_range * temp_percentage)

    def set_servo_pulse(self, channel, pulse):
        pulse_length = 1000000    # 1,000,000 us per second
        pulse_length //= 60       # 60 Hz
        pulse_length //= 4096     # 12 bits of resolution
        pulse *= 1000
        pulse //= pulse_length

        self.pwm.set_pwm(channel, 0, pulse)
