import unittest
from datetime import datetime
from Src.Models.transaction_model import transaction_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Models.range_model import range_model
from Src.Core.validator import argument_exception

import unittest
from datetime import datetime
from Src.Models.transaction_model import transaction_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Models.range_model import range_model
from Src.Core.entity_model import entity_model

class dummy_group_model(entity_model):
    pass

class TestTransactionModel(unittest.TestCase):

    def setUp(self):
        self.group = dummy_group_model()
        self.gram = range_model.create("грамм", 1, None)
        self.nomenclature = nomenclature_model.create("Test Nomenclature", self.group, self.gram)
        self.storage = storage_model()
        self.storage.address = "Warehouse 1"
        self.unit = self.gram

    def test_date_set_get(self):
        t = transaction_model()
        now = datetime.now()
        t.date = now
        self.assertEqual(t.date, now)

        with self.assertRaises(argument_exception):
            t.date = "invalid date"

    def test_nomenclature_set_get(self):
        t = transaction_model()
        t.nomenclature = self.nomenclature
        self.assertEqual(t.nomenclature, self.nomenclature)

        with self.assertRaises(argument_exception):
            t.nomenclature = "not a nomenclature"

    def test_storage_set_get(self):
        t = transaction_model()
        t.storage = self.storage
        self.assertEqual(t.storage, self.storage)

        with self.assertRaises(argument_exception):
            t.storage = 12345

    def test_quantity_set_get(self):
        t = transaction_model()
        t.quantity = 10.5
        self.assertEqual(t.quantity, 10.5)

        with self.assertRaises(argument_exception):
            t.quantity = "ten"

        # with self.assertRaises(argument_exception):
        #     t.quantity = -5

    def test_unit_set_get(self):
        t = transaction_model()
        t.unit = self.unit
        self.assertEqual(t.unit, self.unit)

        with self.assertRaises(argument_exception):
            t.unit = "invalid unit"

if __name__ == '__main__':
    unittest.main()
