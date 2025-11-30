from Src.reposity import reposity
from Src.Logics.factory_entities import factory_entities
from Src.Core.response_formats import response_formats
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Core.validator import validator, argument_exception, operation_exception
import os
import json
from Src.Models.receipt_model import receipt_model
from Src.Models.receipt_item_model import receipt_item_model
from Src.Models.storage_model import storage_model
from Src.Models.transaction_model import transaction_model
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.category_dto import category_dto
from Src.Dtos.storage_dto import storage_dto
from Src.Dtos.transaction_dto import transaction_dto
from Src.Core.prototype_inspector import prototype_inspector
from Src.Core.prototype import prototype

class start_service:
    # Репозиторий
    __repo: reposity = reposity()

    # Хранилище кэша запросов пользователей
    __requests: prototype_inspector = prototype_inspector()

    # Дата, с которой начинается открытый период
    __block_period: str

    # Дата, с которой начинается открытый период
    __current_transactions: prototype

    # Рецепт по умолчанию
    __default_receipt: receipt_model

    # Формат по умолчанию
    __default_format: str = "json"

    # Словарь который содержит загруженные и инициализованные инстансы нужных объектов
    # Ключ - id записи, значение - abstract_model
    __cache = {}

    # Наименование файла (полный путь)
    __full_file_name:str = ""

    def __init__(self):
        self.__repo.initalize()
        self.__requests.initalize()

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance 

    # Текущий файл
    @property
    def file_name(self) -> str:
        return self.__full_file_name

    @property
    def cache(self) -> dict:
        return self.__cache

    @property
    def requests(self):
        return self.__requests

    @property
    def current_transactions(self):
        return self.__current_transactions
    @property
    def blocking_date(self):
        return self.__block_period

    @blocking_date.setter
    def blocking_date(self, value):
        self.__block_period = value

    @property
    def default_format(self) -> str:
        return self.__default_format

    # Полный путь к файлу настроек
    @file_name.setter
    def file_name(self, value:str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)        
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')

    # получить репозиторий целиком
    @property
    def repository(self):
        return self.__repo

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")

        try:
            with open(self.__full_file_name, 'r', encoding='utf-8') as file_instance:
                settings = json.load(file_instance)

                if "default_receipt" in settings.keys():
                    data = settings
                    if "default_format" in settings:
                        self.__default_format = settings["default_format"]
                    if "block_period" in settings:
                        self.__block_period = settings["block_period"]
                    if self.convert(data):
                        return self.load_past_data()

            return False
        except Exception as e:
            error_message = str(e)
            return False
        
    # Сохранить элемент в репозитории
    def __save_item(self, key:str, dto, item):
        validator.validate(key, str)
        item.unique_code = dto.id
        self.__cache.setdefault(dto.id, item)
        self.__repo.data[key].append(item)

        return True

    # Загрузить единицы измерений   
    def __convert_ranges(self, data: dict) -> bool:
        validator.validate(data, dict)
        ranges = data['ranges'] if 'ranges' in data else []    
        if len(ranges) == 0:
            return False
         
        for range in ranges:
            dto = range_dto().create(range)
            item = range_model.from_dto(dto, self.__cache)
            self.__save_item( reposity.range_key(), dto, item )

        return True

    # Загрузить группы номенклатуры
    def __convert_groups(self, data: dict) -> bool:
        validator.validate(data, dict)
        categories =  data['categories'] if 'categories' in data else []
        if len(categories) == 0:
            return False

        for category in  categories:
            dto = category_dto().create(category)    
            item = group_model.from_dto(dto, self.__cache )
            self.__save_item( reposity.group_key(), dto, item )

        return True

    # Загрузить номенклатуру
    def __convert_nomenclatures(self, data: dict) -> bool:
        validator.validate(data, dict)
        nomenclatures = data['nomenclatures'] if 'nomenclatures' in data else []   
        if len(nomenclatures) == 0:
            return False
         
        for nomenclature in nomenclatures:
            dto = nomenclature_dto().create(nomenclature)
            item = nomenclature_model.from_dto(dto, self.__cache)
            self.__save_item( reposity.nomenclature_key(), dto, item )

        return True

    # Загрузить транзакции
    def __convert_transactions(self, data: dict) -> bool:
        if len(data) == 0:
            return False

        transactions = data['transactions'] if 'transactions' in data else []

        for transaction in transactions:
            dto = transaction_dto().create(transaction)
            item = transaction_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.transactions_key(), dto, item)


        return True

    # Загрузить склады
    def __convert_storages(self, data: dict) -> bool:
        if len(data) == 0:
            return False

        for storage in data:
            dto = storage_dto().create(storage)
            item = storage_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.storage_key(), dto, item)
            self.__convert_transactions(storage)

        return True


    # Обработать полученный словарь
    def convert(self, data: dict) -> bool:
        default_receipt = data["default_receipt"]
        default_storages = data["warehouses"]
        validator.validate(default_receipt, dict)

        # 1 Созданим рецепт
        cooking_time = default_receipt['cooking_time'] if 'cooking_time' in default_receipt else ""
        portions = int(default_receipt['portions']) if 'portions' in default_receipt else 0
        name = default_receipt['name'] if 'name' in default_receipt else "НЕ ИЗВЕСТНО"
        self.__default_receipt = receipt_model.create(name, cooking_time, portions)

        # Загрузим шаги приготовления
        steps = default_receipt['steps'] if 'steps' in default_receipt else []
        for step in steps:
            if step.strip() != "":
                self.__default_receipt.steps.append(step)

        # Создадим другие модели
        self.__convert_ranges(default_receipt)
        self.__convert_groups(default_receipt)
        self.__convert_nomenclatures(default_receipt)
        self.__convert_storages(default_storages)


        # Собираем рецепт
        compositions =  data['composition'] if 'composition' in data else []
        for composition in compositions:
            namnomenclature_id = composition['nomenclature_id'] if 'nomenclature_id' in composition else ""
            range_id = composition['range_id'] if 'range_id' in composition else ""
            value  = composition['value'] if 'value' in composition else ""
            nomenclature = self.__cache[namnomenclature_id] if namnomenclature_id in self.__cache else None
            range = self.__cache[range_id] if range_id in self.__cache else None
            item = receipt_item_model.create(  nomenclature, range, value)
            self.__default_receipt.composition.append(item)

        # Сохраняем рецепт
        self.__repo.data[ reposity.receipt_key() ].append(self.__default_receipt)
        return True

    """
    Добавляем в кэш данные о закрытом периоде
    """
    def load_past_data(self) -> bool:
        try:
            all_transactions = self.repository.data.get(self.repository.transactions_key(), [])
            all_transactions_p = prototype(all_transactions)

            # Сохраняем в кэше остатки за закрытый период, получаем только текущие транзакции
            current_transactions = self.__requests.count_blocking_cash(all_transactions_p, self.__block_period)
            self.__current_transactions = current_transactions
        except:
            raise operation_exception("Не вышло загрузить остатки!")
        return True


    """
    Стартовый набор данных
    """
    @property
    def data(self):
        return self.__repo.data   

    """
    Основной метод для генерации эталонных данных
    """
    def start(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        saves_dir = os.path.abspath(os.path.join(current_dir, "..", "Saves"))

        # Перебираем все файлы в директории Saves
        if not os.path.exists(saves_dir) or not os.path.isdir(saves_dir):
            raise operation_exception(f"Директория {saves_dir} не найдена")

        for filename in os.listdir(saves_dir):
            if filename.lower().endswith('.json'):
                full_path = os.path.join(saves_dir, filename)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                        # Проверяем параметр first_start
                        if data.get("first_start") == "True":
                            self.file_name = full_path
                            break
                except Exception as e:
                    # Пропускаем файл при ошибке чтения
                    continue


        if self.file_name is None:
            raise operation_exception(f"Не найден файл с параметром first_start: True в директории {saves_dir}")

        # Загружаем
        result = self.load()
        if result == False:
            raise operation_exception("Невозможно сформировать стартовый набор данных!")



    def save(self, filename: str, first_start_flag: str = "True"):
        """
        Сохраняет текущее состояние репозитория в JSON-файл.
        :param filename: Путь к файлу сохранения
        :param first_start_flag: Значение поля first_start ("True" по умолчанию)
        :return: True при успешной записи
        """
        try:
            responses = {}
            with open(filename, 'w', encoding='utf-8') as f:
                factory = factory_entities()
                instance = factory.create( response_formats.csv() )
                for key in self.repository.data:
                    resp = instance().build(self.repository.data[key])
                    responses[str(key)] = resp
                json.dump(responses, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            return False


