from Src.Core.abstract_response import abstract_response
from Src.Core.common import common


"""
Класс для формирования данных в формате Csv
"""
class response_scv(abstract_response):

    # Сформировать CSV
    def build(self, data: list) -> str:
        text = super().build( data)

        # Шапка
        item = data [ 0 ]
        fields = common.get_fields( item )
        for field in fields:
            text += f"{field};"

        # Данные

        return text    

