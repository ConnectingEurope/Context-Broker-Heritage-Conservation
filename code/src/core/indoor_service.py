import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()
NIFI_NOTIFY_URI = config.nifi_notify_uri
API_NOTIFY_URI = config.api_notify_uri
city_name = config.region
country_info = config.country
list_sub_parameters_elastic = config.indoor_subs_elastic
list_sub_parameters_api = config.indoor_subs_api
notify_elastic = True
notify_api = True
sub_description_elastic = 'Notify Elastic of'
sub_description_api = 'Notify API of'

# Functions that create/update the information of Environment in the CB
def execute_indoor_random(service_name, date_observed):
    method_name = 'execute_indoor_random'
	    
    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    id_indoor_1 = config.sensor_info["005"]["id"]
    id_indoor_2 = config.sensor_info["006"]["id"]
    building_name_1 = config.sensor_info["005"]["building_name"]
    building_name_2 = config.sensor_info["006"]["building_name"]
    indoor_latitude_1 = config.sensor_info["005"]["latitude"]
    indoor_longitude_1 = config.sensor_info["005"]["longitude"]
    indoor_latitude_2 = config.sensor_info["006"]["latitude"]
    indoor_longitude_2 = config.sensor_info["006"]["longitude"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Generate random people occupancy
    temperature = generate.generate_temperature_random(date_observed)
    humidity = generate.generate_humidity_random(date_observed)
    co2 = generate.generate_random_co2_ppm(date_observed)
    illuminance = generate.generate_random_illuminance(date_observed)
    infrared = generate.generate_random_illuminance(date_observed)
    tvoc = generate.generate_random_tvoc(date_observed)
    atmospheric_pressure = generate.generate_random_ap(date_observed)
    
    #Create building dict
    indoor_dict_1 = format_data.create_indoor_environment_dict_formatted(id_indoor_1, city_name, building_name_1, string_date_observed, temperature, humidity, atmospheric_pressure, illuminance, infrared, co2, tvoc, indoor_latitude_1, indoor_longitude_1)
    indoor_dict_2 = format_data.create_indoor_environment_dict_formatted(id_indoor_2, city_name, building_name_2, string_date_observed, temperature, humidity, atmospheric_pressure, illuminance, infrared, co2, tvoc, indoor_latitude_2, indoor_longitude_2)
    
    list_dicts = [indoor_dict_1, indoor_dict_2]
    
    #Publish payloads
    #Create the necessary subscriptions
    api_co2_uri = API_NOTIFY_URI + "index/multisensor"
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_indoor_condition_nifi(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = orion.create_json_subscription_indoor_condition_api(sub_description_api, subscription_type, list_sub_parameters_api, api_co2_uri)
    
    try:
        orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(method_name, ex)
        print(error_text)

# Functions that create/update the information of Environment in the CB
def execute_indoor_sensor(service_name, device_id, date_observed, dict_payload):
    method_name = 'execute_indoor_sensor'
	
    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld
    id_indoor = config.sensor_info[device_id]["id"]
    building_name = config.sensor_info[device_id]["building_name"]
    indoor_latitude=config.sensor_info[device_id]["latitude"]
    indoor_longitude=config.sensor_info[device_id]["longitude"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Generate random people occupancy
    temperature = dict_payload["temperature"]
    humidity = dict_payload["relativeHumidity"]
    co2 = dict_payload["co2"]
    illuminance = dict_payload["illuminance"]
    infrared = dict_payload["infrared"]
    tvoc = dict_payload["tvoc"]
    atmospheric_pressure = dict_payload["atmosphericPressure"]
                
    #Create building dict
    indoor_dict = format_data.create_indoor_environment_dict_formatted(id_indoor, city_name, building_name, string_date_observed, temperature, humidity, atmospheric_pressure, illuminance, infrared, co2, tvoc, indoor_latitude, indoor_longitude)
    list_dicts = [indoor_dict]
    
    #Publish payloads
    #Create the necessary subscriptions
    api_co2_uri = API_NOTIFY_URI + "index/multisensor"
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_indoor_condition_nifi(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = orion.create_json_subscription_indoor_condition_api(sub_description_api, subscription_type, list_sub_parameters_api, api_co2_uri)
    
    try:
        orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(method_name, ex)
        print(error_text)
        
# Functions that create/update the information of Environment in the CB
def execute_indoor_sensor_local(service_name, device_id, date_observed, dict_payload):
    method_name = 'execute_indoor_sensor_local'
	
    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    id_indoor = config.sensor_info[device_id]["id"]
    building_name = config.sensor_info[device_id]["building_name"]
    indoor_latitude=config.sensor_info[device_id]["latitude"]
    indoor_longitude=config.sensor_info[device_id]["longitude"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Generate random people occupancy
    temperature = dict_payload["temperature"]
    humidity = dict_payload["relativeHumidity"]
    co2 = dict_payload["co2"]
    illuminance = dict_payload["illuminance"]
    infrared = dict_payload["infrared"]
    tvoc = dict_payload["tvoc"]
    atmospheric_pressure = dict_payload["atmosphericPressure"]
                
    #Create building dict
    indoor_dict = format_data.create_indoor_environment_dict_formatted(id_indoor, city_name, building_name, string_date_observed, temperature, humidity, atmospheric_pressure, illuminance, infrared, co2, tvoc, indoor_latitude, indoor_longitude)
    
    list_dicts = [indoor_dict]
    
    #Publish payloads
    #Create the necessary subscriptions
    api_co2_uri = API_NOTIFY_URI + "index/multisensor"
    subscription_type = list_dicts[0]["type"]
    subscription_json_elastic = orion.create_json_subscription_indoor_condition_nifi(sub_description_elastic, subscription_type, list_sub_parameters_elastic, NIFI_NOTIFY_URI)
    subscription_json_api = orion.create_json_subscription_indoor_condition_api(sub_description_api, subscription_type, list_sub_parameters_api, api_co2_uri)
    
    try:
        orion.orion_publish_update_data(CB_URI_LD, SUB_URI_LD, headers, list_dicts, notify_elastic, subscription_json_elastic, notify_api, subscription_json_api)
    except Exception as ex:
        error_text = "Exception in {0}: {1}".format(method_name, ex)
        print(error_text)
