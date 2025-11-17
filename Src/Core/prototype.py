from  Src.Models.nomenclature_model import nomenclature_model
from abc import ABC
from Src.Core.validator import validator, argument_exception
from Src.Dtos.filter_dto import filter_dto
from Src.Core.common import common
import operator
from operator import attrgetter

class prototype:

    __data = []

    def __init__(self, data: list):
        self.data = data

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value: list):
        validator.validate(value, list)
        self.__data = value

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
            ">=": operator.ge,
            "<=": operator.le,
            "like": operator.contains
        }

        # не фильтруем пустые данные
        if len(self.data) == 0:
            return self.data

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


