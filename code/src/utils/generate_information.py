import datetime
import pytz
import random

aemet_wave_low=310
aemet_wave_medium=320
aemet_wave_high=330
first_period = '00-24'
second_period = '12-24'
third_period = '12-18'

# Functions that generates a random value of air quality index for no2 -> 0-229
def generate_random_no2(datetime_hour): 
	if(datetime_hour.hour < 7):
		no2= random.randint(0, 75)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 10):
		no2= random.randint(50, 100)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 20):
		no2= random.randint(100, 229)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		no2= random.randint(50, 100)	
	else:
		no2= random.randint(0, 75)
	
	return no2

def generate_random_so2(datetime_hour): 
	if(datetime_hour.hour < 7):
		so2= random.randint(0, 75)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 10):
		so2= random.randint(50, 100)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 20):
		so2= random.randint(100, 229)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		so2= random.randint(50, 100)	
	else:
		so2= random.randint(0, 75)
	
	return so2

def generate_random_co2_ppm(datetime_hour): 
	if(datetime_hour.hour < 7):
		co2= random.randint(0, 300)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 14):
		co2= random.randint(2000, 3000)
	elif (datetime_hour.hour >= 14 and datetime_hour.hour < 22):
		co2= random.randint(1000, 3000)
	elif (datetime_hour.hour >= 22 and datetime_hour.hour <= 23):
		co2= random.randint(0, 300)	
	else:
		co2= random.randint(0, 300)
	
	return co2

def generate_random_illuminance(datetime_hour): 
	if(datetime_hour.hour < 7):
		illuminance= random.randint(0, 50)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 14):
		illuminance= random.randint(300, 600)
	elif (datetime_hour.hour >= 14 and datetime_hour.hour < 19):
		illuminance= random.randint(200, 500)
	elif (datetime_hour.hour >= 19 and datetime_hour.hour <= 23):
		illuminance= random.randint(0, 50)	
	else:
		illuminance= random.randint(0, 50)
	
	return illuminance
	
# Functions that generates a random value of air quality index for o3 -> 0-239
def generate_random_o3(datetime_hour): 
	if(datetime_hour.hour < 7):
		o3= random.randint(0, 100)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 10):
		o3= random.randint(100, 150)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 20):
		o3= random.randint(150, 239)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		o3= random.randint(100, 175)	
	else:
		o3= random.randint(0, 50)
	
	return o3

# Functions that generates a random value of air quality index for pm10 -> 0-150+
def generate_random_pm10(datetime_hour): 
	if(datetime_hour.hour < 7):
		pm10= random.randint(0, 10)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 10):
		pm10= random.randint(10, 20)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 20):
		pm10= random.randint(20, 150)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		pm10= random.randint(20, 40)	
	else:
		pm10= random.randint(0, 20)
	
	return pm10

# Functions that generates a random value of air quality index for pm10 -> 0-150+
def generate_random_tvoc(datetime_hour): 
	if(datetime_hour.hour < 7):
		tvoc= random.randint(10, 200)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 10):
		tvoc= random.randint(200, 5000)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 20):
		tvoc= random.randint(200, 10000)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		tvoc= random.randint(10, 200)	
	else:
		tvoc= random.randint(10, 200)
	
	return tvoc

# Functions that generates a random value of air quality index for pm10 -> 0-150+
def generate_random_ap(datetime_hour): 
	ap= random.randint(900, 1100)
	
	return ap

# Functions that generates a random value of air quality index for pm25 -> 0-75+
def generate_random_pm25(datetime_hour): 
	if(datetime_hour.hour < 7):
		pm25= random.randint(0, 10)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 10):
		pm25= random.randint(10, 20)
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 20):
		pm25= random.randint(20, 75)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		pm25= random.randint(20, 40)	
	else:
		pm25= random.randint(0, 20)
	
	return pm25

def generate_temperature_random(datetime_hour):
	if(datetime_hour.hour < 7):
		temperature= random.randint(5, 12)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 12):
		temperature= random.randint(12, 15)
	elif (datetime_hour.hour >= 12 and datetime_hour.hour < 20):
		temperature= random.randint(18, 25)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		temperature= random.randint(12, 15)	
	else:
		temperature= random.randint(12, 15)
	
	return temperature

