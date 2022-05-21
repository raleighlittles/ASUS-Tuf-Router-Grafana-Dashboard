import socket
import datetime
import influxdb
import pdb
import yaml
import typing

influx_yaml_config_location = "influx_config.yml"

def read_influx_config_setting(setting_name) -> str:
    """
    Simple helper method; reads a setting (currently from a YAML file)
    """

    with open(influx_yaml_config_location, "r") as influx_yaml_file:
        influx_yaml_obj = yaml.safe_load(influx_yaml_file)
        return influx_yaml_obj[setting_name]


def initialize_influx_client():

    influx_client = influxdb.InfluxDBClient(host='localhost', port= read_influx_config_setting("port"))
    database_name = read_influx_config_setting("db_name")

    database_list = influx_client.get_list_database()
    if all([database['name'] != database_name for database in database_list]):
        print("Desired database name {} does not exist, creating one now".format(database_name))
        influx_client.create_database(database_name)

    return influx_client


def convert_data_to_influx_format(full_router_data) -> typing.List:

    measurement = dict()
    measurement['measurement'] = 'ASUS-TUF-Gaming-Router'
    measurement['tags'] = {"host" : socket.gethostname()}
    measurement["time"] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    measurement["fields"] = dict()

    for ssid_index in range(0, len(full_router_data)):
        measurement["fields"]["SSID-{}".format(ssid_index)] = full_router_data[0][ssid_index]
        measurement["fields"]["Noise Level (dbM) - SSID-{}".format(ssid_index)] = int(full_router_data[1][ssid_index])

    return [measurement]


def send_data_to_influx(influx_client, json_data_array):
    """
    Uses the InfluxDB Python API to send data.
    """
    influx_client.switch_database(read_influx_config_setting('db_name'))
    bool_response = influx_client.write_points(json_data_array)

    return bool_response