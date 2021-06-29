from .Address import Address
from .Location import Location

class Building:
    def __init__(self, id_building, city_name, country_info, building_name, building_category, building_occupancy, max_capacity, building_polygon, list_opening_hours, date_observed):
        self.id             = "urn:ngsi-ld:Building:{0}:{1}:{2}".format(city_name.replace(" ","-"), building_name.replace(" ","-"), id_building)
        self.type           = "Building"
        self.name           = {"type": "Property","value": building_name}
        self.description    = {"type": "Property","value": "Building information of {0} in {1}".format(building_name, city_name)}
        self.category       = {"type": "Property","value": [building_category]}
        self.dateObserved   = {"type": "Property", "value": {"type": "DateTime", "value": date_observed}}
        self.dataProvider   = {"type": "Property","value": id_building}
        self.peopleCapacity = {"type": "Property","value": max_capacity}
        self.peopleOccupancy= {"type": "Property","value": building_occupancy}
        self.address        = {"type": "Property","value": Address(country_info, city_name).__dict__}
        self.location       = {"type": "GeoProperty","value": Location("Polygon",[building_polygon]).__dict__}
        self.openingHours   = {"type": "Property","value": list_opening_hours}
