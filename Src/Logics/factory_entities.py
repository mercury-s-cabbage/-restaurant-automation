from Src.Core.abstract_response import abstract_response
from Src.Logics.response_csv import response_scv
from Src.Core.validator import operation_exception

"""
Фабрика для формирования различных ответов
"""
class factory_entities:

    # Сопоставление
    __match = {
        "csv":  response_scv
    }

    # Получить нужный тип
    def create(self, format:str) -> abstract_response:
        if format not in self.__match.keys():
            raise operation_exception("Формат не верный")
        
        return self.__match[  format ]

