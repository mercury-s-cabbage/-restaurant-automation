from collections import defaultdict
from Src.reposity import reposity

from Src.Core.prototype import prototype
from Src.Dtos.filter_dto import filter_dto, FilterOperator

"""
Класс для отслеживания кэшированных прототипов
"""
class prototype_inspector:
    __data = {}

    @property
    def data(self):
        return self.__data

    """
    Ключ для данных о закрытом периоде
    """
    @staticmethod
    def past_data_key():
        return "past_data"

    """
    Ключ для кэшированных данных 
    """
    @staticmethod
    def current_data_key():
        return "current_data"


    """
    Распоряжается фильтрацией и кэшированием запросов 
    """
    def use_filter(self, start_p: prototype, f: dict, repo_key: str = ""):
        repo = self.data[self.current_data_key()]

        # проверяем на наличие уже существующего фильтра
        if repo_key in repo:
            filtered_p = repo[repo_key]
        else:
            # создадим фильтр склада
            f_obj = filter_dto()
            for key, value in f.items():
                if hasattr(f_obj, key):
                    setattr(f_obj, key, str(value))
            filtered_p = start_p.filter(f_obj)
            repo.setdefault(repo_key, filtered_p)

        return filtered_p


    """
    Считает и сохраняет в репозиторий остатки до даты блокировки
    """

    def count_blocking_cash(self, transactions: prototype, blocking_data) -> prototype:

        # Получим все существующие склады и номенклатуры
        storages = []
        nomenclatures = []
        for transaction in transactions.data:
            if not transaction.storage in storages:
                storages.append(transaction.storage.unique_code)
            if not transaction.nomenclature in nomenclatures:
                nomenclatures.append(transaction.nomenclature.unique_code)

        # отфильтруем по дате
        f_obj = filter_dto()
        f_obj.filter_name = "date"
        f_obj.filter_value = blocking_data
        f_obj.filter_type = "<="
        date_filtered = transactions.filter(f_obj)

        for s in storages:
            result = defaultdict(float)
            unit_map = {}

            f_obj.filter_name = "storage"
            f_obj.value_type = "id"
            f_obj.filter_value = str(s)
            f_obj.filter_type = "=="
            storage_filtered = date_filtered.filter(f_obj)

            for n in nomenclatures:
                f_obj.filter_name = "nomenclature"
                f_obj.value_type = "id"
                f_obj.filter_value = str(n)
                f_obj.filter_type = "=="
                filtered = storage_filtered.filter(f_obj)

                # Пройдём по всем транзакциям для расчёта начального остатка
                for t in filtered.data:
                    real_range = t.unit.base.unique_code if getattr(t.unit, 'base', None) else t.unit.unique_code
                    key = (t.nomenclature.unique_code,
                           real_range)  # храним номенклатуру и валюту на случай, если будут штуки и кг напр
                    qty = t.quantity * t.unit.value  # приводим к одной валюте
                    result[key] += qty
                    if key not in unit_map:
                        unit_map[key] = t.unit.name

            self.data[ self.past_data_key() ].setdefault(f"{blocking_data}_{s}", result)

        # получим только текущие транзакции
        f_obj = filter_dto()
        f_obj.filter_name = "date"
        f_obj.filter_value = blocking_data
        f_obj.filter_type = ">"
        result = transactions.filter(f_obj)

        return result

    """
    Получить список всех ключей
    Источник: https://github.com/Alyona1619
    """
    @staticmethod
    def keys() -> list:
        result = []
        methods = [method for method in dir(prototype_inspector) if
                    callable(getattr(prototype_inspector, method)) and method.endswith('_key')]
        for method in methods:
            key = getattr(prototype_inspector, method)()
            result.append(key)

        return result

    """
    Инициализация
    """
    def initalize(self):
        keys = prototype_inspector.keys()
        for key in keys:
            self.__data[ key ] = {}

