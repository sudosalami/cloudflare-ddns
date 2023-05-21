from auth import ZONE_ID, DOMAIN, API_EMAIL, API_KEY
import requests
import json
import public
import alert

class DNSRecord:
    base_url = 'https://api.cloudflare.com/client/v4/zones/'

    headers = {
        "Content-Type": "application/json",
        "X-Auth-Email": API_EMAIL,
        "Authorization": f"Bearer {API_KEY}",
    }

    def __init__(self):
        self.type = "A"
        self.name = '@'
        self.content = public.get_ip()
        self.proxied = False
        self.comment = "Dynamic DNS"
        self.ttl = 1
    
    def validate_record(self):
        url = f"{DNSRecord.base_url}{ZONE_ID}/dns_records"
        record_request = requests.get(url, headers=DNSRecord.headers)
        record_list = record_request.json()['result']
        
        if self.name == '@':
            desired_name = DOMAIN
        else:
            desired_name = F"{self.name}.{DOMAIN}"
        
        desired_type = self.type
        desired_content = self.content
        desired_proxy = self.proxied


        matching_record = False
        for record in record_list:
            # If record exists
            if record['name'] ==  desired_name and record['type'] == desired_type:
                matching_record = True
                # AND if record is stale
                if record['content'] != desired_content:
                    matching_record = True
                    DNSRecord.update_record(self, record['id'])
                    notif = alert.Email()
                    notif.new_info(old=(record['content']), new=desired_content)
                    break
                elif record['proxied'] != desired_proxy:
                    matching_record = True
                    DNSRecord.update_record(self, record['id'])
                    break
        # If record does not exist
        if not matching_record:
            DNSRecord.create_record(self)
            pass


    def update_record(self, RECORD_ID):
        url = f"{DNSRecord.base_url}{ZONE_ID}/dns_records/{RECORD_ID}"
        data = {
            "type": self.type,
            "name": self.name,
            "content": self.content,
            "proxied": self.proxied,
            "comment": self.comment,
            "ttl": self.ttl
        }

        requests.put(url, headers=DNSRecord.headers, data=json.dumps(data))


    def create_record(self):
        url = f"{DNSRecord.base_url}{ZONE_ID}/dns_records"
        data = {
            "type": self.type,
            "name": self.name,
            "content": self.content,
            "proxied": self.proxied,
            "comment": self.comment,
            "ttl": self.ttl
        }
        
        requests.post(url, headers=DNSRecord.headers, data=json.dumps(data))