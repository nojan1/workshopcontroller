import config
from heat_controller_base import HeatControllerBase
from Adafruit_PCA9685 import PCA9685

class ServoHeatController(HeatControllerBase):
    def __init__(self):
        HeatControllerBase.__init__(self)

        self.pwm = PCA9685(address=config.SERVO_I2C_ADDRESS, busnum=config.SERVO_I2C_BUSNUM)
        self.pwm.set_pwm_freq(60)

    def set_heat(self, downstairs, upstairs):
        corrected_downstairs = self.correct_temperature(downstairs)
        corrected_upstairs = self.correct_temperature(upstairs)
        
        pulse_downstairs = self.pulse_from_temp(corrected_downstairs)
        pulse_upstairs = self.pulse_from_temp(corrected_upstairs)

        print("Setting downstairs to: {0}, pulse: {1}".format(corrected_downstairs, pulse_downstairs))
        print("Setting upstarts to: {0}, pulse: {1}".format(corrected_upstairs, pulse_upstairs))

        self.set_servo_pulse(0, pulse_downstairs)
        self.set_servo_pulse(1, pulse_upstairs)

        return corrected_downstairs, corrected_upstairs
    
    def set_servo_pulse(self, channel, pulse):
        pulse_length = 1000000    # 1,000,000 us per second
        pulse_length //= 60       # 60 Hz
        pulse_length //= 4096     # 12 bits of resolution
        pulse *= 1000
        pulse //= pulse_length

        self.pwm.set_pwm(channel, 0, int(pulse))
