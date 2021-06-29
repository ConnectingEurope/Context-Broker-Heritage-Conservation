import time

import core.weather_forecast_service as weather
import core.air_quality_service as aqo

import utils.generate_information as generate
import config.config as cnf

config = cnf.Config()

AQI_SERVICE_NAME = config.air_quality_service
WEATHER_SERVICE_NAME = config.weather_service

if __name__ == "__main__":
    seconds_to_wait = 1*60*60 #1h
    print("START - EXECUTION EVERY {0} seconds.".format(seconds_to_wait))

    while True:
        string_datetime_now, date_datetime_now = generate.datetime_time_tz()

        print("{0} {1}".format(string_datetime_now, AQI_SERVICE_NAME))
        aqo.execute_air_quality_observed(AQI_SERVICE_NAME)

        print("{0} {1}".format(string_datetime_now, WEATHER_SERVICE_NAME))
        weather.execute_weather_forecast(WEATHER_SERVICE_NAME)
        
        print("SLEEP {0}".format(seconds_to_wait))
        time.sleep(seconds_to_wait)