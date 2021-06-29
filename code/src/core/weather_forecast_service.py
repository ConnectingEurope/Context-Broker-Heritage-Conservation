import connectors.aemet_connector as aemet
import connectors.orion_connector_ld as orion
import connectors.format_data as format_data
import utils.generate_information as generate
import config.config as cnf
from core.DayExtreme import DayExtreme

config = cnf.Config()
NIFI_NOTIFY_URI = config.nifi_notify_uri
API_NOTIFY_URI = config.api_notify_uri
city_name = config.region
country_info = config.country
list_sub_parameters_elastic = config.weather_forecast_subs
list_sub_parameters_api = []
notify_elastic = True
notify_api = False
sub_description_elastic = 'Notify Elastic of'
sub_description_api = 'Notify API of'

# Functions that create/update the information of Environment in the CB
def execute_weather_forecast(service_name):
    method_name = 'execute_weather_forecast'

    CB_URI_LD = config.context_broker_uri_ld
    SUB_URI_LD = config.subscription_uri_ld
    id_weather = config.sensor_info["002"]["id"]
    weather_latitude = config.sensor_info["002"]["latitude"]
    weather_longitude = config.sensor_info["002"]["longitude"]

    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    #Request weather forecast AEMET
    aemet_raw_data = aemet.request_daily_forecast()
    orion_datetime_payload = ''

    try:
        existing_data = orion.check_existing_data_id(CB_URI_LD, headers, "urn:ngsi-ld:WeatherForecast:{0}:{1}".format(city_name, id_weather))

        if existing_data.status_code == 200 and len(existing_data.json()) >= 1:
            received_json = existing_data.json()
            orion_datetime_payload = received_json["dateIssued"]["value"]["value"]
    except Exception as ex:
        error_text = "Error consulting orion. Service name: {0} // Exception: {1}".format(service_name, ex)
        print(error_text)

    received_datetime_aemet = generate.convert_datetime_aemet(aemet_raw_data[0]["elaborado"])

    if received_datetime_aemet == orion_datetime_payload:
        print("SAME DATETIME, NO PUBLISH")
    else:
        #Create building dict
        weather_forecast_dict = format_data.create_weather_forecast_dict_formatted(id_weather, city_name, country_info, weather_latitude, weather_longitude, aemet_raw_data[0])
        
        list_dicts = [weather_forecast_dict]

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
def execute_weather_forecast_local(service_name):
    method_name = 'execute_weather_forecast'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    id_weather = config.sensor_info["002"]["id"]
    weather_latitude = config.sensor_info["002"]["latitude"]
    weather_longitude = config.sensor_info["002"]["longitude"]

    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    #Request weather forecast AEMET
    aemet_raw_data = aemet.request_daily_forecast()
    orion_datetime_payload = ''

    try:
        existing_data = orion.check_existing_data_id(CB_URI_LD, headers, "urn:ngsi-ld:WeatherForecast:{0}:{1}".format(city_name, id_weather))

        if existing_data.status_code == 200 and len(existing_data.json()) >= 1:
            received_json = existing_data.json()
            orion_datetime_payload = received_json["dateIssued"]["value"]["value"]
    except Exception as ex:
        error_text = "Error consulting orion. Service name: {0} // Exception: {1}".format(service_name, ex)
        print(error_text)

    received_datetime_aemet = generate.convert_datetime_aemet(aemet_raw_data[0]["elaborado"])

    if received_datetime_aemet == orion_datetime_payload:
        print("SAME DATETIME, NO PUBLISH")
    else:
        #Create building dict
        weather_forecast_dict = format_data.create_weather_forecast_dict_formatted(id_weather, city_name, country_info, weather_latitude, weather_longitude, aemet_raw_data[0])
        
        list_dicts = [weather_forecast_dict]

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

# Functions that create/update random information of Environment in the CB
def execute_random_weather_forecast(service_name, date_observed):
    method_name = 'execute_random_weather_forecast'

    CB_URI_LD = config.context_broker_uri_ld_local
    SUB_URI_LD = config.subscription_uri_ld_local
    id_weather = config.sensor_info["002"]["id"]
    weather_latitude = config.sensor_info["002"]["latitude"]
    weather_longitude = config.sensor_info["002"]["longitude"]

    string_date_observed = date_observed.isoformat()
    headers = {
        'fiware-service': service_name,
        'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    #Generate random weather forecast
    temperature = generate.generate_temperature_random(date_observed)
    feels_like_temperature = temperature+1
    relative_humidity = generate.generate_humidity_random(date_observed)
	
    day_min = DayExtreme(temperature-2, temperature-3, relative_humidity)
    day_max = DayExtreme(temperature+3, temperature+2, relative_humidity)
    weather_type = generate.generate_weather_type_random()
    source = "https://www.aemet.es"
    precipitation_prob = generate.generate_random_prob_precipitation()
    wind_speed = generate.generate_wind_speed_random(date_observed)
    date_issued = string_date_observed
    uv_max = generate.generate_random_uvmax()
    
    #Create building dict
    weather_forecast_dict = format_data.create_random_weather_forecast_dict_formatted(id_weather, city_name, country_info, weather_latitude, weather_longitude, day_min, day_max, feels_like_temperature, temperature, weather_type, source, precipitation_prob, wind_speed, string_date_observed, relative_humidity, uv_max)
    
    list_dicts = [weather_forecast_dict]
    
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