def generate_humidity_random(datetime_hour):
	if(datetime_hour.hour < 7):
		humidity= random.randint(50, 80)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 12):
		humidity= random.randint(10, 30)
	elif (datetime_hour.hour >= 12 and datetime_hour.hour < 20):
		humidity= random.randint(0, 15)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		humidity= random.randint(20, 40)	
	else:
		humidity= random.randint(10, 30)
	
	return humidity

def generate_wind_speed_random(datetime_hour):
	if(datetime_hour.hour < 7):
		wind_speed = random.randint(0, 8)
	elif (datetime_hour.hour >= 7 and datetime_hour.hour < 12):
		wind_speed= random.randint(5, 20)
	elif (datetime_hour.hour >= 12 and datetime_hour.hour < 20):
		wind_speed= random.randint(10, 20)
	elif (datetime_hour.hour >= 20 and datetime_hour.hour <= 23):
		wind_speed= random.randint(0, 12)	
	else:
		wind_speed= random.randint(0, 20)
	
	return wind_speed

def generate_building_occupancy_random(datetime_hour):
	if(datetime_hour.hour < 10):
		building_occupancy = 0
	elif (datetime_hour.hour >= 10 and datetime_hour.hour < 14):
		building_occupancy= random.randint(50, 300)
	elif (datetime_hour.hour >= 14 and datetime_hour.hour < 22):
		building_occupancy= random.randint(100, 500)
	elif datetime_hour.hour >= 22:
		building_occupancy= 0	
	else:
		building_occupancy= 0
	
	return building_occupancy
	
def generate_wind_dir_random():
	wind_direction_list = [0, 45, 90, 135, 180, -135, -90, -45]
	wind_direction = random.choice(wind_direction_list)
	
	return wind_direction

# Functions that generates a datetime from now to ISO 8601
def datetime_time_tz():
	datetime_spain = pytz.timezone("Europe/Madrid")
	datetime_now = datetime.datetime.now(datetime_spain)
	datetime_now_no_micro = datetime_now.replace(microsecond=0)
	string_now_tz = datetime_now_no_micro.isoformat()
	
	return string_now_tz, datetime_now_no_micro
	
# Function that converts the datetime of AEMET to ISO 8601
def convert_datetime_aemet(string_datetime):
	datetime_spain = pytz.timezone("Europe/Madrid")
	AEMET_datetime = datetime.datetime.strptime(string_datetime, '%Y-%m-%dT%H:%M:%S')
	AEMET_datetime_tz = pytz.timezone('Europe/Madrid').localize(AEMET_datetime)
	AEMET_datetime_iso = AEMET_datetime_tz.isoformat()

	return AEMET_datetime_iso

# Function that converts the datetime of LOWERIS to ISO 8601 - '2021-05-31T10:27:18.463753543Z'
def convert_datetime_loweris(string_datetime):
	datetime_split = string_datetime.split(".")
	datetime_zero = pytz.timezone("Etc/GMT+0")
	datetime_spain = pytz.timezone("Europe/Madrid")

	loweris_datetime = datetime.datetime.strptime(datetime_split[0], '%Y-%m-%dT%H:%M:%S')
	loweris_datetime_tz_0 = datetime_zero.localize(loweris_datetime)
	loweris_datetime_spain = loweris_datetime_tz_0.astimezone(datetime_spain)

	return loweris_datetime_spain

def convert_timestamp_xovis(timestamp):
	valid_timestamp = int(timestamp / 1000)
	datetime_timestamp = datetime.datetime.fromtimestamp(valid_timestamp, pytz.timezone("Europe/Madrid"))

	return datetime_timestamp

def current_date():
	date = datetime.datetime.now().strftime('%Y-%m-%d')

	return date

def generate_weather_type_random():
	weather_type_list = ['11', '12', '14', '17', '15', '11', '11', '11']
	weather_type = convert_AEMET_skystate(random.choice(weather_type_list))
	
	return weather_type

def generate_random_prob_precipitation():
	return random.randint(0, 100)

def generate_random_uvmax():
	return random.randint(0, 8)
		
