import connectors.air_quality_index_request as air_quality_index
import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import utils.generate_information as generate
import config.config as cnf
import algorithms.aqi.air_quality_index as aqi

config = cnf.Config()
NIFI_NOTIFY_URI = config.nifi_notify_uri
API_NOTIFY_URI = config.api_notify_uri
city_name = config.region
country_info = config.country
list_sub_parameters_elastic = config.air_quality_subs
list_sub_parameters_api = []
notify_elastic = True
notify_api = False
sub_description_elastic = 'Notify Elastic of'
sub_description_api = 'Notify API of'

# Functions that create/update the information of Environment in the CB
def execute_air_quality_observed(service_name):
    method_name = 'execute_air_quality_observed'

    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld
    id_aqi = config.sensor_info["003"]["id"]

    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Request data from open data platform
    raw_data = air_quality_index.request_air_quality_index()
    orion_datetime_payload = ''

    try:
        existing_data = orion.check_existing_data_id(CB_URI_LD, headers, "urn:ngsi-ld:AirQualityObserved:{0}:{1}".format(city_name, id_aqi))

        if existing_data.status_code == 200 and len(existing_data.json()) >= 1:
            received_json = existing_data.json()
            orion_datetime_payload = received_json["dateObserved"]["value"]["value"]
    except Exception as ex:
        error_text = "Error consulting orion. Service name: {0} // Exception: {1}".format(service_name, ex)
        print(error_text)

    received_datetime_aemet = raw_data["data"]["time"]["iso"]

    if received_datetime_aemet == orion_datetime_payload:
        print("SAME DATETIME, NO PUBLISH")
    else:
        #Format new parameter values to python class
        air_quality_dict = format_data.create_air_quality_dict_formatted(raw_data, id_aqi, city_name, country_info)

        list_dicts = [air_quality_dict]
        
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
def execute_air_quality_observed_local(service_name):
    method_name = 'execute_air_quality_observed'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    id_aqi = config.sensor_info["003"]["id"]

    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Request data from open data platform
    raw_data = air_quality_index.request_air_quality_index()
    orion_datetime_payload = ''

    try:
        existing_data = orion.check_existing_data_id(CB_URI_LD, headers, "urn:ngsi-ld:AirQualityObserved:{0}:{1}".format(city_name, id_aqi))

        if existing_data.status_code == 200 and len(existing_data.json()) >= 1:
            received_json = existing_data.json()
            orion_datetime_payload = received_json["dateObserved"]["value"]["value"]
    except Exception as ex:
        error_text = "Error consulting orion. Service name: {0} // Exception: {1}".format(service_name, ex)
        print(error_text)

    received_datetime_aemet = raw_data["data"]["time"]["iso"]

    if received_datetime_aemet == orion_datetime_payload:
        print("SAME DATETIME, NO PUBLISH")
    else:
        #Format new parameter values to python class
        air_quality_dict = format_data.create_air_quality_dict_formatted(raw_data, id_aqi, city_name, country_info)

        list_dicts = [air_quality_dict]
        
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

def execute_air_quality_observed_random(service_name, date_observed):
    method_name = 'execute_air_quality_observed_random'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    id_aqi = config.sensor_info["003"]["id"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    
    #Generate random values
    random_co = generate.generate_random_no2(date_observed)
    random_humidity = generate.generate_humidity_random(date_observed)
    random_temperature = generate.generate_temperature_random(date_observed)
    random_wind_speed = generate.generate_wind_speed_random(date_observed)
    random_no2 = generate.generate_random_no2(date_observed)
    random_pm10 = generate.generate_random_pm10(date_observed)
    random_so2 = generate.generate_random_so2(date_observed)
    random_o3 = generate.generate_random_o3(date_observed)
    aqi_agent = aqi.calculate_AQI(["no2","pm10","so2","o3"],[random_no2, random_pm10, random_so2, random_o3])

    raw_data = {'data': {'city': {'geo': [37.3977124, -6.000886]}, 'dominentpol': aqi_agent.agent, 'iaqi': {'co': {'v': random_co}, 'h': {'v': random_humidity}, 'no2': {'v': random_no2}, 'o3': {'v': random_o3}, 'pm10': {'v': random_pm10}, 'so2': {'v': random_so2}, 't': {'v': random_temperature}, 'w': {'v': random_wind_speed}}, 'time': {'iso': string_date_observed}}}

    #Format new parameter values to python class
    air_quality_dict = format_data.create_air_quality_dict_formatted(raw_data, id_aqi, city_name, country_info )

    list_dicts = [air_quality_dict]
    
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
