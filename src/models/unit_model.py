from src.core.validator import Validator
from src.core.abstract_model import AbstractModel


###############################################
# Модель единицы измерения
class UnitModel(AbstractModel):
    __base: "UnitModel" = None  # отложенная аннотация
    __coef: float = 1.0
    _cache = {}

    def __init__(self, name: str, coef: float = 1.0, base=None):
        super().__init__()
        self.name = name
        self.coef = coef
        if base:
            self.base = base

    @property
    def base(self) -> str:
        return self.__base

    @base.setter
    def base(self, value: "UnitModel"):
        Validator.validate(value, UnitModel)
        self.__base = value

    @property
    def coef(self) -> float:
        return self.__coef

    @coef.setter
    def coef(self, value: float):
        Validator.validate(value, (float, int))
        self.__coef = value

    @staticmethod
    def create(name: str, base=None):
        if name in UnitModel._cache:
            return UnitModel._cache[name]

        item = UnitModel(name)
        if base is not None:
            Validator.validate(base, UnitModel)
            item.base = base
        UnitModel._cache[name] = item
        return item
    """
    Киллограмм
    """

    @staticmethod
    def create_kill():
        inner_gram = UnitModel.create_gram()
        return UnitModel.create("киллограмм", inner_gram)

    """
    Грамм
    """

    @staticmethod
    def create_gram():
        return UnitModel.create("грамм")

    """
    Литр
    """

    @staticmethod
    def create_liter():
        return UnitModel.create("литр")


