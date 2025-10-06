from src.settings_manager import SettingsManager
from src.models.company_model import CompanyModel
import unittest
from src.models.storage_model import StorageModel
import uuid
from src.models.unit_model import UnitModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.nomenclature_group_model import NomenclatureGroupModel


class TestModels(unittest.TestCase):

    ###############################################
    # CompanyModel
    # Пустая модель
    def test_EmptyCreate_CompanyModel(self):
        # Подготовка
        model = CompanyModel()

        # Действие

        # Проверки
        assert model.name == ""

    # Заполненные данные
    def test_NotEmptyCreate_CompanyModel(self):
        # Подготовка
        model = CompanyModel()

        # Действие
        model.name = "test"

        # Проверки
        assert model.name != ""

    # Данные из json
    def test_LoadCreate_CompanyModel(self):
        # Подготовка
        file_name = "settings.json"
        manager = SettingsManager()
        manager.file_name = file_name

        # Действие
        result = manager.load()

        # Проверки
        assert result == True

    # Работа SingleTone
    def test_TestSingleTone_CompanyModel(self):
        # Подготовка
        file_name = "settings.json"
        manager1 = SettingsManager()
        manager1.file_name = file_name
        manager2 = SettingsManager()
        check_inn = -1

        # Действие
        manager1.load()

        # Проверки
        assert manager1.settings == manager2.settings
        assert (manager1.settings.company.inn == check_inn)

    ###############################################
    # StorageModel
    # Сравнение по id
    def test_EqualsStorage_StorageModel(self):
        # Подготовка
        id = uuid.uuid4().hex
        storage1 = StorageModel()
        storage1.unique_code = id
        storage2 = StorageModel()
        storage2.unique_code = id

        # Действие GUID

        # Проверки
        assert storage1 == storage2

    ###############################################
    # UnitModel
    # Пустая модель
    def test_EmptyCreate_UnitModel(self):
        # Подготовка
        unit = UnitModel("г")

        # Действие GUID

        # Проверки
        assert unit.coef == 1

    # Заполненные данные
    def test_NotEmptyCreate_UnitModel(self):
        # Подготовка
        base_unit = UnitModel("г")
        another_unit = UnitModel("кг", 1000, base_unit)

        # Действие GUID

        # Проверки
        assert another_unit.base == base_unit

    ###############################################
    # NomenclatureModel
    # Пустые данные
    def test_EmptyCreate_NomenclatureModel(self):
        # Подготовка
        nom = NomenclatureModel()

        # Действие GUID

        # Проверки
        assert nom != None

    # Заполненные данные
    def test_NotEmptyCreate_NomenclatureModel(self):
        # Подготовка
        nom = NomenclatureModel()
        unit = UnitModel("g")

        # Действие GUID
        nom.unit = unit

        # Проверки
        assert nom.unit == "g"

    ###############################################
    # NomenclatureGroupModel
    # Пустые данные

    def test_EmptyCreate_NomenclatureGroupModel(self):
        # Подготовка
        nom = NomenclatureGroupModel()

        # Действие GUID

        # Проверки
        assert nom != None

    # Заполненные данные
    def test_NotEmptyCreate_NomenclatureGroupModel(self):
        # Подготовка
        nom = NomenclatureGroupModel()

        # Действие GUID
        nom.description = "test"

        # Проверки
        assert nom.description == "test"


if __name__ == '__main__':
    unittest.main()
