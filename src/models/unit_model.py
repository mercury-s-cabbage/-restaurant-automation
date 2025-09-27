from src.core.validator import Validator
from src.core.abstract_model import AbstractModel


###############################################
# Модель единицы измерения
class UnitModel(AbstractModel):
    __base: "UnitModel" = None  # отложенная аннотация
    __coef: float = 1.0

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