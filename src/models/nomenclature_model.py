from src.core.validator import Validator
from src.core.abstract_model import AbstractModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.unit_model import UnitModel

###############################################
# Модель номенклатуры
class NomenclatureModel(AbstractModel):
    __group: NomenclatureGroupModel = None
    __unit: UnitModel = None
    __fullname: str = ""
    _cache = {}

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    @property
    def group(self):
        return self.__group.name

    @group.setter
    def group(self, value):
        Validator.validate(value, NomenclatureGroupModel)
        self.group = value

    @property
    def unit(self):
        return self.__unit.name

    @unit.setter
    def unit(self, value):
        Validator.validate(value, UnitModel)
        self.__unit = value

    @property
    def fullname(self):
        return self.__fullname

    @fullname.setter
    def fullname(self, value):
        Validator.validate(value, str, 255)
        self.__fullname = value

    @staticmethod
    def create(name: str, unit: UnitModel = None):
        if name in NomenclatureModel._cache:
            return NomenclatureModel._cache[name]
        item = NomenclatureModel(name)
        item.unit = unit
        NomenclatureModel._cache[name] = item
        return item
