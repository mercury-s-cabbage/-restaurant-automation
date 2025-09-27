"""
Исключение при проверки аргумента
"""


class ArgumentException(Exception):
    pass


"""
Исключение при выполнении бизнес операции
"""


class OperationException(Exception):
    pass


"""
Набор проверок данных
"""


class Validator:

    @staticmethod
    def validate(value, type_, len_=None):
        """
            Валидация аргумента по типу и длине
        Args:
            value (any): Аргумент
            type_ (object): Ожидаемый тип
            len_ (int): Максимальная длина
        Raises:
            arguent_exception: Некорректный тип
            arguent_exception: Неулевая длина
            arguent_exception: Некорректная длина аргумента
        Returns:
            True или Exception
        """

        if value is None:
            raise ArgumentException("Пустой аргумент")

        # Проверка типа
        if not isinstance(value, type_):
            raise ArgumentException(f"Некорректный тип!\nОжидается {type_}. Текущий тип {type(value)}")

        # Проверка аргумента
        if len(str(value).strip()) == 0:
            raise ArgumentException("Пустой аргумент")

        if len_ is not None and len(str(value).strip()) > len_:
            raise ArgumentException("Некорректная длина аргумента")

        return True