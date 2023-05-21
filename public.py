import requests
import time
import alert


def get_ip():
    api_dict = {
        'https://ident.me/': None,
        'https://api.seeip.org/jsonip': 'ip',
        'https://api.bigdatacloud.net/data/client-ip': 'ipString'
    }

    for api, ip_key in api_dict.items():
        response = requests.get(api)
        if response.status_code == 200:
            if ip_key is None:
                public_ip = response.text
            else:
                public_ip = response.json()[ip_key]
    
    i = 0
    while(public_ip is None):
        time.sleep(300)
        if i == 288:
            api_list = list(api_dict.keys())
            notif = alert.Email()
            notif.bad_api(api=api_list)
            break
    
    return public_ip