import unittest
import json
from src.set_org_model import settings_manager
from src.company_model import company_model



class test_models(unittest.TestCase):

    # Провери создание основной модели
    # Данные после создания должны быть пустыми
    def test_empty_createmodel_companymodel(self):
        # Подготовка
        model = company_model()

        # Действие

        # Проверки
        assert model.name == ""



    # Проверить создание основной модели
    # Данные меняем. Данные должны быть
    def test_notEmpty_createmodel_companymodel(self):
        # Подготовка
        model = company_model()

        # Действие
        model.name = "test"
        model.prop = "OOO"
        model.inn = 123456789012
        model.bic = 123456789
        model.acc = 12345678901
        model.corr_acc = 12345678901

        # Проверки
        assert model.name != ""
        assert model.prop != ""
        assert model.inn == 123456789012
        assert model.inn == 123456789012
        assert model.bic == 123456789
        assert model.acc == 12345678901
        assert model.corr_acc == 12345678901

    # Проверить создание основной модели
    # Данные загружаем через json настройки
    def test_load_createmodel_companymodel(self):
        # Подготовка
        file_name = r"C:\Users\admin\PycharmProjects\restaurant_automation\settings.json"
        manager = settings_manager()
        manager.file_name = file_name

        # Дейсвтие
        result = manager.load()

        # Проверки
        assert result == True

    # Проверить создание основной модели
    # Данные загружаем. Проверяем работу Singletone
    def test_loadCombo_createmodel_companymodel(self):
        # Подготовка
        file_name = r"C:\Users\admin\PycharmProjects\restaurant_automation\settings.json"
        manager1 = settings_manager()
        manager1.file_name = file_name
        manager2 = settings_manager()

        # Дейсвтие
        manager1.load()

        # Проверки
        assert manager1.company == manager2.company

    def test_convert_function(self):
        # Подготовка
        d = {"company": {"name": "Рога и копыта"}}
        manager1 = settings_manager()

        # Дейсвтие
        manager1.convert(d)

        # Проверки
        assert manager1.company != ""



if __name__ == '__main__':
    unittest.main()
