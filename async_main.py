#!/usr/bin/env python3.12

# python3.12 -m venv venv --upgrade-deps
# source venv/bin/activate
# pip3.12 install --no-cache-dir --upgrade pip setuptools wheel
# pip3.12 install --no-cache-dir --upgrade aiohttp[speedups]

from datetime import datetime
app_start_time = datetime.now()
from pathlib import PurePath, Path
import inspect
import asyncio

app_path = PurePath(__file__)
app_name = app_path.name
app_dir = str(app_path.parent)

import config
zabbix_username = config.ZABBIX_USERNAME
zabbix_password = config.ZABBIX_PASSWORD
zabbix_api_url = config.ZABBIX_API_URL


async def main():

    zabbix_auth_payload_login = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": zabbix_username,
            "password": zabbix_password},
        "id": 1
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=zabbix_auth_payload_login, ssl=False) as resp:
            print(resp.status)
            print(json.dumps(await resp.json(), indent=4))
            zabbix_auth_token = await resp.json()["result"]
            print(json.dumps(zabbix_auth_token, indent=4, sort_keys=True))

        zabbix_payload = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "selectParentTemplates": [
                    "templateid",
                    "name"
                ],
                "selectTags": ["tag", "value"],
                "selectInheritedTags": ["tag", "value"]
            },
            "id": 2,
            "auth": zabbix_auth_token
        }

        async with session.post(url, json=zabbix_payload, ssl=False) as resp:
            print(resp.status)
            resp_json = await resp.json()
            print(json.dumps(await resp_json, indent=4))

            #print(json.dumps(resp_json, indent=4, sort_keys=True))

        zabbix_auth_payload_logout = {
            "jsonrpc": "2.0",
            "method": "user.logout",
            "params": {},
            "id": 999,
            "auth": zabbix_auth_token
        }
        async with session.post(url, json=zabbix_payload, ssl=False) as resp:
            print(resp.status)
            resp_json = await resp.json()
            print(json.dumps(await resp_json, indent=4))


if __name__ == "__main__":
    asyncio.run(main())


app_end_time = datetime.now()
app_delta_time = app_end_time - app_start_time
app_finished_in = f"\n--- Finished in {app_delta_time.days} days, {app_delta_time.seconds // 3600} hours, {app_delta_time.seconds // 60 % 60} mins, {app_delta_time.seconds % 60} secs"
print(app_finished_in)
