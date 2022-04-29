import socket
import datetime



def convert_data_to_influx_format(full_router_data):

    measurement = dict()
    measurement['measurement'] = 'ASUS-TUF-Gaming-Router'
    measurement['tags'] = {"host" : socket.gethostname()}
    measurement["time"] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    for ssid, ssid_index in enumerate(full_router_data):
        measurement["fields"]["SSID-{}".format(ssid_index)] = full_router_data[0][ssid_index]
        measurement["fields"]["Noise Level (dbM)"] = full_router_data[1][ssid_index]

    return measurement