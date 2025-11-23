import unittest
from Src.Core.common import common
from Src.start_service import start_service
from Src.Core.prototype import prototype
from Src.reposity import reposity
from Src.Core.validator import operation_exception
from Src.Dtos.filter_dto import filter_dto

class test_prototype(unittest.TestCase):

    def test_prototype(self):
        service = start_service()
        service.start()

        start_prototype = prototype(service.repository.data[reposity.transactions_key()])

        # Проверки
        assert len(start_prototype.data) > 0

    def test_empty_prototype(self):
        start_prototype = prototype([])

        # Проверки
        assert len(start_prototype.data) == 0

    def test_filtered_prototype(self):
        service = start_service()
        service.start()

        all_transactions = service.repository.data.get(service.repository.transactions_key(), [])
        all_transactions_p = prototype(all_transactions)
        filters_list = []

        response = {
                      "filters": [
                      {
                          "filter_name": "nomenclature",
                          "filter_value": "0c101a7e-5934-4155-83a6-d2c388fcc11a",
                          "filter_type": "==",
                          "value_type": "id",
                          "sort_name": "nomenclature"
                      },
                        {
                          "filter_name": "storage",
                          "filter_value": "warehouse-002",
                          "value_type": "id",
                          "filter_type": "==",
                          "sort_name": ""
                        }
                      ]
                    }

        for filter_data in response["filters"]:
            filter_obj = filter_dto()
            for key, value in filter_data.items():
                if hasattr(filter_obj, key):
                    setattr(filter_obj, key, str(value))
            filters_list.append(filter_obj)


        new_prototype1 = all_transactions_p.filter(filters_list[0])
        new_prototype2 = new_prototype1.filter(filters_list[1])


        # Проверки
        assert len(new_prototype1.data) != 0
        assert len(all_transactions_p.data) > len(new_prototype2.data)



if __name__ == '__main__':
    unittest.main()

