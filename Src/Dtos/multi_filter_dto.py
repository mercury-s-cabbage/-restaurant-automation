from typing import List, Union
from Src.Core.abstract_dto import abstact_dto
from Src.Dtos.filter_dto import filter_dto

class multi_filter_dto(abstact_dto):
    __filters: List[Union[filter_dto]]  # список с DTO

    @property
    def filters(self) -> list[filter_dto]:
        return self.__filters

    @filters.setter
    def filters(self, value):
        self.filters = value
