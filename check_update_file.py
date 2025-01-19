import configparser
import hashlib
import os
from configparser import DuplicateSectionError
from typing import Any


def create_config(file_ini: str, new_file: str, md5: str) -> None:
    """
    Функция для создания файла конфига с данными
    :param file_ini: Имя файла ini
    :param new_file: Имя файла
    :param md5: Хэш файла
    :return: None
    """
    config = configparser.ConfigParser()
    config.read(file_ini)
    try:
        config.add_section("Settings")
    except DuplicateSectionError:
        pass
    config.set("Settings", new_file, md5)
    with open(file_ini, "w") as config_file:
        config.write(config_file)


def get_config(file_ini: str) -> Any:
    """
    Функция возвращает объект конфига
    :param file_ini: Имя файла ini
    :return: Any
    """
    if not os.path.exists(file_ini):
        create_config(file_ini, "f.txt", "5")

    config = configparser.ConfigParser()
    config.read(file_ini)
    return config


def update_setting(file_ini: str, section: str, setting: str, value: str) -> None:
    """
    Функция обновляет данные в файле ini
    после изменений данных на компьютере
    :param file_ini: Имя файла ini
    :param section: Имя секции в файле ini
    :param setting: Имя файла
    :param value: Значение для имени файла
    :return: None
    """
    config = get_config(file_ini)
    config.set(section, setting, value)
    with open(file_ini, "w") as config_file:
        config.write(config_file)


def delete_setting(file_ini: str, setting: str) -> None:
    """
    Функция удаляет данные из файла ini
    :param file_ini: Имя файла ini
    :param setting: Имя файла
    :return: None
    """
    config = get_config(file_ini)
    config.remove_option("Settings", setting)
    with open(file_ini, "w") as config_file:
        config.write(config_file)


def check_delete_file(name_file_ini: str, local_files: list) -> dict:
    """
    Функция собирает в словарь данные из файла name_file_ini.
    Проверяет какие файлы были удалены из папки
    и отправляет удалить эти файлы из файла ini
    :param name_file_ini: файл ini
    :param local_files: Список локальных файлов в папке
    :return: dict
    """
    data_file_ini: dict = {}
    with open(name_file_ini) as file:
        for index, line in enumerate(file):
            line = line.replace("\n", "")
            if index == 0 or line == "":
                continue
            (key, val) = line.split(" = ")
            data_file_ini[key] = val

    for file in data_file_ini:
        if file not in local_files:
            delete_setting(name_file_ini, file)

    return data_file_ini


def check_file() -> list:
    """
    Функция проверяет файлы на локальном компьютере.
    Какие были изменены/удалены/добавлены.
    И возвращает список файлов которые надо
    обновить на удаленном хранилище
    :return: List
    """
    name_file_ini: str = "list_file.ini"
    files: list = os.listdir("C:/Users/Admin/PycharmProjects/folder")

    content_file_ini: dict = check_delete_file(name_file_ini, files)
    scroll_update_file: list = []
    for file in files:
        with open(f"C:/Users/Admin/PycharmProjects/folder/{file}", "rb") as file_obj:
            file_contents = file_obj.read()
            md5_hash = hashlib.md5(file_contents).hexdigest()

        if file not in content_file_ini:
            create_config(name_file_ini, file, md5_hash)
            content_file_ini: dict = check_delete_file(name_file_ini, files)

        if md5_hash != content_file_ini[file]:
            update_setting(name_file_ini, "Settings", file, md5_hash)
            scroll_update_file.append(file)

    return scroll_update_file
