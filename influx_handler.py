import socket
import datetime
import influxdb

def initialize_influx(database_name, influx_db_port):
    influx_client = influxdb.InfluxDBClient(host='localhost', port=influx_db_port)

    database_list = influx_client.get_list_database()
    if all([database['name'] != database_name for database in database_list]):
        print("Desired database name {} does not exist, creating one now".format(database_name))
        influx_client.create_database(database_name)

    return influx_client


def convert_data_to_influx_format(full_router_data):

    measurement = dict()
    measurement['measurement'] = 'ASUS-TUF-Gaming-Router'
    measurement['tags'] = {"host" : socket.gethostname()}
    measurement["time"] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    for ssid, ssid_index in enumerate(full_router_data):
        measurement["fields"]["SSID-{}".format(ssid_index)] = full_router_data[0][ssid_index]
        measurement["fields"]["Noise Level (dbM)"] = full_router_data[1][ssid_index]

    return measurement


def send_data_to_influx(influx_client, json_data_array):
    """
    Uses the InfluxDB Python API to send data.
    """
    influx_client.switch_database('ups')
    bool_response = influx_client.write_points(json_data_array)

    return bool_response