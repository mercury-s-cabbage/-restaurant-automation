from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
import xml.etree.ElementTree as ET

class response_xml(abstract_response):

    def build(self, data: list) -> str:
        text = super().build(data)

        root_tag = "Items"
        item_tag = "Item"

        # Корневой элемент
        root = ET.Element(root_tag)

        # Получаем поля из первого объекта
        if not data:
            return text  # Пустой список, возвращаем то, что сделал базовый build

        fields = common.get_fields(data[0])

        # Для каждого объекта создаём элемент с полями
        for obj in data:
            item_elem = ET.SubElement(root, item_tag)
            for field in fields:
                value = getattr(obj, field)
                child = ET.SubElement(item_elem, field)
                child.text = str(value)

        # Преобразуем дерево в строку XML с отступами
        def indent(elem, level=0):
            i = "\n" + level*"  "
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + "  "
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
                for child in elem:
                    indent(child, level+1)
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = i

        indent(root)

        xml_str = ET.tostring(root, encoding='unicode')

        # Добавляем результат базового build (если нужно)
        return text + xml_str
