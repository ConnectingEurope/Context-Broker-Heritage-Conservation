import pytz
import datetime
import time

import config.config as cnf
config = cnf.Config()

import core.air_quality_service as aqo
import core.building_service as building
import core.indoor_service as indoor
import core.weather_forecast_service as weather
import utils.delete_data as delete

def generate_air_quality_historical_data():
    datetime_spain = pytz.timezone("Europe/Madrid")
    datetime_now = datetime.datetime.now(datetime_spain)
    datetime_now_no_micro = datetime_now.replace(microsecond=0)
    initial_datetime = datetime_now_no_micro - datetime.timedelta(hours=10*24, minutes=0)
    service_name = config.air_quality_service
    print(service_name)
    
    while initial_datetime < datetime.datetime.now(datetime_spain):
        print(initial_datetime)
        aqo.execute_air_quality_observed_random(service_name, initial_datetime)
        initial_datetime = initial_datetime + datetime.timedelta(hours=0, minutes=60)
   
def generate_building_historical_data():
    datetime_spain = pytz.timezone("Europe/Madrid")
    datetime_now = datetime.datetime.now(datetime_spain)
    datetime_now_no_micro = datetime_now.replace(microsecond=0)
    initial_datetime = datetime_now_no_micro - datetime.timedelta(hours=10*24, minutes=0)
    service_name = config.building_service
    print(service_name)

    while initial_datetime < datetime.datetime.now(datetime_spain):
        print(initial_datetime)
        building.execute_building(service_name, initial_datetime)
        initial_datetime = initial_datetime + datetime.timedelta(hours=0, minutes=30)
        
def generate_indoor_historical_data():
    datetime_spain = pytz.timezone("Europe/Madrid")
    datetime_now = datetime.datetime.now(datetime_spain)
    datetime_now_no_micro = datetime_now.replace(microsecond=0)
    initial_datetime = datetime_now_no_micro - datetime.timedelta(hours=10*24, minutes=0)
    service_name = config.indoor_service
    print(service_name)
    
    while initial_datetime < datetime.datetime.now(datetime_spain):
        print(initial_datetime)
        indoor.execute_indoor(service_name, initial_datetime)
        initial_datetime = initial_datetime + datetime.timedelta(hours=0, minutes=30)
    
def generate_weather_forecast_historical_data():
    datetime_spain = pytz.timezone("Europe/Madrid")
    datetime_now = datetime.datetime.now(datetime_spain)
    datetime_now_no_micro = datetime_now.replace(microsecond=0)
    initial_datetime = datetime_now_no_micro - datetime.timedelta(hours=10*24, minutes=0)
    service_name = config.weather_service
    print(service_name)
    
    while initial_datetime < datetime.datetime.now(datetime_spain):
        print(initial_datetime)
        weather.execute_random_weather_forecast(service_name, initial_datetime)
        initial_datetime = initial_datetime + datetime.timedelta(hours=24)
        
if __name__ == "__main__":	
	generate_air_quality_historical_data()
	generate_building_historical_data()
	generate_indoor_historical_data()
	generate_weather_forecast_historical_data()
