from sensorservice.sensor import Sensor
from sensorservice.noiseservice.noise208_adapter import NoiseSensor
from sensorservice.illuminanceservice.illumdummy_adapter import IllumDummySensor
from sensorservice.co2service.c9co2_adapter import C9CO2Sensor
class ConcentrationService(Sensor):
    def __init__(self):
        self.noise = NoiseSensor()
        self.illum = IllumDummySensor()
        self.co2 = C9CO2Sensor()

    def get_data(self):
        noise_data = self.noise.get_data()
        illum_data = self.illum.get_data()
        co2_data = self.co2.get_data()
        response = {"nosie": noise_data, "illuminance": illum_data, "co2": co2_data}
        return response

    def get_place(self):
        return "None"

    def get_unit(self):
        return "None"

    def get_service_type(self):
        return "Air Quality" 