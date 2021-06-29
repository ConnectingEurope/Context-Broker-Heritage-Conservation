# daily maximum and minimum values in temperature and realtive humidity
class DayExtreme:
    def __init__(self, feels_like_temperature, temperature, relative_humidity):
        self.feelsLikeTemperature = {"type": "Property","value": feels_like_temperature}
        self.temperature          = {"type": "Property","value": temperature}
        self.relativeHumidity     = {"type": "Property","value": relative_humidity}
