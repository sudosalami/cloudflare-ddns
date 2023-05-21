# cloudflare-ddns

## Description

cloudflare-ddns allows you to automate the management of your DNS records on CloudFlare. By running the `main.py` script in a container or virtual machine, you can keep your DNS records up to date with your current public IP address. As an added bonus you can use email alerts to keep tabs on your network.

## Prerequisites

Before running the script, ensure you have the following:

- CloudFlare API Key: Generate an API key with the necessary permissions (Zone.DNS) by visiting [CloudFlare API Tokens](https://dash.cloudflare.com/profile/api-tokens).
- Zone ID: Obtain the Zone ID by navigating to the dashboard for the zone where you want to enable DDNS.
- CloudFlare Account Email: Provide the email associated with your CloudFlare account.
- Domain name: example.com (Used for code logic, not for configuring the records themselves)

## Installation and Setup

1. Clone this repository or download the code.
2. Install [requests](https://pypi.org/project/requests/). `pip install requests`
3. Set the environment variables in auth.py
4. Run the `main.py` script in a container or virtual machine.

## Custom Records

By default, the script creates a dynamic record for the root domain with the proxy off. However, if you want to automate additional records or choose a different DNS record as your DDNS, you can customize the `main.py` file.

The `DNSRecord` object has the following editable attributes:

- `name:str` Describes the prefix for your DNS record (default: @).
- `content:str` Specifies the value you want to assign to the prefix (default: Your IP Address).
- `proxied:bool` Determines whether the DNS record should be proxied by CloudFlare. (default: False)
  - If unsure, it's recommended to leave this as the default to avoid potential issues with your applications.
- `type:str` Sets the record type (default: A).
- `comment:str` Provides an optional comment to identify automatically managed records. (default: Dynamic DNS)
- `ttl:int` Sets the TTL (Time To Live) for the DNS record in seconds. (default: 1)
  - Valid values range from 60 to 86400, or you can set it to 1 for automatic TTL.
  - If proxied=True, CloudFlare overwrites this to automatic

## Email Alerts

Email alerts are not required, but can be helpful to keep track of your network.

I created some custom alerts, but you can make your own using the `Email.send_email` method. Below is a list of editable attributes:

- `subject:str`
- `body:str`

## Usage Examples

Here are a few usage examples to help you get started:

```bash
# Run the main.py script
python main.py
```

```py
# Customize the DNS record name and ttl
# in main.py
custom_record = cloudflare.DNSRecord()
custom_record.name="subdomain"
custom_record.ttl=60
custom_record.validate_record()
```

```py
# When event happens, trigger custom email
import alert
notif = alert.Email()
notif.send_email(subject='Email Subject', body='Email body')

# in auth.py
EMAIL_USER = 'name@gmail.com'
EMAIL_PASSWORD = 'app password'
EMAIL_SERVER = 'smtp.gmail.com'
EMAIL_PORT = '465'
```

## Troubleshooting

If you encounter any issues or errors, please refer to the following troubleshooting steps:

1. Make sure you have provided the correct API key, Zone ID, and email information.
2. Check your internet connection and ensure one of the public IP APIs are available (public.py).
3. Review the CloudFlare API documentation
4. Review your email provider documentation (ex: [Gmail](https://support.google.com/mail/answer/7126229?hl=en))