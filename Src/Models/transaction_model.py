from datetime import datetime
from Src.Core.abstract_model import abstact_model
from Src.Core.validator import validator
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Models.range_model import range_model
from Src.Core.validator import argument_exception
from Src.Dtos.transaction_dto import transaction_dto

class transaction_model(abstact_model):
    __date: datetime = None
    __nomenclature: nomenclature_model = None
    __storage: storage_model = None
    __quantity: float = 0.0
    __unit: range_model = None

    # Дата
    @property
    def date(self) -> datetime:
        return self.__date

    @date.setter
    def date(self, value):
        validator.validate(value, datetime)
        self.__date = value

    # Номенклатура
    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    # Склад
    @property
    def storage(self) -> storage_model:
        return self.__storage

    @storage.setter
    def storage(self, value: storage_model):
        validator.validate(value, storage_model)
        self.__storage = value

    # Количество
    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        validator.validate(value, (int, float))
        if value <= 0:
            raise argument_exception("Количество должно быть положительным числом")
        self.__quantity = float(value)

    # Единица измерения
    @property
    def unit(self) -> range_model:
        return self.__unit

    @unit.setter
    def unit(self, value: range_model):
        validator.validate(value, range_model)
        self.__unit = value

    """
    Универсальный фабричный метод
    """

    @staticmethod
    def create(date: datetime, nomenclature: nomenclature_model, storage: storage_model,
               quantity: float, unit: range_model):

        validator.validate(date, datetime)
        validator.validate(nomenclature, nomenclature_model)
        validator.validate(storage, storage_model)
        validator.validate(quantity, (int, float))

        validator.validate(unit, range_model)

        item = transaction_model()
        item.date = date
        item.nomenclature = nomenclature
        item.storage = storage
        item.quantity = quantity
        item.unit = unit
        return item

    """
    Фабричный метод из DTO
    """

    @staticmethod
    def from_dto(dto: transaction_dto, cache: dict):
        validator.validate(dto, transaction_dto)
        validator.validate(cache, dict)
        print(cache)

        # Получаем связанные объекты из кэша по id, если есть
        nomenclature = cache[str(dto.nomenclature_id).strip()] if str(dto.nomenclature_id).strip() in cache else None
        storage = cache[dto.storage_id] if dto.storage_id in cache else None
        unit = cache[dto.unit_id] if dto.unit_id in cache else None
        date_string = dto.date  # строка с датой, например "2025-11-03"

        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")

        item = transaction_model.create(date_object, nomenclature, storage, dto.quantity, unit)
        return item