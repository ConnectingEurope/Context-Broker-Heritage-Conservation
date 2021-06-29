#config generic parameters 
class Config:
	def __init__(self):
		#CONTAINER NAMES
		self.context_broker_uri='http://fiware-orion-ld-container:1026/v2/entities/'
		self.context_broker_uri_ld='http://fiware-orion-ld-container:1026/ngsi-ld/v1/entities/'
		self.context_broker_types='http://fiware-orion-ld-container:1026/ngsi-ld/v1/types/'
		self.context_broker_uri_ld_local='http://localhost:1026/ngsi-ld/v1/entities/'
		self.subscription_uri='http://localhost:1026/v2/subscriptions/'
		self.subscription_uri_ld='http://fiware-orion-ld-container:1026/ngsi-ld/v1/subscriptions/'
		self.subscription_uri_ld_local='http://localhost:1026/ngsi-ld/v1/subscriptions/'
		self.api_notify_uri="http://flask-server-container:5000/"
		self.cygnus_notify_uri_elastic='http://fiware-cygnus:5058/notify'
		self.cygnus_notify_uri_mongo='http://fiware-cygnus:5051/notify'
		self.nifi_notify_uri='http://nifi-container:8889/elastic'
		#MYSQL
		self.mysql_host="db-mysql-container"
		self.mysql_host_local="localhost"
		self.mysql_user="ubuntu"
		self.mysql_pw="cat123"
		self.mysql_db="minerva"
		self.id_people_count=1
		self.table_people_count='count_people_table'
		self.column_name_datetime='date_timestamp'
		self.column_name_people='people_count'
		#GENERAL INFO
		self.region = 'Sevilla'
		self.country = 'ES'
		#API
		self.fields_index_received={
			"co2": ["co2"],
			"tvoc": ["tvoc"],
			"multisensor": ["co2","tvoc"]
		}
		self.fields_index_update={
			"co2": {"co2": "co2Level"},
			"tvoc": {"tvoc": "tvocLevel"},
			"multisensor": {
				"co2": "co2Level",
				"tvoc": "tvocLevel"}
		}
		self.weather_service        = "weatherforecast"
		self.air_quality_service    = "airquality"
		self.building_service       = "building"
		self.indoor_service         = "indoor"
		self.alerts_service         = "alerts"
		self.air_quality_subs       = ["dataProvider","name","description","source","location","address","typeOfLocation","temperature","relativeHumidity","windSpeed","airQualityIndex","airQualityLevel","co","so2","no2","o3","pm10","dateObserved"]
		self.building_subs          = ["dataProvider","name","description","location","dateObserved","address","category","openingHours","peopleCapacity","openingHours","peopleOccupancy"]
		self.indoor_subs_elastic    = ["dataProvider","name","description","location","dateObserved","temperature","relativeHumidity","illuminance","co2","co2Level","tvoc","tvocLevel","atmosphericPressure","infrared"]
		self.indoor_subs_api        = ["co2","co2Level","tvoc","tvocLevel"]
		self.weather_forecast_subs  = ["dataProvider","name","description","dayMinimum", "dayMaximum","feelsLikeTemperature","temperature", "weatherType", "precipitationProbablity", "source", "address", "windSpeed", "dateIssued", "relativeHumidity", "uvIndexMax"]
		self.entity_types = {
							'weatherforecast':'WeatherForecast',
							'airquality':'AirQualityObserved', 
							'building':'Building', 
							'indoor':'IndoorEnvironmentObserved',
							'alerts': 'Alert'
							}
		self.church_polygon=[[-5.98804771900177,37.3982830871188],[-5.988093316555022,37.398498301131994],[-5.988205969333649,37.39889250341477],[-5.9887343645095825,37.39886480278157],[-5.9889355301856995,37.39876252343175],[-5.988844335079193,37.39838962878674],[-5.98878800868988,37.39811688181438],[-5.988326668739319,37.39817867613726],[-5.988340079784392,37.39823620873691],[-5.98804771900177,37.3982830871188]]
		#OPEN DATA
		self.waqi_api_key ='API_key' # Obtain the API key from waqi and enter the key here
		self.aemet_api_key = 'API_key' # Obtain the API key from AEMET and enter the key here
		self.aemet_source ='AEMET'
		self.waqi_source='WAQI'
		self.aemet_weather_forecast_uri='https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio'
		self.waqi_base_uri='https://api.waqi.info/feed/'
		self.aemet_sevilla_id='41091'
		self.sevilla_station='spain/andalucia/sevilla/torneo/'
		#RULE ENGINE
		self.mysql_alert_table='rules'
		self.mysql_alert_attribute_column = 'attribute_name'
		self.mysql_alert_columns = 'id, service_name, entity_type, attribute_name, operator, threshold, value_category, value_subcategory, value_severity, subscription_id, recurrence_seconds'
		#MQTT CONNECTORS
		self.sensor_type = {
			"005":"AM107",
			"006":"AM107",
			"-":"EM500-CO2",
			"--":"EM500-SMTC"
		}
		self.sensor_info = {
			"001": {"id":"B001", "serviceName":self.building_service, "building_name":"Nave central - Iglesia San Luis de los Franceses", "location": self.church_polygon},
			"002": {"id":"WF001", "serviceName":self.weather_service, "name": self.region, "description":"This pointer indicates the values from the open data portal measured in {0}.".format(self.region), "latitude":37.3977124, "longitude":-6.000886},
			"003": {"id":"AQO001", "serviceName":self.air_quality_service, "name": self.region, "description":"This pointer indicates the values from the open data portal measured in {0}.".format(self.region)},
			"005": {"id":"IE005", "serviceName":self.indoor_service, "building_name":"Capilla - Iglesia San Luis de los Franceses", "latitude":37.398661415965854, "longitude":-5.988659155893938},
			"006": {"id":"IE006", "serviceName":self.indoor_service, "building_name":"Nave central - Iglesia San Luis de los Franceses", "latitude":37.39839293165148, "longitude":-5.988294375456022}
		}