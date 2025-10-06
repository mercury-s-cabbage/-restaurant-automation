"""
Репозиторий данных
"""


class reposity:
    __data = {}

    @property
    def data(self):
        return self.__data

    """
    Ключ для единиц измерений
    """

    @staticmethod
    def range_key():
        return "range_model"

    @staticmethod
    def nomenclature_key():
        return "nomenclature_model"

    @staticmethod
    def group_key():
        return "group_model"

    @staticmethod
    def recipe_key():
        return "recipe_model"
