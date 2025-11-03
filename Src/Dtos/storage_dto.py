from Src.Core.abstract_dto import abstact_dto

# Модель склада (dto)
# Пример
#                "address":"ул. Примерная, 10",
#                "id":"c1234567-89ab-cdef-0123-456789abcdef"
class storage_dto(abstact_dto):
    __address: str = ""

    """ 
    Адрес склада.
    Пример: "ул. Примерная, 10"
    """

    @property
    def address(self) -> str:
        # Возвращает адрес склада с удалением пробелов в начале и конце
        return self.__address.strip()

    @address.setter
    def address(self, value):
        # Устанавливает адрес склада, предварительно удаляя пробелы вокруг
        self.__address = value.strip()
