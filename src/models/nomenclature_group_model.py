from src.core.validator import Validator
from src.core.abstract_model import AbstractModel


###############################################
# Модель группы номенклатур
class NomenclatureGroupModel(AbstractModel):
    __description: str = ""
    _cache = {}

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        Validator.validate(value, str, 255)
        self.__description = value

    @staticmethod
    def create(name: str):
        if name in NomenclatureGroupModel._cache:
            return NomenclatureGroupModel._cache[name]
        item = NomenclatureGroupModel(name)
        NomenclatureGroupModel._cache[name] = item
        return item