from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS
import requests

import config.config as cnf
config = cnf.Config()

import data_formatter.data_formatter as formatter
import connectors.orion_connector_ld as orion
import connectors.mysql_connector as mysql
import rule_engine.rule_engine as rule_engine
import core.building_service as building
import utils.generate_information as generate

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

#ORION
CB_URI_LD = config.context_broker_uri_ld
SUB_URI_LD = config.subscription_uri_ld
CB_TYPES = config.context_broker_types
NIFI_NOTIFY_URI = config.nifi_notify_uri

BUILDING_SERVICE_NAME = config.building_service

RULE_TABLE = config.mysql_alert_table
DATABASE = config.mysql_db

FIELDS_INDEXES_UPDATE = config.fields_index_update

class Health(Resource):
    def get(self):
        return {"Status":"OK"}, 200

class PublishIndex(Resource):
	def post(self, id):
		try:
			print("Received post of {0}".format(id))
			post_json_received = request.get_json()
			receied_dict_data = post_json_received["data"][0]
			print(receied_dict_data)
			
			service_name = request.headers["fiware-service"]
			headers={'fiware-service': service_name,
				'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
			}
			
			#id -> co2 or tvoc or multisensor
			list_field = formatter.get_index_fields(id)
			dict_data_level = {}

			for field in list_field:
				field_value = receied_dict_data[field]["value"]
				dict_data_level[FIELDS_INDEXES_UPDATE[id][field]] = formatter.calculate_level(field, field_value)
			
			# format to json
			json_update = formatter.parse_data(dict_data_level)
			print(json_update)
			
			response = orion.update_specific_data(CB_URI_LD, receied_dict_data["id"], headers, json_update)	
			print(response.status_code)
			print(response.content)
			
			return 200

		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

#This method received the notification of all dat from orion and it executes the rule engine
class Notifications(Resource):
	def post(self):
		try:
			#Get data from request received
			post_json_received  = request.get_json()
			service_name = request.headers["fiware-service"]
			dict_data = post_json_received["data"][0]
    
			#process received data
			list_attributes = formatter.parse_received_data_rule_engine()
			list_data_rule_engine = formatter.data_to_rule_engine(service_name, dict_data, list_attributes)
			
			#Load the rules in mysql
			list_rules = rule_engine.load_rules()
			
			#For every rule to be analyzed is processed into rule engine
			for data_rule in list_data_rule_engine:
				print(data_rule)
				rule_engine.evaluate_rules(service_name, list_rules, data_rule)
            
			return {"Status":"OK"}, 200
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

class User(Resource):
	def post(self):
		try:
			post_json_received = request.get_json()
			if post_json_received['register']:
				response, code = formatter.register_user(post_json_received)
			else:
				response, code = formatter.login_user(post_json_received)
			return response, code
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
			print(response)
			return response, 500		
	def delete(self,id):
		try:
			# post_json_received = request.get_json()
			response, code = formatter.delete_user(id)
			return response,code
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
			print(response)
			return response, 500
	def put(self):
		try:
			post_json_received = request.get_json()
			response, code = formatter.update_user(post_json_received)
			return response,code
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
			print(response)
			return response, 500

class Categories(Resource):
	def get(self):
		try:
			mydb = mysql.connect()
			query = "SELECT category.value FROM category "
			query_result = mysql.select_query(mydb, query)
			response = formatter.single_value_tuple_list_to_list(query_result)
			return response, 200, {'Access-Control-Allow-Origin': '*'} 
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

class SubCategories(Resource):
	def get(self, category):
		try:
			mydb = mysql.connect()
			query_cat_id = "SELECT category.id FROM category WHERE category.value = '{0}'".format(category)
			query_cat_result = mysql.select_query(mydb, query_cat_id)
			single_value = query_cat_result[0][0]
			query = "SELECT subcategory.value FROM relational JOIN subcategory ON relational.id_subcategory = subcategory.id WHERE relational.id_category = {0}".format(single_value)
			query_result = mysql.select_query(mydb, query)
			response = formatter.single_value_tuple_list_to_list(query_result)
			return response, 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response, {'Access-Control-Allow-Origin': '*'}

