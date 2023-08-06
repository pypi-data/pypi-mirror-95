
[![License](https://img.shields.io/badge/license-MIT-_red.svg)](https://opensource.org/licenses/MIT)
# chaos-python
This is Un-Official Python client to communicate with Chaos API

## Installation:- 

```bash
git clone git@github.com:arkwrn/chaos-python.git
cd chaos-python
```

## Usage:- 

This will display help for the tool. Here are all the switches it supports.

| Flag                     | Description                              |
| ------------------------ | ---------------------------------------- |
| --domain                 | Domain to find subdomains for            |
| --count                  | Show statistics for the specified domain |
| --key                    | Chaos key for API                        |
### Running chaos

In order to get subdomains for a domain, use the following command.

```bash
↳ python3 chaos-client.py --key MASKED_API_KEY --domain gojek.com  
mail.gojek.com
mailserver.gojek.com
gocorp.gojek.com
l.gojek.com
sms-demo.gojek.com
www.gojek.com
track.gojek.com
thmerchant.gojek.com
netbox-test.gojek.com
gocorp-integration.gojek.com
track-integration.gojek.com
www.newsroom.gojek.com
newsroom.gojek.com
```

To get the number of subdomains count, you can use the `count` flag.

```bash
↳ python3 chaos-client.py --key MASKED_API_KEY --domain gojek.com --count
13
```

### Use as python module:

```bash
pip3 install Chaos-Python-Client==1.0.0
```
### example:

```python
from chaos_python.client import chaosAPI as chaosapi

domain = "example.com"
key = "XXXXXXXXX"
options = "default"

print(chaosapi(domain, key, options))
```

Available options:
    - default   : output will be only subdomains
    - count     : output will be only count of subdomain
    - json      : output as JSON format
### How to avail `API_KEY`

As of now Chaos dataset is in beta for testing and API endpoint access available to invited users only, you can request an invite for yourself [here](https://forms.gle/GP5nTamxJPfiMaBn9)

💡 Notes
-----

- The API is rate-limited to 1 request at a time per token.
- Chaos API **only** supports domain name to query.
- All API is owned by : ProjectDiscovery, Inc.

📌 Reference
-----

- [Introducing Chaos Recon data API](https://blog.projectdiscovery.io/introducing-chaos-bug-bounty-recon-data-api)