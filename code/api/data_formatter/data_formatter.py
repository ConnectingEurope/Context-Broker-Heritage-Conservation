from flask.wrappers import Response

import connectors.mysql_connector as mysql
import connectors.orion_connector_ld as orion
import utils.generate_information as generate
import config.config as cnf
config = cnf.Config()

#RULE ENGINE CONSTANTS
RULE_ATTRIBUTE_COLUMN = config.mysql_alert_attribute_column
RULE_ENGINE_TABLE = config.mysql_alert_table
ENTITY_TYPES = config.entity_types
NOTYFY_API_URI = config.api_notify_uri+"notifications"
ID_PEOPLE_COUNT = config.id_people_count
TABLE_PEOPLE_COUNT = config.table_people_count
COLUMN_NAME_DATETIME = config.column_name_datetime
COLUMN_NAME_COUNT = config.column_name_people

def get_index_fields(id):
    if id == "co2":
        selected_fields = config.fields_index_received["co2"]
    elif id == "tvoc":
        selected_fields = config.fields_index_received["tvoc"]
    elif id == "multisensor":
        selected_fields = config.fields_index_received["multisensor"]
    else:
        exception_message = "Index id doesn't exist '{0}'".format(id)
        raise Exception(exception_message)
    print(selected_fields)    
    return selected_fields 

def calculate_level(field, field_value):
    result_level = ""

    if field == "co2":
        result_level = calculate_co2_level(field_value)
    elif field == "tvoc":
        result_level = calculate_tvoc_level(field_value)

    return result_level

def calculate_tvoc_level(tvoc_value):
    tvoc_level= ''

    if tvoc_value <= 60:
        tvoc_level="very good"
    if tvoc_value > 60 and tvoc_value <= 200:
        tvoc_level="good"
    elif tvoc_value > 200 and tvoc_value <= 600:
        tvoc_level="medium"
    elif tvoc_value > 600 and tvoc_value <= 2000:
        tvoc_level="poor"
    elif tvoc_value > 2000:
        tvoc_level="very poor"

    return tvoc_level

def calculate_co2_level(co2_value):
    co2_level= ''

    if co2_value <= 600:
        co2_level="very good"
    elif co2_value > 600 and co2_value <= 1000:
        co2_level="good"
    elif co2_value > 1000 and co2_value <= 1500:
        co2_level="medium"
    elif co2_value > 1500 and co2_value <= 2000:
        co2_level="poor"
    elif co2_value > 2000:
        co2_level="very poor"

    return co2_level

def parse_data(dict_data):
    json_update = { }

    for key in dict_data:
        json_update[key] = {"type": "Property", "value": dict_data[key]}
    
    return json_update

def parse_co2_data(co2_level):
    co2_json_update = {
        "co2Level": {"type": "Property", "value": co2_level}
    }
    
    return co2_json_update
    
#This method parse the rule engine dat received from the post
def parse_received_data_rule_engine():
	#Select of the fields of the current rules
	mysql_connector = mysql.connect()
	query = "SELECT {0} FROM {1}".format(RULE_ATTRIBUTE_COLUMN, RULE_ENGINE_TABLE)        
	mysql_result = mysql.select_query(mysql_connector, query)
	
	list_attributes = []
	
	#If there are eisting rules, we add to the list the name of the values to be checked.
	if len(mysql_result) > 0:
		for (attribute,) in mysql_result:
			list_attributes.append(str(attribute))
			
	return list_attributes

#This method creates a dictionary for every rule depending on the received fields.
def data_to_rule_engine(service, dict_data, list_attributes):
	list_data_rules = []
	for attribute in list_attributes:
		if attribute in dict_data:
			data = {"service": service,
					"attribute": attribute,
					"dateObserved": dict_data["dateObserved"],
					"value": dict_data[attribute]["value"],
					"dataProvider" : dict_data["dataProvider"]
					}
			list_data_rules.append(data)
               
	return list_data_rules
#This method check the log in parameters
def login_user(user_data):
    db_connector = mysql.connect()
    query="SELECT * FROM web_users where email='{0}' and password='{1}'".format(user_data['email'], user_data['password'])
    user_info = mysql.select_query(db_connector, query)
    
    if len(user_info) == 0:
        exception_message = "Incorrect user or password"
        raise Exception(exception_message)
    else:
        response = {
            "id"                    : user_info[0][0],
            "username"              : user_info[0][1],
            "email"                 : user_info[0][2],
            "name"                  : user_info[0][4],
        }
        
    return response, 200

#This method registers a user to the mysql
def register_user(user_data):
    db_connector = mysql.connect()
    query="INSERT INTO web_users(username, email, password, name) VALUES('{0}','{1}','{2}','{3}')".format(user_data['username'],user_data['email'], user_data['password'],user_data['name'])
    user_info, code = mysql.insert_query(db_connector, query)

    if not isinstance(user_info, int):
        exception_message = "Missing fields. Fill all the required fields."
        raise Exception(exception_message)
    else:
        response = {
            "id" : user_info
        }

    return response, code
def update_user(user_data):
    db_connector = mysql.connect()
    query="UPDATE web_users SET name='{0}' WHERE id={1}".format(user_data['name'],user_data['id'])
    code = mysql.update_query(db_connector, query)

    if code != 200:
        exception_message = "Could not update. Check updated fields."
        raise Exception(exception_message)
    else:
        response={
            "message" : "user successfully updated."
        }
    return response,code
