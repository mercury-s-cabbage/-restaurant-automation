from src.core.validator import Validator
from src.core.abstract_model import AbstractModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.unit_model import UnitModel

###############################################
# Модель рецепта


class RecipeModel(AbstractModel):
    __description: str = ""
    _cache = {}


    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.ingredients = {}  # Список объектов Ingredient

    @staticmethod
    def create(name: str, nomenclatures: list = None, amounts: list = None):
        if name in RecipeModel._cache:
            return RecipeModel._cache[name]
        item = RecipeModel(name)
        if nomenclatures and amounts:
            if len(nomenclatures) != len(amounts):
                raise ValueError("Списки номенклатур и количеств должны быть одинаковой длины")
            for nomenclature, amount in zip(nomenclatures, amounts):
                item.add_ingredient(nomenclature, amount)
        RecipeModel._cache[name] = item
        return item

    def add_ingredient(self, nomenclature: NomenclatureModel, amount: float):
        self.ingredients[nomenclature.name] = {
            "amount": amount,
            "unit": nomenclature.unit
        }

    def __repr__(self):
        ingredients_str = ", ".join(
            f"{name}: {data['amount']} {data['unit']}" for name, data in self.ingredients.items()
        )
        return f"{self.name!r}. Ингредиенты: {{ {ingredients_str} }}"

