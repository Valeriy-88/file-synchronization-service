import os


def name_file_in_cloud(data_folder: dict) -> list:
    """
    Функция создает список имен файлов из удаленного хранилища
    :param data_folder: Словарь данных из удаленного хранилища
    :return: список имен файлов в удаленном хранилище
    """
    if data_folder == {}:
        return []
    scroll_file_in_cloud: list = []
    for file in data_folder["_embedded"]["items"]:
        scroll_file_in_cloud.append({"name": file["name"]})
    return scroll_file_in_cloud


def check_delete_local_file(path_local_folder: str, files_in_cloud: list) -> list:
    """
    Функция создает список файлов на удаление с удаленного хранилища
    :param path_local_folder: Путь к папке в локальном компьютере
    :param files_in_cloud: список файлов из удаленного хранилища
    :return: список файлов на удаление из папки
    """
    files: list = os.listdir(path_local_folder)
    if files:
        scroll_delete_file: list = []
        for file in files_in_cloud:
            if file['name'] not in files:
                scroll_delete_file.append(file['name'])
        return scroll_delete_file
    else:
        return files_in_cloud


def check_new_local_file(path_local_folder: str, files_in_cloud: list) -> list:
    """
    Функция создает список файлов на создание в удаленном хранилище
    :param path_local_folder: Путь к папке в локальном компьютере
    :param files_in_cloud: список файлов из удаленного хранилища
    :return: список файлов на создание в удаленном хранилище
    """
    files: list = os.listdir(path_local_folder)
    scroll_new_file: list = []
    for file in files:
        data_file = {'name': file}
        if data_file not in files_in_cloud:
            scroll_new_file.append(file)
    return scroll_new_file