def delete_user(id):
    db_connector = mysql.connect()
    query="DELETE FROM web_users WHERE id={0}".format(id)
    code = mysql.delete_query(db_connector, query)

    if code != 200:
        exception_message = "Could not delete the user."
        raise Exception(exception_message)
    else:
        response={
            "message" : "user successfully deleted."
        }
    return response,code

#This method transforms a list of tuples with a sigle value [ (value1, ), (value2,), ...] to a list [value1, value2, ...]
def single_value_tuple_list_to_list(tuple_list):
    return [item for t in tuple_list for item in t]

#This method creates a json to be sent to the front end 
def create_rule_json( query_result, column_list ):
    json_result = []
    
    for q in query_result:
        row = {}
        for i in range(len(column_list)):
            row[column_list[i]] = q[i]
        
        json_result.append(row)

    return json_result

#This method extracts the values of a json to create a tuple
def get_rule_values_from_json( json ):
    list_temp = [ json["rule_name"], json["service_name"], json["entity_type"], json["attribute_name"],
    json["operator"], json["threshold"], json["value_category"],json["value_subcategory"], json["value_severity"],
    json["subscription_id"], json["recurrence_seconds"] ]
    tuple_res = []
    for value in list_temp:
        if value == None:
            value = 'NULL'
        tuple_res.append(value)
    return tuple(tuple_res)

    
#This method creates the string set for an update query for rules
def get_columns_string_for_update( column_tuple ):
    update_set = ""
    aux_tuple = column_tuple[1:]
    for field in aux_tuple:
        if field[0] == "recurrence_seconds" or field[0] == "threshold":
            update_set = update_set + str(field[0])+'=%s,'
        else:
            update_set = update_set + str(field[0])+'="%s",'
    update_set = update_set.rstrip(',')
    return update_set

#This method creates a subscription json
def create_subscription_json( rule_dic ):
	sub_description_alert = "Notify API of {0} {1} {2}".format(rule_dic["attribute_name"], rule_dic["operator"], rule_dic["threshold"])
	list_sub_parameters = ["dateObserved", "dataProvider", rule_dic["attribute_name"]]
	rule_dic["entity_type"]= ENTITY_TYPES[rule_dic["service_name"]]
	if int(rule_dic["recurrence_seconds"]) != 0:
		subs_json = orion.create_json_subscription_alert_condition(sub_description_alert, rule_dic["entity_type"],list_sub_parameters,NOTYFY_API_URI, int(rule_dic["recurrence_seconds"]) )
	else:
		subs_json = orion.create_json_subscription_no_condition(sub_description_alert, rule_dic["entity_type"],list_sub_parameters,NOTYFY_API_URI)
	
	return subs_json

def get_current_count(db_connector, current_date):
    current_people_count = 0
    #Check if there is any record
    query_people_count = "SELECT * FROM {0} WHERE id={1}".format(TABLE_PEOPLE_COUNT, ID_PEOPLE_COUNT)
    result_select = mysql.select_query(db_connector, query_people_count)
    if len(result_select) == 0:
        #Insert
        current_people_count = 0
        query_people_count = "INSERT INTO {0} (id, {1}, {2}) VALUES ({3}, {4}, '{5}')".format(TABLE_PEOPLE_COUNT, COLUMN_NAME_COUNT, COLUMN_NAME_DATETIME, ID_PEOPLE_COUNT, current_people_count, current_date)
        result_select = mysql.insert_query(db_connector, query_people_count)
    else:
        #Select
        query_people_count = "SELECT {0} FROM {1} WHERE id={2} AND {3}='{4}'".format(COLUMN_NAME_COUNT, TABLE_PEOPLE_COUNT, ID_PEOPLE_COUNT, COLUMN_NAME_DATETIME, current_date)
        result_select = mysql.select_query(db_connector, query_people_count)

        if len(result_select) > 0:
            current_people_count = result_select[0][0]

    return current_people_count

def update_current_count(db_connector, current_count, current_date):
    query_people_count = "UPDATE {0} SET {1}={2}, {3}='{4}' WHERE id={5}".format(TABLE_PEOPLE_COUNT, COLUMN_NAME_COUNT, current_count, COLUMN_NAME_DATETIME, current_date, ID_PEOPLE_COUNT)
    result_select = mysql.update_query(db_connector, query_people_count)

    return result_select

def check_people_cam_payload(people_cam_payload):
    valid_payload = True
    dict_data = {}

    if {"direction", "objectType", "timestamp"} <= set(people_cam_payload):
        json_direction = people_cam_payload["direction"]
        json_type = people_cam_payload["objectType"]
        json_type_count = people_cam_payload["type"]
        json_datetime = generate.convert_timestamp_xovis(people_cam_payload["timestamp"])
        if (json_direction == 'forward' or json_direction == 'backward') and json_type == 'PERSON' and json_type_count =='LineCrossing':
            valid_payload = True
            dict_data["direction"] = json_direction
            dict_data["objectType"] = json_type
            dict_data["dateObserved"] = json_datetime
        else:
            valid_payload = False
    else:
        valid_payload = False

    return valid_payload, dict_data

if __name__ == "__main__":
    db_connector = mysql.connect_local()
    current_date = '2021-06-05'
    result = update_current_count(db_connector, 3, current_date)
    print(type(result))
    print(result)