# Function that converts the number of state of the sky from AEMET to a descriptive state of the sky
def convert_AEMET_skystate(sky_state_number):
	switcher={
		"11":"despejado",
		"11n":"despejado noche",
		"12":"poco nuboso",
		"12n":"poco nuboso noche",
		"13":"intervalos nubosos",
		"13n":"intervalos nubosos noche",
		"14":"nuboso",
		"14n":"nuboso noche",
		"15":"muy nuboso",
		"15n":"muy nuboso noche",
		"16":"cubierto",
		"16n":"cubierto noche",
		"17":"nubes altas",
		"17n":"nubes altas noche",
		"23":"intervalos nubosos con lluvia",
		"23n":"intervalos nubosos con lluvia noche",
		"24":"nuboso con lluvia",
		"24n":"nuboso con lluvia noche",
		"25":"muy nuboso con lluvia",
		"25n":"muy nuboso con lluvia noche",
		"26":"cubierto con lluvia",
		"26n":"cubierto con lluvia noche",
		"33":"intervalos nubosos con nieve",
		"33n":"intervalos nubosos con nieve noche",
		"34":"nuboso con nieve",
		"34n":"nuboso con nieve noche",
		"35":"muy nuboso con nieve",
		"35n":"muy nuboso con nieve noche",
		"36":"cubierto con nieve",
		"36n":"cubierto con nieve noche",
		"43":"intervalos nubosos con lluvia escasa",
		"43n":"intervalos nubosos con lluvia escasa noche",
		"44":"nuboso con lluvia escasa",
		"44n":"nuboso con lluvia escasa noche",
		"45":"muy nuboso con lluvia escasa",
		"45n":"muy nuboso con lluvia escasa noche",
		"46":"cubierto con lluvia escasa",
		"46n":"cubierto con lluvia escasa noche",
		"51":"intervalos nubosos con tormenta",
		"51n":"intervalos nubosos con tormenta noche",
		"52":"nuboso con tormenta",
		"52n":"nuboso con tormenta noche",
		"53":"muy nuboso con tormenta",
		"53n":"muy nuboso con tormenta noche",
		"54":"cubierto con tormenta",
		"54n":"cubierto con tormenta noche",
		"61":"intervalos nubosos con tormenta y lluvia escasa",
		"61n":"intervalos nubosos con tormenta y lluvia escasa noche",
		"62":"nuboso con tormenta y lluvia escasa",
		"62n":"nuboso con tormenta y lluvia escasa noche",
		"63":"muy nuboso con tormenta y lluvia escasa",
		"63n":"muy nuboso con tormenta y lluvia escasa noche",
		"64":"cubierto con tormenta y lluvia escasa",
		"64n":"cubierto con tormenta y lluvia escasa noche",
		"71":"intervalos nubosos con nieve escasa",
		"71n":"intervalos nubosos con nieve escasa noche",
		"72":"nuboso con nieve escasa",
		"72n":"nuboso con nieve escasa noche",
		"73":"muy nuboso con nieve escasa",
		"73n":"muy nuboso con nieve escasa noche",
		"74":"cubierto con nieve escasa",
		"74n":"cubierto con nieve escasa noche",
		"81":"niebla",
		"82":"bruma",
		"83":"calima",
		}

	return switcher.get(sky_state_number, "despejado")
	
# Functions that ensures the data from some AEMET aparameters, it checks if the parameter is not empty
def find_aemet_prediction_data(array_aemet, period_parameter, check_parameter, save_parameter):
	period_used = ""
	prediction_value = ""
	
	for aemet_element in array_aemet:
		if aemet_element[period_parameter] == first_period:
			if aemet_element[check_parameter] == "":
				continue
				#print("Period: {0} empty: {1}".format(first_period, aemet_element[check_parameter]))
			else:
				period_used = first_period
				prediction_value = aemet_element[save_parameter]
				#print("Period: {0} full: {1} value:{2}".format(first_period, aemet_element[check_parameter], aemet_element[save_parameter]))
				break
		elif aemet_element[period_parameter] == second_period:
			if aemet_element[check_parameter] == "":
				continue
				#print("Period: {0} empty: {1}".format(second_period, aemet_element[check_parameter]))
			else:
				period_used = second_period
				prediction_value = aemet_element[save_parameter]
				#print("Period: {0} full: {1} value:{2}".format(second_period, aemet_element[check_parameter], aemet_element[save_parameter]))
				break
			
		elif aemet_element[period_parameter] == third_period:
			if aemet_element[check_parameter] == "":
				continue
				#print("Period: {0} empty: {1}".format(third_period, aemet_element[check_parameter]))
			else:
				period_used = third_period
				prediction_value = aemet_element[save_parameter]
				#print("Period: {0} full: {1} value:{2}".format(third_period, aemet_element[check_parameter], aemet_element[save_parameter]))
				break
	
	return period_used, prediction_value

if __name__ == "__main__":
	result = current_date()
	print(result)
	print(type(result))