import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()
NIFI_NOTIFY_URI = config.nifi_notify_uri
API_NOTIFY_URI = config.api_notify_uri
city_name = config.region
country_info = config.country
list_sub_parameters_elastic = config.building_subs
list_sub_parameters_api = []
notify_elastic = True
notify_api = False
sub_description_elastic = 'Notify Elastic of'
sub_description_api = 'Notify API of'
building_category = 'church'
building_capacity = 500
opening_hours = ["Mon-Fri 10:00-19:00", "Sa 10:00-22:00", "Su 10:00-21:00"]

# Functions that create/update the information of Environment in the CB
def execute_building_sensor(service_name, date_observed, people_count):
    method_name = 'execute_building_sensor'

    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld
    id_building = config.sensor_info["001"]["id"]
    building_name = config.sensor_info["001"]["building_name"]
    building_location = config.sensor_info["001"]["location"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    #Generate random people occupancy
    building_occupancy = people_count
    
    #Create building dict
    building_dict = format_data.create_building_dict_formatted(id_building, city_name, country_info, building_name, building_category, building_occupancy, building_capacity, building_location, opening_hours, string_date_observed)
    
    list_dicts = [building_dict]
    
    #Publish payloads
    #Create the necessary subscriptions
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = ''
    
    try:
        orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(method_name, ex)
        print(error_text)

# Functions that create/update the information of Environment in the CB
def execute_building_random(service_name, date_observed):
    method_name = 'execute_building_random'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    id_building = config.sensor_info["001"]["id"]
    building_name = config.sensor_info["001"]["building_name"]
    building_location = config.sensor_info["001"]["location"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    #Generate random people occupancy
    building_occupancy = generate.generate_building_occupancy_random(date_observed)
    
    #Create building dict
    building_dict = format_data.create_building_dict_formatted(id_building, city_name, country_info, building_name, building_category, building_occupancy, building_capacity, building_location, opening_hours, string_date_observed)
    
    list_dicts = [building_dict]
    
    #Publish payloads
    #Create the necessary subscriptions
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_no_condition(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = ''
    
    try:
        orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(method_name, ex)
        print(error_text)
