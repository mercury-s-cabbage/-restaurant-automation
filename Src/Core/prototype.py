from Src.Core.validator import validator, argument_exception
from Src.Dtos.filter_dto import filter_dto
from Src.Core.common import common
import operator
from operator import attrgetter
from Src.reposity import reposity
class prototype:

    __data = []
    __repo = reposity()

    def __init__(self, data: list):
        self.data = data

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value: list):
        validator.validate(value, list)
        self.__data = value

    @property
    def repo(self):
        return self.__repo

    def clone(self, data: list = None) -> "prototype":
        inner_data = None
        if data is None:
            inner_data = self.data
        else:
            inner_data = data

        response = prototype(inner_data)
        return response


    def filter(self, filter_params: filter_dto):

        ops = {
            "==": operator.eq,
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le,
            "like": operator.contains
        }

        # не фильтруем пустые данные
        if len(self.data) == 0:
            return self.clone(self.data)

        validator.validate(filter_params, filter_dto)

        first_item = self.data[0]

        # проверка на корректность атрибута фильтрации
        if not hasattr(first_item, filter_params.filter_name):
            raise argument_exception("Некорректный атрибут для фильтрации")

        # проверка на корректность атрибута сортировки
        if filter_params.sort_name != "" and not hasattr(first_item, filter_params.sort_name):
            raise argument_exception("Некорректный атрибут для сортировки")

        result = []
        for field in common.get_fields(first_item):
            for item in self.data:
                # в каждом объекте из data достаем нужное поле
                if field == filter_params.filter_name:
                    value = getattr(item, field)

                    # устанавливаем, по какому атрибуту поля будем сравнивать
                    if filter_params.value_type == "id":
                        to_compare = value.unique_code
                    elif filter_params.value_type == "name":
                        to_compare = value.name
                    else:
                        to_compare = value

                    # сравниваем согласно виду сравнения
                    comp_func = ops.get(filter_params.filter_type)
                    if comp_func and comp_func(str(to_compare), filter_params.filter_value):
                        result.append(item)

        if filter_params.sort_name and filter_params.sort_name != "":
            sort_key = attrgetter(filter_params.sort_name)
            result = sorted(result, key=sort_key)

        return self.clone(result)

    def filter_many(self, model_name, filters: [], result):

        # ключ, по которому будут храниться прототипы (будет дописываться)
        repo_key = f"{model_name}"

        # сортируем фильтры по полю filter_name чтобы в ключах они были в одном порядке
        sorted_filters = sorted(filters, key=lambda f: f["filter_name"])

        # перебираем пришедшие фильтры
        for filter in sorted_filters:

            # создаем ДТО фильтра
            filter_obj = filter_dto()
            for key, value in filter.items():
                if hasattr(filter_obj, key):
                    setattr(filter_obj, key, str(value))

            # дополняем ключ прототипа согласно полю фильтрации
            repo_key += f"_{filter["filter_name"]}_{filter["filter_type"]}_{filter["filter_value"]}"  # например range_equal_kg

            # проверяем на наличие уже существующего прототипа
            if repo_key in self.repo.data:
                result = self.repo.data[repo_key]
            else:
                # сохраняем в репозиторий в случае, если там нету
                result = result.filter(filter_obj)
                self.repo.data.setdefault(repo_key, result)

            # если прототип пустой, нет смысла фильтровать дальше
            if result == []:
                break

        return result


