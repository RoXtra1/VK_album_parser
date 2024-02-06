import math
import os
import requests
import vk_api
from configparser import ConfigParser


def create_config():
    """ Создание и чтение файла конфигурации """
    cfg = ConfigParser()
    config_file = "Configuration.ini"
    if not os.path.exists(config_file):
        cfg.add_section("Configuration")
        cfg.set("Configuration", "Token", "token")  # публичный токен-ключ для авторизации
        cfg.set("Configuration", "Root", "root")  # адрес корневой папки, куда требуется скачивать
        with open(config_file, "w") as config_file:
            cfg.write(config_file)
    cfg.read("Configuration.ini", encoding='utf-8')
    return cfg


def authorization():
    """ Авторизация в вк через токен """
    try:
        vk_session = vk_api.VkApi(token=TOKEN)
        print('Авторизован!')
        return vk_session.get_api()
    except vk_api.AuthError as error_msg:
        print(error_msg)
    return None