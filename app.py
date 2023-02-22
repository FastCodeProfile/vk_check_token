import json
import asyncio
from contextlib import suppress

import aiohttp
from loguru import logger


class VkApi:
    def __init__(self, access_token: str) -> None:
        self.host = 'https://api.vk.com/method/'
        self.params = {'v': 5.131}
        self.headers = {'Authorization': f"Bearer {access_token}"}

    async def check_token(self) -> bool:
        method = 'account.setOnline'
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(self.host + method, params=self.params) as response:
                json_response = await response.json()
                return 'error' not in json_response


def load_data(filename: str) -> dict:
    with open(filename, encoding='utf-8') as file:
        return json.load(file)


def dump_data(filename: str, valid_data: dict) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(valid_data, file, indent=2)


async def main() -> None:
    valid_data, valid_key = {}, 0
    no_valid_data, no_valid_key = {}, 0
    data = load_data('data.json')
    for key, user in data.items():
        vk_api = VkApi(user['access_token'])
        result = await vk_api.check_token()
        if result:
            logger.success(f'Валид - {user["url_profile"]}')
            valid_data[str(valid_key)] = user
            valid_key += 1
        else:
            logger.warning(f'Не валид - {user["url_profile"]}')
            no_valid_data[str(no_valid_key)] = user
            no_valid_key += 1

    dump_data('valid.json', valid_data)
    dump_data('no_valid.json', no_valid_data)


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