class Severity(Resource):
	def get(self):
		try:
			mydb = mysql.connect()
			query = "SELECT severity.value FROM severity "
			query_result = mysql.select_query(mydb, query)
			response = formatter.single_value_tuple_list_to_list(query_result)
			return response, 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

class RuleEngine(Resource):
	def get(self):
		try:
			mydb = mysql.connect()
			query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{0}' AND TABLE_NAME='{1}'".format(DATABASE,RULE_TABLE)#databasename and table name
			column_query = mysql.select_query(mydb, query)
			column_list = formatter.single_value_tuple_list_to_list(column_query)

			rule_query = "SELECT * FROM rules"#.format("rules")
			rule_query_result = mysql.select_query(mydb, rule_query)

			response = formatter.create_rule_json(rule_query_result, column_list)

			return response, 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

	def delete(self, id):
		try:
			mydb = mysql.connect()
			service_subs_query = "SELECT service_name, subscription_id FROM {0} WHERE id = {1}".format(RULE_TABLE, id)
			service_subs = mysql.select_query(mydb, service_subs_query)
			query = "DELETE FROM {0} WHERE id = {1}".format(RULE_TABLE,id)
			response = mysql.delete_query(mydb, query)

			delete_header = {
								'fiware-service': service_subs[0][0],
								'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
							}

			orion.request_delete_data(SUB_URI_LD, delete_header, service_subs[0][1])
			#Delete from orion

			return response, 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

	def post(self):
		try:
			post_json_received = request.get_json()
			mydb = mysql.connect()
			query = "SELECT COLUMN_NAME  FROM INFORMATION_SCHEMA.COLUMNS  WHERE TABLE_SCHEMA='{0}' AND TABLE_NAME='{1}'".format(DATABASE, RULE_TABLE)#databasename and table name
			column_query = mysql.select_query(mydb, query)
			print("PRE FOR")
			for rule in post_json_received:
				headers = {
							'fiware-service': rule["service_name"],
							'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
						}
				response = ""
				bool_update = False
				request_json = requests.get(CB_TYPES+"?details=true", headers=headers).json()
				print("REQUEST")
				if type(request_json) is dict:
					error_message = 'The service does not exists'
					raise Exception(error_message)
				elif rule["attribute_name"] not in request_json[0]["attributeNames"]:
					error_message = 'The attribute does not belong to the service'
					raise Exception(error_message)
				print("VALIDATION")
				if rule["id"] != "":
					try:
						#In case we need to delete subs and service changed
						query_service = "SELECT service_name FROM rules WHERE id = {0}".format(rule["id"])
						service_result = mysql.select_query(mydb, query_service)
						delete_header = {
							'fiware-service': service_result[0][0],
							'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
						}

						rule_json_values = formatter.get_rule_values_from_json(rule)
						query_set = formatter.get_columns_string_for_update(column_query)
						query_set = query_set % rule_json_values
						query_set = query_set.rstrip(',')
						query = "UPDATE {0} SET {1} WHERE id={2}".format(RULE_TABLE, query_set, rule["id"])
						query_result = mysql.update_query(mydb,query)
						if query_result[0] != 0:
							
							#DELETE SUBS
							orion.request_delete_data(SUB_URI_LD, delete_header, rule["subscription_id"])

							subs_json = formatter.create_subscription_json(rule)

							response = orion.create_subscription(SUB_URI_LD, headers, subs_json)
							bool_update = True
					except Exception as ex:
						response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
						print(response)
						return response
				else:
					try:
						print("POSTING")
						#POST TO ORION
						subs_json = formatter.create_subscription_json(rule)
						
						response = orion.create_subscription(SUB_URI_LD, headers, subs_json)
						
					except Exception as ex:
						response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
						print(response)
						return response
						
				if response != "" and response.status_code >= 200 and response.status_code < 300:
					subscription_id = ''
					check_subscription_content = orion.check_existing_sub(SUB_URI_LD, headers).json()
					
					if len(check_subscription_content) > 0:
						for i in range(len(check_subscription_content)):
							if subs_json["description"] == check_subscription_content[i]["description"]:
								subscription_id = check_subscription_content[i]["id"]
								break
								
					if subscription_id == '':
						error_message = 'Could not locate the id of the subscription'
						raise Exception(error_message)
					else:
						if bool_update:
							rule["subscription_id"]=subscription_id
							query = "UPDATE {0} SET subscription_id='{1}' WHERE id = {2}".format(RULE_TABLE, subscription_id, rule["id"])					
							response = mysql.update_query(mydb, query)
						else:
							rule["subscription_id"]=subscription_id		
							rule_json_values = formatter.get_rule_values_from_json(rule)
							column_list = []
							for column in column_query:
								column_list.append(column[0])
							column_tuple = tuple(column_list[1:])
							query = "INSERT INTO {0} {1} VALUES %s".format(RULE_TABLE, str(column_tuple).replace("'",""))					
							query = query % str(rule_json_values)
							response = mysql.insert_query(mydb, query)
			return 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

