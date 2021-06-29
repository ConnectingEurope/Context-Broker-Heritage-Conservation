from .DayExtreme import DayExtreme
from .Address    import Address
from .Location   import Location

#Equivalent class for WeatherForecast datal model
class WeatherForecast:
    def __init__(self, id_weather, city_name, country_info, latitude, longitude, day_minimum: DayExtreme, day_maximum: DayExtreme, 
                feels_like_temperature, temperature, weather_type, source,
                precipitation_prob, wind_speed, date_issued,  relative_humidity, uv_index_max):
        self.id                         = "urn:ngsi-ld:WeatherForecast:{0}:{1}".format(city_name, id_weather)
        self.type                       = "WeatherForecast"
        self.name                       = {"type": "Property","value": city_name}
        self.description                = {"type": "Property","value": "Weather forecast of {0}".format(city_name)}
        self.dataProvider               = {"type": "Property","value": id_weather}
        self.source                     = {"type": "Property","value": source}
        self.address                    = {"type": "Property","value": Address(country_info, city_name).__dict__}
        self.location                   = {"type": "GeoProperty", "value": Location("Point", [longitude,latitude]).__dict__}
        self.dateIssued                 = {"type": "Property", "value": {"type": "DateTime", "value": date_issued}}
        self.dayMinimum                 = {"type": "Property","value": day_minimum.__dict__}
        self.dayMaximum                 = {"type": "Property","value": day_maximum.__dict__}
        self.feelsLikeTemperature       = {"type": "Property","value": feels_like_temperature}
        self.temperature                = {"type": "Property","value": temperature}
        self.relativeHumidity           = {"type": "Property","value": relative_humidity}
        self.weatherType                = {"type": "Property","value": weather_type}
        self.precipitationProbablity    = {"type": "Property","value": precipitation_prob}
        self.windSpeed                  = {"type": "Property","value": wind_speed}
        self.uvIndexMax                 = {"type": "Property","value": uv_index_max}
