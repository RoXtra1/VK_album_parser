import math
import os
import requests
import vk_api
from configparser import ConfigParser


def create_config():
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
