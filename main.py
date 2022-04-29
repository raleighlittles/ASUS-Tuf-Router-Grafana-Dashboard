import yaml
import query
import influx_handler

with open("config.yml", "r") as yaml_file:

    config_yaml_obj = yaml.safe_load(yaml_file)

    influx_client = influx_handler.initialize_influx(config_yaml_obj['influx_db']['database_name'], config_yaml_obj['influx_db']['port'])
    
    # Run this next section on a loop
    extracted_info = query.extract_wireless_radio_info(config_yaml_obj['router_web_url'], config_yaml_obj['asus_token_cookie'])
    influx_measurement = influx_handler.convert_data_to_influx_format(extracted_info)
    influx_handler.send_data_to_influx(influx_client, influx_measurement)
