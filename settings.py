import configparser
import logging
import os
from typing import Any

name_file_config = "config.ini"


def create_config(file_config: str) -> None:
    """
    Функция для создания файла конфига с данными
    :param file_config: Имя файла ini
    :return: None
    """
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "secret_token", "Your secret token from yandex disk")
    config.set("Settings", "path_folder", "Your path to synchronization folder")
    config.set("Settings", "folder_cloud_storage", "Name folder cloud storage")
    config.set("Settings", "synchronization_period", "Period synchronization")
    config.set("Settings", "path_file_log", "Your path to file logging")

    with open(file_config, "w") as config_file:
        config.write(config_file)


def get_config(file_config: str) -> Any:
    """
    Функция возвращает объект конфига
    :param file_config: Имя файла ini
    :return: Any
    """
    if not os.path.exists(file_config):
        create_config(file_config)

    config = configparser.ConfigParser()
    config.read(file_config)
    return config


def get_setting(file_config: str, section: str, setting: str) -> Any:
    """
    Функция получает данные из файла ini
    :param file_config: Имя файла ini
    :param section: Имя секции в файле ini
    :param setting: Имя файла
    :return: Any
    """
    config = get_config(file_config)
    value = config.get(section, setting)
    return value


secret_token = get_setting(name_file_config, "Settings", "secret_token")
folder_cloud_storage = get_setting(name_file_config, "Settings", "folder_cloud_storage")
path_folder = get_setting(name_file_config, "Settings", "path_folder")
synchronization_period = get_setting(
    name_file_config, "Settings", "synchronization_period"
)
path_file_log = get_setting(name_file_config, "Settings", "path_file_log")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(path_file_log)
file_handler.setFormatter(
    logging.Formatter("%(module)s %(asctime)s %(levelname)s %(message)s")
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(module)s %(asctime)s %(levelname)s %(message)s")
)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
