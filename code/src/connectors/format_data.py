from core.AirQualityObserved import AirQualityObserved 
from core.Building import Building 
from core.IndoorEnvironmentObserved import IndoorEnvironmentObserved
from core.WeatherForecast import WeatherForecast
from core.DayExtreme import DayExtreme

import utils.generate_information as generate
import algorithms.aqi.air_quality_index as aqi
import json

#function to format an object to a dict 
def format_data(generic_object):
    object_to_dict = generic_object.__dict__
    return object_to_dict
    
def create_air_quality_dict_formatted(dict_data, id_aqi, city_name, country_info):
    air_quality_object = AirQualityObserved(id_aqi,
                                            city_name,
                                            country_info,
                                            dict_data["data"]["time"]["iso"],
                                            dict_data["data"]["city"]["geo"][0],
                                            dict_data["data"]["city"]["geo"][1],
                                            dict_data["data"]["iaqi"]["t"]["v"],
                                            dict_data["data"]["iaqi"]["h"]["v"], 
                                            dict_data["data"]["iaqi"]["w"]["v"], 
                                            aqi.calculate_AQI([dict_data["data"]["dominentpol"]],[dict_data["data"]["iaqi"][dict_data["data"]["dominentpol"]]["v"]]).rangeValue,
                                            aqi.calculate_AQI([dict_data["data"]["dominentpol"]],[dict_data["data"]["iaqi"][dict_data["data"]["dominentpol"]]["v"]]).rangeLevel,
                                            dict_data["data"]["iaqi"]["co"]["v"],
                                            dict_data["data"]["iaqi"]["so2"]["v"],
                                            dict_data["data"]["iaqi"]["no2"]["v"],
                                            dict_data["data"]["iaqi"]["o3"]["v"],
                                            dict_data["data"]["iaqi"]["pm10"]["v"])
    
    air_quality_dict = format_data(air_quality_object)
    return air_quality_dict
    
def create_building_dict_formatted(id_building, city_name, country_info, building_name, building_category, building_occupancy, max_capacity, building_polygon, list_opening_hours, string_date_observed):
    building_object = Building(id_building, city_name, country_info, building_name, building_category, building_occupancy, max_capacity, building_polygon, list_opening_hours, string_date_observed)
    building_dict = format_data(building_object)
    return building_dict

def create_indoor_environment_dict_formatted(id_indoor, city_name, building_name, date_observed, temperature, relative_humidity, atmospheric_pressure, illuminance, infrared, co2, tvoc, latitude, longitude):
    indoor_object = IndoorEnvironmentObserved(id_indoor, city_name, building_name, date_observed, temperature, relative_humidity, atmospheric_pressure, illuminance, infrared, co2, tvoc, latitude, longitude)
    indoor_dict = format_data(indoor_object)
    return indoor_dict

def create_weather_forecast_dict_formatted(id_weather, city_name, country_info, country_latitude, country_longitude, aemet_raw_data):
	day_min = DayExtreme(aemet_raw_data["prediccion"]["dia"][0]["sensTermica"]["minima"], aemet_raw_data["prediccion"]["dia"][0]["temperatura"]["minima"], aemet_raw_data["prediccion"]["dia"][0]["humedadRelativa"]["minima"])
	day_max = DayExtreme(aemet_raw_data["prediccion"]["dia"][0]["sensTermica"]["maxima"], aemet_raw_data["prediccion"]["dia"][0]["temperatura"]["maxima"], aemet_raw_data["prediccion"]["dia"][0]["humedadRelativa"]["maxima"])
	feels_like_temperature = aemet_raw_data["prediccion"]["dia"][0]["sensTermica"]["dato"][1]["value"]
	temperature = aemet_raw_data["prediccion"]["dia"][0]["temperatura"]["dato"][1]["value"]
	period_stake_of_the_sky, state_of_the_sky = generate.find_aemet_prediction_data(aemet_raw_data["prediccion"]["dia"][0]["estadoCielo"], "periodo", "value", "value")
	weather_type = generate.convert_AEMET_skystate(state_of_the_sky)
	source = aemet_raw_data["origen"]["web"]
	period_prob_precipitation_value, prob_precipitation_value = generate.find_aemet_prediction_data(aemet_raw_data["prediccion"]["dia"][0]["probPrecipitacion"], "periodo", "value", "value")
	precipitation_prob = prob_precipitation_value
	periodwind_speed, wind_speed_value = generate.find_aemet_prediction_data(aemet_raw_data["prediccion"]["dia"][0]["viento"], "periodo", "velocidad", "velocidad")
	wind_speed = wind_speed_value
	date_issued = generate.convert_datetime_aemet(aemet_raw_data["elaborado"])
	relative_humidity = aemet_raw_data["prediccion"]["dia"][0]["humedadRelativa"]["dato"][1]["value"]

	day_prediction = aemet_raw_data["prediccion"]["dia"][0]
	
	if {"uvMax"} <= set(day_prediction):
		uv_max = day_prediction["uvMax"]
	else:
		uv_max = -1

	weather_forecast_object = WeatherForecast(
		id_weather, 
		city_name, 
		country_info,
		country_latitude, 
		country_longitude,
		day_min,
		day_max,
		feels_like_temperature,
		temperature,
		weather_type,
		source,
        precipitation_prob,
        wind_speed, 
        date_issued,
        relative_humidity,
        uv_max)
		
	weather_forecast_dict = format_data(weather_forecast_object)
	return weather_forecast_dict
	
def create_random_weather_forecast_dict_formatted(id_weather, city_name, country_info, country_latitude, country_longitude, day_min, day_max, feels_like_temperature, temperature, weather_type, source, precipitation_prob, wind_speed, date_issued, relative_humidity, uv_max):
	
	weather_forecast_object = WeatherForecast(
		id_weather, 
		city_name, 
		country_info,
		country_latitude, 
		country_longitude,
		day_min,
		day_max,
		feels_like_temperature,
		temperature,
		weather_type,
		source,
        precipitation_prob,
        wind_speed, 
        date_issued,
        relative_humidity,
        uv_max)
		
	weather_forecast_dict = format_data(weather_forecast_object)
	return weather_forecast_dict
