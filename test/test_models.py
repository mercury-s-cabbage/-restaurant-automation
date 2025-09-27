from src.settings_manager import SettingsManager
from src.models.company_model import CompanyModel
import unittest
from src.models.storage_model import StorageModel
import uuid


class TestModels(unittest.TestCase):

    # Проверим создание основной модели
    # Данные после создания должны быть пустыми
    def test_empty_createmodel_companymodel(self):
        # Подготовка
        model = CompanyModel()

        # Действие

        # Проверки
        assert model.name == ""

    # Проверить создание основной модели
    # Данные меняем. Данные должны быть
    def test_notEmpty_createmodel_companymodel(self):
        # Подготовка
        model = CompanyModel()

        # Действие
        model.name = "test"

        # Проверки
        assert model.name != ""

    # Проверить создание основной модели
    # Данные загружаем через json настройки
    def test_load_createmodel_companymodel(self):
        # Подготовка
        file_name = "settings.json"
        manager = SettingsManager()
        manager.file_name = file_name

        # Действие
        result = manager.load()

        # Проверки
        assert result == True

    # Проверить создание основной модели
    # Данные загружаем. Проверяем работу Singletone
    def test_loadCombo_createmodel_companymodel(self):
        # Подготовка
        file_name = "settings.json"
        manager1 = SettingsManager()
        manager1.file_name = file_name
        manager2 = SettingsManager()
        check_inn = -1 #по умолчанию, поскольку в файле inn1

        # Действие
        manager1.load()

        # Проверки
        assert manager1.settings == manager2.settings
        print(manager1.file_name)
        assert (manager1.settings.company.inn == check_inn)
        print("YES\n")
        print(f"ИНН {manager1.settings.company.inn}")

    # Проверка на сравнение двух по значению одинаковых моделей
    def text_equals_storage_model_create(self):
        # Подготовка
        id = uuid.uuid4().hex
        storage1 = StorageModel()
        storage1.id = id
        storage2 = StorageModel()
        storage2.id = id
        # Действие GUID

        # Проверки
        assert storage1 == storage2


if __name__ == '__main__':
    unittest.main()
