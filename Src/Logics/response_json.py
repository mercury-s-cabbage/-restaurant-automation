import json
from Src.Core.abstract_response import abstract_response
from Src.Core.common import common

def to_serializable(obj):
    # Простейшее преобразование для кастомных типов
    if hasattr(obj, '__dict__'):
        # Преобразуем объект в словарь с сериализуемыми значениями
        result = {}
        for key, value in obj.__dict__.items():
            result[key] = to_serializable(value)
        return result
    elif isinstance(obj, list):
        return [to_serializable(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    else:
        return obj  # предполагается, что это примитивный тип

class response_json(abstract_response):

    def build(self, data: list) -> str:
        if not data:
            return ""

        fields = common.get_fields(data[0])
        json_list = []
        for obj in data:
            obj_dict = {}
            for field in fields:
                value = getattr(obj, field)
                obj_dict[field] = to_serializable(value)
            json_list.append(obj_dict)

        json_text = json.dumps(json_list, ensure_ascii=False, indent=2)
        return json_text