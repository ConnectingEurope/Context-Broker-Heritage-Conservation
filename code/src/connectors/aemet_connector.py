import connectors.open_data_connector as connector
import config.config as cnf

config = cnf.Config()

API_KEY=config.aemet_api_key
BASE_URI=config.aemet_weather_forecast_uri
CITY_ID=config.aemet_sevilla_id
SOURCE=config.aemet_source

# Request daily forecast
def request_daily_forecast():
    uri = BASE_URI + '/diaria/' + CITY_ID + '/?api_key=' + API_KEY
    data = connector.request_data(uri,SOURCE)
    return(data)

#Request hourly forecast
def request_hourly_forecast():
    uri = BASE_URI + '/horaria/' + CITY_ID + '/?api_key=' + API_KEY
    data = connector.request_data(uri,SOURCE)
    return(data)
