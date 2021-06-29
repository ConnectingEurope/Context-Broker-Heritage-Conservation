from .Location import Location 
from .Address import Address

class AirQualityObserved:
    def __init__(self, id_aqi, city_name, country_info, date_observed, latitude, longitude, temperature, relative_humidity, wind_speed, air_quality_index, air_quality_level, co, so2, no2, o3, pm10):
        self.id                 = "urn:ngsi-ld:AirQualityObserved:{0}:{1}".format(city_name, id_aqi)
        self.type               = "AirQualityObserved"
        self.name               = {"type": "Property","value": city_name}
        self.description        = {"type": "Property","value": "Air quality in {0} - {1}".format(id_aqi, city_name)}
        self.address            = {"type": "Property","value": Address(country_info, city_name).__dict__}
        self.dateObserved       = {"type": "Property", "value": {"type": "DateTime", "value": date_observed}}
        self.location           = {"type": "GeoProperty","value": Location("Point",[longitude,latitude]).__dict__}
        self.source             = {"type": "Property", "value": "https://aqicn.org/"}
        self.dataProvider       = {"type": "Property","value": id_aqi}
        self.typeOfLocation     = {"type": "Property", "value": "outdoor"}
        self.temperature        = {"type": "Property", "value": temperature}
        self.relativeHumidity   = {"type": "Property", "value": relative_humidity}
        self.windSpeed          = {"type": "Property", "value": wind_speed}
        self.airQualityIndex    = {"type": "Property", "value": air_quality_index}
        self.airQualityLevel    = {"type": "Property", "value": air_quality_level}
        self.co                 = {"type": "Property", "value": co}
        self.so2                = {"type": "Property", "value": so2}
        self.no2                = {"type": "Property", "value": no2}
        self.o3                 = {"type": "Property", "value": o3}
        self.pm10               = {"type": "Property", "value": pm10}
