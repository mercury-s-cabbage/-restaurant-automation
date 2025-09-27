from src.core.validator import validator
from src.core.abstract_model import abstact_model

class StorageModel(abstact_model):
    __name:str = ""

    # Наименование
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value:str):
        validator.validate(value, str)
        self.__name = value.strip()
