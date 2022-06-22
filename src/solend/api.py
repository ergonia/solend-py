import requests
from urllib.parse import urljoin


def solend_market_config(deployment="production",
                         solend_api="https://api.solend.fi"
                        ):
    response = requests.get(urljoin(solend_api, f"/v1/config?deployment={deployment}"))
    if response.status_code == 200:
        config = response.json()
        return config
    else:
        raise Exception(f"Solend API Status Code: {response.status_code} | {response.text}")