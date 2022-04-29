from numpy import extract
import requests
import pdb
import urllib.parse


wireless_url = "http://router.asus.com/wl_log.asp"

def query_wireless_info(url, login_cookie) -> str:

    header = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Host': 'router.asus.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36' }

    cookies = { 'asus_token' : login_cookie, 'clickedItem_tab': '0' }

    resp = requests.get(url, cookies=cookies, headers=header, allow_redirects=False)
    
    #pdb.set_trace()

    # If the login info was wrong, the server will return with the login prompt, instead of the valid data that we want
    if (resp.ok) and (len(resp.text) > 100):
        return resp.text.split("\n")

    else:
        print("Error querying wireless info from router @ ", url, " | status_code =", resp.status_code, "response length = ", len(resp.text))
        return ''


def extract_wireless_radio_info(url, login_cookie):

    raw_wireless_info = query_wireless_info(url, login_cookie)

    # Router has multiple SSIDs; one for each frequency band (2.4 GHz, 5 GHz, etc.)
    # The format goes: SSID on one line, then Noise on the next (See docs for more info)
    ssid_list, noise_val_list = [], []
    
    for line in raw_wireless_info:
        if 'SSID' in line:
            ssid = extract_ssid_name(line.split()[1])
            print("SSID found: ", ssid)
            ssid_list.append(ssid)

        elif 'noise' in line:
            noise_level_value = line.split()[1]
            print("Noise level value at ", noise_level_value, " dBm")
            # Add the noise level measurement to the last seen SSID
            noise_val_list.append(noise_level_value)

    return [ssid_list, noise_val_list]

def extract_ssid_name(text) -> str:
    # Extact SSID from wireless info
    # See docs for an example of the SSID string
    return urllib.parse.unquote(text.strip("\""))