from Src.Core.abstract_dto import abstact_dto
from typing import List

# Вспомогательный DTO для элемента состава рецепта
class recipe_composition_dto(abstact_dto):
    __nomenclature_id: str = ""
    __range_id: str = ""
    __value: float = 0.0

    @property
    def nomenclature_id(self) -> str:
        return self.__nomenclature_id

    @nomenclature_id.setter
    def nomenclature_id(self, value: str):
        self.__nomenclature_id = value

    @property
    def range_id(self) -> str:
        return self.__range_id

    @range_id.setter
    def range_id(self, value: str):
        self.__range_id = value

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, v: float):
        self.__value = v

# DTO рецепта
class recipe_dto(abstact_dto):
    __name: str = ""
    __cooking_time: str = ""
    __portions: int = 0
    __composition: List[recipe_composition_dto] = []

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def cooking_time(self) -> str:
        return self.__cooking_time

    @cooking_time.setter
    def cooking_time(self, value: str):
        self.__cooking_time = value

    @property
    def portions(self) -> int:
        return self.__portions

    @portions.setter
    def portions(self, value: int):
        self.__portions = value

    @property
    def composition(self) -> List[recipe_composition_dto]:
        return self.__composition

    @composition.setter
    def composition(self, value: List[recipe_composition_dto]):
        self.__composition = value