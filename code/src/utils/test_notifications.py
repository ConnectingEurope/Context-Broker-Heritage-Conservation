import time

import connectors.mysql_connector as mysql
import connectors.orion_connector_ld as orion
import rule_engine.rules.rules as rules
import config.config as cnf

config = cnf.Config()
MYSQL_DT = config.mysql_alert_table
COLUMN_NAMES_RULES = config.mysql_alert_columns
SUB_URI_LD = config.subscription_uri_ld_local

# Functions that create/update the information of Bike Lanes in the CB
if __name__ == "__main__":
    #Retrive info data base
    db_connector = mysql.connect_local()
    mysql_result = mysql.select_query(db_connector, 'SELECT {0} FROM {1}'.format(COLUMN_NAMES_RULES, MYSQL_DT))
    #print(mysql_result)
    list_rules = []

    if len(mysql_result) > 0: 
        for (rule_id, service_name, entity_type, attribute_name, operator, max_threshold, value_category, value_subcategory, value_severity, subscription_id, recurrence_seconds) in mysql_result:
            rule_class = rules.Rule(rule_id, service_name, entity_type, attribute_name, operator, max_threshold, value_category, value_subcategory, value_severity, '', recurrence_seconds)
            print(rule_class)
            list_rules.append(rule_class)

    for rule in list_rules:
        print(rule.id)
        #Create JSON subcscription
        sub_description_alert = "Notify Elastic-Alerts of {0}".format(rule.attribute)
        list_sub_parameters = ["dateObserved", "dataProvider", rule.attribute]
        notify_uri = 'http://flask-server-container:5000/notifications'

        if isinstance(rule.secondsToWait, int):
            print("INT")
            subscription_json = orion.create_json_subscription_alert_condition(sub_description_alert, rule.entityType, list_sub_parameters, notify_uri, rule.secondsToWait)
        else:
            print("NO INT")
            subscription_json = orion.create_json_subscription_no_condition(sub_description_alert, rule.entityType, list_sub_parameters, notify_uri)
        
        print(subscription_json)

        headers = {
            'fiware-service': rule.serviceName,
            'Link': '<https://smartdatamodels.org/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
        }

        response = orion.create_subscription(SUB_URI_LD, headers, subscription_json)
        print(response.status_code)
        print(response.content)

        if response.status_code >= 200 and response.status_code < 300:
            subscription_id = ''
            check_subscription = orion.check_existing_sub(SUB_URI_LD, headers)
            check_subscription_content = check_subscription.json()
            print("SUB CONTENT")
            print(check_subscription_content)

            if len(check_subscription_content) > 0:
                for i in range(len(check_subscription_content)):
                    if subscription_json["description"] == check_subscription_content[i]["description"]:
                        subscription_id = check_subscription_content[i]["id"]
                        break
            
            if subscription_id == '':
                error_message = 'Could not locate the id of the subscription'
                raise Exception(error_message)
            else:
                update_query = mysql.update_query(db_connector, "UPDATE {0} SET subscription_id='{1}' WHERE id={2}".format(MYSQL_DT, subscription_id, rule.id))
                print("MYSQL UPDATE RESULT: {0}".format(update_query))

    time.sleep(2)
