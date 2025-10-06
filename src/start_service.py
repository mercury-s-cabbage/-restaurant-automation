from src.reposity import reposity
from src.models.unit_model import UnitModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.recipe_model import RecipeModel
from src.models.nomenclature_group_model import NomenclatureGroupModel


class start_service:
    __repo: reposity = reposity()

    def __init__(self):
        self.__repo.data[reposity.range_key()] = {}
        self.__repo.data[reposity.nomenclature_key()] = {}
        self.__repo.data[reposity.group_key()] = {}
        self.__repo.data[reposity.recipe_key()] = {}

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance

    def __default_create_ranges(self):
        self.__repo.data[reposity.range_key()]["г"] = (UnitModel.create_gram())
        self.__repo.data[reposity.range_key()]["кг"] = (UnitModel.create_kill())
        self.__repo.data[reposity.range_key()]["л"] = (UnitModel.create_liter())
        self.__repo.data[reposity.range_key()]["шт"] = (UnitModel.create("шт"))

    def __default_create_groups(self):
        repo_groups = self.__repo.data[reposity.group_key()]

        repo_groups["Фрукты"] = NomenclatureGroupModel.create("Фрукты")
        repo_groups["Фермерские продукты"] = NomenclatureGroupModel.create("Фермерские продукты")
        repo_groups["Специи"] = NomenclatureGroupModel.create("Специи")

    def __default_create_nomenclatures(self):
        repo_nomenclature = self.__repo.data[reposity.nomenclature_key()]
        repo_unit = self.__repo.data[reposity.range_key()]

        repo_nomenclature["Кокосовое молоко"] = NomenclatureModel.create("Кокосовое молоко", repo_unit["л"])
        repo_nomenclature["Яблоко"] = NomenclatureModel.create("Яблоко", repo_unit["г"])
        repo_nomenclature["Тыква"] = NomenclatureModel.create("Тыква", repo_unit["г"])
        repo_nomenclature["Сливочное масло"] = NomenclatureModel.create("Сливочное масло", repo_unit["г"])
        repo_nomenclature["Мускатный орех"] = NomenclatureModel.create("Мускатный орех", repo_unit["г"])
        repo_nomenclature["Яйцо"] = NomenclatureModel.create("Яйцо", repo_unit["шт"])
        repo_nomenclature["Сахар"] = NomenclatureModel.create("Сахар", repo_unit["г"])
        repo_nomenclature["Мука"] = NomenclatureModel.create("Мука", repo_unit["г"])
        repo_nomenclature["Ванилин"] = NomenclatureModel.create("Ванилин", repo_unit["г"])

    def __default_create_recipes(self):
        repo_nomenclature = self.__repo.data[reposity.nomenclature_key()]
        repo_recipes = self.__repo.data[reposity.recipe_key()]

        repo_recipes["Тыквенный суп"] = RecipeModel.create(
            "Тыквенный суп",
            nomenclatures=[repo_nomenclature["Тыква"], repo_nomenclature["Яблоко"],
            repo_nomenclature["Кокосовое молоко"], repo_nomenclature["Сливочное масло"], repo_nomenclature["Мускатный орех"]],
            amounts=[1000, 200, 0.5, 50, 5]
        )

        repo_recipes["Хрустящие вафли"] = RecipeModel.create(
            "Хрустящие вафли",
            nomenclatures=[repo_nomenclature["Мука"], repo_nomenclature["Сахар"],
            repo_nomenclature["Сливочное масло"], repo_nomenclature["Яйцо"], repo_nomenclature["Ванилин"]],
            amounts=[100, 80, 70, 1, 5]
        )


    """
    Стартовый набор данных
    """

    def data(self):
        return self.__repo.data

    """
    Основной метод для генерации эталонных данных
    """

    def start(self):
        self.__default_create_ranges()
        self.__default_create_nomenclatures()
        self.__default_create_recipes()
        self.__default_create_groups()

    def get_repo(self):
        return self.__repo.data

s = start_service()
s.start()
print(s.get_repo())