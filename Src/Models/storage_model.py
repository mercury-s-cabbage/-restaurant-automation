from Src.Core.entity_model import entity_model
from Src.Core.validator import validator
from Src.Dtos.storage_dto import storage_dto


"""
Модель склада
"""
class storage_model(entity_model):
    __address:str = ""

    """
    Адрес
    """
    @property
    def address(self) -> str:
        return self.__address.strip()
    
    @address.setter
    def address(self, value:str):
        validator.validate(value, str)
        self.__address = value.strip()

    """
    Универсальный фабричный метод
    """

    def create(adress: str):
        validator.validate(adress, str)
        item = storage_model()
        item.address = adress
        return item

    """
    Фабричный метод из Dto
    """

    def from_dto(dto: storage_dto, cache: dict):
        validator.validate(dto, storage_dto)
        validator.validate(cache, dict)
        item = storage_model.create(dto.address)
        return item
