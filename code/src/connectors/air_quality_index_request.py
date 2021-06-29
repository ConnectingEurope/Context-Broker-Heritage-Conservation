import connectors.open_data_connector as connector
import config.config as cnf

config = cnf.Config()

API_KEY=config.waqi_api_key
BASE_URI=config.waqi_base_uri
SEVILLA=config.sevilla_station
SOURCE=config.waqi_source

# AQI Sevilla method
def request_air_quality_index():
    uri = BASE_URI + SEVILLA + '?token=' + API_KEY
    data = connector.request_data(uri,SOURCE)
    return data
