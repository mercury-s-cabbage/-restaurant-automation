from Src.Core.abstract_dto import abstact_dto

# Модель транзакции (dto)
# Пример
#                "date":"2025-10-31T12:00:00",
#                "nomenclature_id":"0c101a7e-5934-4155-83a6-d2c388fcc11a",
#                "storage_id":"a33dd457-36a8-4de6-b5f1-40afa6193346",
#                "quantity":10.5,
#                "unit_id":"7f4ecdab-0f01-4216-8b72-4c91d22b8918",
#                "id":"123e4567-e89b-12d3-a456-426614174000"

class transaction_dto(abstact_dto):
    __date: str = ""
    __nomenclature_id: str = ""
    __storage_id: str = ""
    __quantity: float = 0.0
    __unit_id: str = ""

    @property
    def date(self) -> str:
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    @property
    def nomenclature_id(self) -> str:
        return self.__nomenclature_id

    @nomenclature_id.setter
    def nomenclature_id(self, value):
        self.__nomenclature_id = value

    @property
    def storage_id(self) -> str:
        return self.__storage_id

    @storage_id.setter
    def storage_id(self, value):
        self.__storage_id = value

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        self.__quantity = value

    @property
    def unit_id(self) -> str:
        return self.__unit_id

    @unit_id.setter
    def unit_id(self, value):
        self.__unit_id = value
