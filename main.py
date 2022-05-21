import yaml
import query
import influx_handler
import time
import pdb

with open("config.yml", "r") as yaml_file:

    config_yaml_obj = yaml.safe_load(yaml_file)

    influx_client = influx_handler.initialize_influx_client()
    
    while True:
        extracted_info = query.extract_wireless_radio_info(config_yaml_obj['router_web_url'], config_yaml_obj['asus_token_cookie'], config_yaml_obj['user_agent'])

        if extracted_info == '':
            print("Error: Unable to retrieve wireless radio information. Make sure your login information is correct")
            exit(1)

        influx_measurement = influx_handler.convert_data_to_influx_format(extracted_info)
        influx_handler.send_data_to_influx(influx_client, influx_measurement)
        time.sleep(5)