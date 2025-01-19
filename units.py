import logging
import time
from typing import Any

import requests
from check_update_file import check_file
from methods import check_delete_local_file, check_new_local_file, name_file_in_cloud
from requests.exceptions import ConnectionError, HTTPError, Timeout
from settings import (
    folder_cloud_storage,
    path_folder,
    secret_token,
    synchronization_period,
)


class SynchronizationFile:
    """
    Класс синхронизации файлов.
    Конструктор класса принимает на вход
    токен доступа к удаленному серверу
    путь к существующей папке
    для хранения резервных копий в удалённом хранилище
    """

    def __init__(self, token: str, path_cloud_storage: str):
        self.token = token
        self.path_folder_cloud_storage = path_cloud_storage

    def load_file(self, files: list) -> None:
        """
        Метод класса добавляет новые файлы
        из локального компьютера в удаленное хранилище
        :param files: список файлов
        :return: None
        """
        for file in files:
            try:
                response = requests.get(
                    f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={self.path_folder_cloud_storage}/{file}",
                    headers={"Authorization": self.token},
                )
                answer = response.json()
                requests.put(answer["href"], headers={"Authorization": self.token})
                logging.info(f"Файл {file} успешно записан.")
            except (HTTPError, Timeout, ConnectionError):
                logging.error(
                    f"Не удалось записать файл в хранилище. Ошибка соединения."
                )
            finally:
                return

    def reload_file(self, files: list) -> None:
        """
        Метод класса перезаписывает файлы
        облачного хранилища, файлами
        из локального компьютера
        :param files: список файлов
        :return: None
        """
        for file in files:
            try:
                self.delete_file([file])
                response = requests.get(
                    f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={self.path_folder_cloud_storage}/{file}",
                    headers={"Authorization": self.token},
                )
                answer = response.json()
                requests.put(answer["href"], headers={"Authorization": self.token})
                logging.info(f"Файл {file} успешно перезаписан.")
            except (HTTPError, Timeout, ConnectionError):
                logging.error(
                    f"Не удалось записать файл в хранилище. Ошибка соединения."
                )
            finally:
                return

    def delete_file(self, array_filename: list) -> None:
        """
        Метод класса удаляет файлы из облачного хранилища
        :param array_filename: список файлов
        :return: None
        """
        try:
            for filename in array_filename:
                response = requests.delete(
                    f"https://cloud-api.yandex.net/v1/disk/resources?path={self.path_folder_cloud_storage}/{filename}",
                    headers={"Authorization": self.token},
                )
                if response.status_code == 204:
                    logging.info(f"Файл {filename} успешно удален.")
                else:
                    logging.error(f"Файл {filename} не был удален. Ошибка сервера.")
        except (HTTPError, Timeout, ConnectionError):
            logging.error(f"Не удалось записать файл в хранилище. Ошибка соединения.")
        finally:
            return

    def get_info(self) -> Any:
        """
        Метод класса для получения информации
        о хранящихся в удалённом хранилище файлах.
        :return: Any
        """
        result = {}
        try:
            response = requests.get(
                f"https://cloud-api.yandex.net/v1/disk/resources?path={self.path_folder_cloud_storage}",
                headers={"Authorization": self.token},
            )
            result = response.json()
            print(result["_embedded"]["items"])
        except (HTTPError, Timeout, ConnectionError):
            logging.error(
                f"Не удалось получить информацию о файлах. Ошибка соединения."
            )
        finally:
            return result


def main():
    """
    Функция синхронизирует файлы на локальном компьютере
    с удаленным сервером яндекс диска
    """
    file = SynchronizationFile(secret_token, folder_cloud_storage)
    while True:
        logging.info(
            f"Программа синхронизации файлов начинает работу с директорией {path_folder}."
        )
        array_update_files: list = check_file()
        if array_update_files:
            file.reload_file(array_update_files)

        get_cloud_file = file.get_info()
        array_files_in_cloud: list = name_file_in_cloud(get_cloud_file)
        result: list = check_delete_local_file(path_folder, array_files_in_cloud)
        if result:
            file.delete_file(result)

        new_files: list = check_new_local_file(path_folder, array_files_in_cloud)
        if new_files:
            file.load_file(new_files)

        time.sleep(int(synchronization_period))
