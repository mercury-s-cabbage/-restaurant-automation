from src.core.validator import Validator
from src.core.abstract_model import AbstractModel


###############################################
# Модель группы номенклатур
class NomenclatureGroupModel(AbstractModel):
    __description: str = ""

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        Validator.validate(value, str, 255)
        self.__description = value