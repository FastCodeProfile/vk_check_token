import json
import asyncio
from contextlib import suppress

import aiohttp


class VK:
    """
    Класс для взаимодействия с ВК
    """

    def __init__(self, token: str) -> None:
        """
        Метод инициализации класса

        :param token: Токен аккаунта ВК
        """
        self.headers = {'Authorization': f'Bearer {token}'}

    async def set_online(self) -> tuple[bool, str | None]:
        """
        Метод для отправки статуса онлайн аккаунта ВК

        :return: tuple[bool, str | None]
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(f'https://api.vk.com/method/account.setOnline?v=5.131') as response:
                json_response = await response.json()
                if 'error' in json_response:
                    return False, json_response["error"]["error_msg"]
                else:
                    return True, None


def file_input() -> dict:
    """
    Функция читает и возвращает словарь с данными аккаунтов

    :return: dict
    """
    with open('./input.json', 'r') as file:
        return json.load(file)


def file_valid(valid_data: dict) -> None:
    """
    Функция записывает словарь с данными аккаунтов в файл

    :return: None
    """
    with open('./valid.json', 'w') as file:
        json.dump(valid_data, file)


def file_no_valid(no_valid_data: dict) -> None:
    """
    Функция записывает словарь с данными аккаунтов в файл

    :return: None
    """
    with open('./no_valid.json', 'w') as file:
        json.dump(no_valid_data, file)


async def main() -> None:
    """
    Главная функция запуска

    :return: None
    """
    valid_data = {}  # Валидные данные аккаунтов
    valid_key = 0  # Ключ для валидных данных аккаунта
    no_valid_data = {}  # Не валидные данные аккаунтов
    no_valid_key = 0  # Ключ для не валидных данных аккаунта
    input_data = file_input()  # Получаем словарь с данными аккаунтов
    for key in input_data.keys():  # Перебираем словарь по его ключам
        account = input_data[key]
        vk = VK(token=account['access_token'])  # Инициализируем класс
        status, response = await vk.set_online()  # Отправляем статус онлайн на аккаунт ВК
        if status:  # Если отправка статуса онлайн удалось
            print(f'Валид - {account["url_profile"]}')
            valid_data[str(valid_key)] = input_data[key]
            valid_key += 1
        else:  # Если отправка статуса онлайн не удалось
            print(f'Не валид - {account["url_profile"]}: {response} ')
            no_valid_data[str(no_valid_key)] = input_data[key]
            no_valid_key += 1

    file_valid(valid_data)  # Записываем валидные данные аккаунтов в файл
    file_no_valid(no_valid_data)  # Записываем не валидные данные аккаунтов в файл


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):  # Игнорирование ошибок при остановке
        asyncio.run(main())  # Запуск асинхронной функции из синхронного контекста
