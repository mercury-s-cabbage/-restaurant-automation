import os

from Src.reposity import reposity
from Src.start_service import start_service
import unittest

# Набор тестов для проверки работы статового сервиса
class test_start(unittest.TestCase):

    # Проверить создание start_service и заполнение данными
    def test_notThow_start_service_load(self):
        # Подготовка
        start = start_service()

        # Действие
        start.start()

        # Проверка
        assert len(start.data[ reposity.range_key()]) > 0

    # Проверить уникальность элементов
    def test_checkUnique_start_service_load(self):
        # Подготовка
        start = start_service()

        # Действие
        start.start()

        # Проверка
        gramm =  list(filter(lambda x: x.name == "Грамм", start.data[ reposity.range_key()])) 
        kg =  list(filter(lambda x: x.name == "Киллограмм", start.data[ reposity.range_key()])) 
        assert gramm[0].unique_code == kg[0].base.unique_code


    # Проверить метод keys класса reposity
    def test_any_reposity_keys(self):
        # Подготовка

        # Действие
        result = reposity.keys()
        
        # Проверка
        assert len(result) > 0

    # Проверить метод initalize класса reposity 
    def test_notThrow_reposity_initialize(self):   
        # Подготовка
        repo = reposity()

        # Действие
        repo.initalize()

    # Проверить создание непустого файла сохранений
    def test_save_creates_nonempty_file(self):
        start = start_service()
        start.start()  # загрузить данные перед сохранением

        filename = "test_save_output.json"
        try:
            result = start.save(filename)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(filename))
            self.assertTrue(os.path.getsize(filename) > 0)
        finally:
            # Удаляем файл после проверки, чтобы не засорять систему
            if os.path.exists(filename):
                os.remove(filename)


          
if __name__ == '__main__':
    unittest.main()  