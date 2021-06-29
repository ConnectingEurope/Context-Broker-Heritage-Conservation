from .Location import Location

class IndoorEnvironmentObserved:
    def __init__(self, id_indoor, city_name, building_name, date_observed, temperature, relative_humidity, atmospheric_pressure, illuminance, infrared, co2, tvoc, latitude, longitude):
        self.id                         = "urn:ngsi-ld:IndoorEnvironmentObserved:{0}:{1}:{2}".format(city_name, building_name.replace(" ","-"), id_indoor)
        self.type                       = "IndoorEnvironmentObserved"
        self.name                       = {"type": "Property","value": building_name}
        self.description                = {"type": "Property","value": "Indoor information of {0} in {1}".format(building_name, city_name)}
        self.location                   = {"type": "GeoProperty", "value": Location("Point", [longitude,latitude]).__dict__}
        self.dateObserved               = {"type": "Property", "value": {"type": "DateTime", "value": date_observed}}
        self.dataProvider               = {"type": "Property","value": id_indoor}
        self.temperature                = {"type": "Property","value": temperature}
        self.relativeHumidity           = {"type": "Property","value": relative_humidity}
        self.illuminance                = {"type": "Property","value": illuminance}
        self.co2                        = {"type": "Property","value": co2}
        self.co2Level                   = {"type": "Property","value": " "}
        self.infrared                   = {"type": "Property","value": infrared}
        self.tvoc                       = {"type": "Property","value": tvoc}
        self.tvocLevel                  = {"type": "Property","value": " "}
        self.atmosphericPressure        = {"type": "Property","value": atmospheric_pressure}