class Attributes(Resource):
	def get(self, service):
		try:
			headers = {'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' , 'fiware-service': service}
			request_json = requests.get(CB_TYPES+"?details=true", headers=headers).json()
			if type(request_json) is dict:
				error_message = 'The service does not exists, could not load attributes'
				raise Exception(error_message)
			else:
				response = request_json[0]["attributeNames"]
			return response, 200, {'Access-Control-Allow-Origin': '*'}
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}, 500
			print(response)
			return response

class PeopleCam(Resource):
	def post(self):
		try:
			post_json_received = request.get_json()
			print(post_json_received)
			bool_received_payload_list = isinstance(post_json_received, list)

			if bool_received_payload_list:
				#SELECT MYSQL
				db_connector = mysql.connect()
				current_date = generate.current_date()
				current_people_count = formatter.get_current_count(db_connector, current_date)
				future_people_count = current_people_count
				string_now_tz, update_datetime = generate.datetime_time_tz()

				for json_payload in post_json_received:
					valid_payload, dict_data = formatter.check_people_cam_payload(json_payload)

					if valid_payload:
						print(dict_data)
						if dict_data["direction"] == 'forward':
							future_people_count = current_people_count+1
						else:
							future_people_count = current_people_count-1
						
						update_datetime = dict_data["dateObserved"]
					else:
						response = {"Message": "Something went wrong.", "Exception": "Not valid json inside the list (missing/invalid fields). Json: {0}".format(json_payload)}
						#print(response)

				if future_people_count < 0:
					future_people_count = 0

				if future_people_count != current_people_count:
					print(future_people_count)
					#Publish information
					building.execute_building_sensor(BUILDING_SERVICE_NAME, update_datetime, future_people_count)

					#UPDATE MYSQL
					result = formatter.update_current_count(db_connector, future_people_count, current_date)
					print(result)

				return 200
			else:
				response = {"Message": "Something went wrong.", "Exception": "Payload is not a list: {0}".format(type(post_json_received))}
				print("Payload is not a list: {0} -> {1}".format(type(post_json_received), post_json_received))
				return response, 500
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
			print(response)
			return response, 500

class PeopleCamStatus(Resource):
	def post(self):
		try:
			data = request.data
			#print(data)
			#post_json_received = request.get_json()
			#print(post_json_received)
			#print("PeopleCamStatus")
			return 200
		except Exception as ex:
			response = {"Message": "Something went wrong.", "Exception type": type(ex).__name__, "Exception": str(ex)}
			print(response)
			return response, 500

api.add_resource(Health, "/health")
api.add_resource(PublishIndex, "/index/<id>")
api.add_resource(Notifications, "/notifications")
api.add_resource(User,"/user", "/user/<id>")
api.add_resource(Categories, "/categories")
api.add_resource(SubCategories, "/subcategories/<string:category>")
api.add_resource(Severity, "/severity")
api.add_resource(RuleEngine, "/rule-engine", "/rule-engine/<id>")
api.add_resource(Attributes, "/attributes/<string:service>")
api.add_resource(PeopleCam, "/peoplecam")
api.add_resource(PeopleCamStatus, "/peoplecam/status")

if __name__ == "__main__":
    app.run(debug=True)
