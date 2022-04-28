import requests
import pdb


wireless_url = "http://router.asus.com/wl_log.asp"

def query_wireless_info(url, login_cookie):

    header = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Host': 'router.asus.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36' }

    cookies = { 'asus_token' : login_cookie, 'clickedItem_tab': '0' }

    resp = requests.get(url, cookies=cookies, headers=header, allow_redirects=False)
    pdb.set_trace()


query_wireless_info(wireless_url, login_cookie="nxlAHI0M0exRp72sNdXehkYpN7WE8my")
    
