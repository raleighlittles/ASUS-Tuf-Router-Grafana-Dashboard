import requests
import pdb
import urllib.parse
import typing

def query_wireless_info(url, login_cookie, user_agent) -> str:

    header = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Host': 'router.asus.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': user_agent }

    cookies = { 'asus_token' : login_cookie, 'clickedItem_tab': '0' }

    resp = requests.get(url, cookies=cookies, headers=header, allow_redirects=False)
    
    # If the login info was wrong, the server will return with the login prompt, instead of the valid data that we want
    if (resp.ok) and (len(resp.text) > 100):
        # To remove byte order mark
        resp.encoding = "utf-8-sig"
        return resp.text.split("\n")

    else:
        print("Error querying wireless info from router @ ", url, " | status_code =", resp.status_code, "response length = ", len(resp.text))
        raise Exception("Error: Unable to retrieve wireless radio information. Make sure your login information is correct")


def extract_wireless_radio_info(url, login_cookie, user_agent) -> typing.List:

    raw_wireless_info = query_wireless_info(url, login_cookie, user_agent)

    # Router has multiple SSIDs; one for each frequency band (2.4 GHz, 5 GHz, etc.)
    # The format goes: SSID on one line, then Noise on the next (See docs for more info)
    ssid_list, noise_val_list = [], []
    
    for line in raw_wireless_info:
        if line.startswith('SSID'):
            ssid = extract_ssid_name(line.split()[1])
            ssid_list.append(ssid)

        elif 'noise' in line:
            noise_level_value = line.split()[1]
            # Add the noise level measurement to the last seen SSID
            noise_val_list.append(noise_level_value)

    return [ssid_list, noise_val_list]

def extract_ssid_name(text) -> str:
    """
    Extract SSID from wireless info
    See docs for an example of the SSID string
    """
    return urllib.parse.unquote(text.strip("\""))