from src.models.settings_model import SettingsModel
from src.core.validator import ArgumentException
from src.core.validator import OperationException
from src.core.validator import Validator
from src.models.company_model import CompanyModel
import os
import json


####################################################3
# Менеджер настроек.
# Предназначен для управления настройками и хранения параметров приложения
class SettingsManager:

    # Наименование файла (полный путь)
    __full_file_name: str = ""

    # Настройки
    __settings: SettingsModel = None

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SettingsManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.set_default()

    # Текущие настройки
    @property
    def settings(self) -> SettingsModel:
        return self.__settings

    # Текущий каталог
    @property
    def file_name(self) -> str:
        return self.__full_file_name

    # Полный путь к файлу настроек
    @file_name.setter
    def file_name(self, value: str):
        Validator.validate(value, str)
        full_file_name = os.path.abspath(value)
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")

        try:
            with open(self.__full_file_name, 'r') as file_instance:
                settings = json.load(file_instance)

                if "company" in settings.keys():
                    data = settings["company"]
                    return self.convert(data)

            return False
        except:
            return False

    # Обработать полученный словарь
    def convert(self, data: dict) -> bool:
        validator.validate(data, dict)

        fields = list(filter(lambda x: not x.startswith("_"), dir(self.__settings.company)))
        matching_keys = list(filter(lambda key: key in fields, data.keys()))

        try:
            for key in matching_keys:
                setattr(self.__settings.company, key, data[key])
        except:
            return False

        return True

    # Параметры настроек по умолчанию
    def set_default(self):
        company = CompanyModel()
        company.name = "Рога и копыта"
        company.inn = -1

        self.__settings = SettingsModel()
        self.__settings.company = company





