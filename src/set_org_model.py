from src.company_model import company_model
import os
import json


####################################################3
# Менеджер настроек.
# Предназначен для управления настройками и хранения параметров приложения
class settings_manager:
    __file_name: str = ""
    __company: company_model = None

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.set_default()

    # Параметры организации из настроек
    @property
    def company(self) -> company_model:
        return self.__company

    @property
    def file_name(self) -> str:
        return self.__file_name

    # Полный путь к файлу настроек
    @file_name.setter
    def file_name(self, value: str):
        if value.strip() == "":
            return

        if os.path.exists(value):
            self.__file_name = value.strip()
        else:
            raise Exception("Не найден файл настроек!")

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__file_name.strip() == "":
            raise Exception("Не найден файл настроек!")

        try:
            with open(self.__file_name.strip(), 'r') as file_instance:
                data = json.load(file_instance)
                self.convert(data)
        except:
            return False
        return True

    # импорт из словаря
    def convert(self, data: dict):
        try:
            if "company" in data.keys():
                item = data["company"]
                self.__company.name = item["name"]
                self.__company.prop = item["prop"]
            if "bank_details" in data.keys():
                item = data["bank_details"]
                self.__company.acc = item["acc"]
                self.__company.corr_acc = item["corr_acc"]
                self.__company.bic = item["bic"]
                self.__company.inn = item["inn"]
            return True
        except:
            return False


    # Параметры настроек по умолчанию
    def set_default(self):
        self.__company = company_model()
        self.__company.name = "Рога и копыта"
        self.__company.inn = 100000000000
        self.__company.acc = 10000000000
        self.__company.corr_acc = 10000000000
        self.__company.bic = 100000000
        self.__company.prop = "AAAOO"


