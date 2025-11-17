from Src.Core.abstract_dto import abstact_dto
from enum import Enum

class FilterOperator(Enum):
    LIKE = "like"
    GREATER_THAN = ">="
    LESS_THAN = "<="
    EQUAL = "=="
# Фильтрация
class filter_dto(abstact_dto):
    __filter_name: str = ""  # атрибут, по которому производится фильтрация
    __filter_value: str = ""  # значение с которым сравниваем
    __value_type: str = ""  # поле атрибута, по которому будем сравнивать (id или name)
    __filter_type: FilterOperator = FilterOperator.EQUAL  # тип сравнения
    __sort_name: str = ""  # атрибут, по которому отсортируем результат

    @property
    def filter_name(self) -> str:
        return self.__filter_name

    @filter_name.setter
    def filter_name(self, value: str):
        self.__filter_name = value

    @property
    def filter_value(self) -> str:
        return self.__filter_value

    @filter_value.setter
    def filter_value(self, value: str):
        self.__filter_value = value

    @property
    def filter_type(self):
        return self.__filter_type

    @filter_type.setter
    def filter_type(self, value):
        self.__filter_type = value

    @property
    def value_type(self) -> str:
        return self.__value_type

    @value_type.setter
    def value_type(self, value: str):
        self.__value_type = value

    @property
    def sort_name(self) -> str:
        return self.__sort_name

    @sort_name.setter
    def sort_name(self, value: str):
        self.__sort_name = value
