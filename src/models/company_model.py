from src.core.validator import Validator
from src.core.abstract_model import AbstractModel


###############################################
# Модель организации
class CompanyModel(AbstractModel):
    __inn: int = 0
    __bic: int = 0
    __corr_account: int = 0
    __account: int = 0
    __ownership: str = ""

    # ИНН : 12 символов
    # Счет 11 символов
    # Корреспондентский счет 11 символов
    # БИК 9 символов
    # Наименование
    # Вид собственности 5 символов

    # ИНН
    @property
    def inn(self) -> int:
        return self.__inn

    @inn.setter
    def inn(self, value: int):
        Validator.validate(value, int, 12)
        self.__inn = value

    # КПП
    @property
    def bic(self) -> int:
        return self.__bic

    @bic.setter
    def bic(self, value: int):
        Validator.validate(value, int, 9)
        self.__bic = value

    # Корреспондентский счет
    @property
    def corr_account(self) -> int:
        return self.__corr_account

    @corr_account.setter
    def corr_account(self, value: int):
        Validator.validate(value, int, 11)
        self.__corr_account = value

    @property
    def account(self) -> int:
        return self.__account

    @account.setter
    def account(self, value: int):
        Validator.validate(value, int, 11)
        self.__account = value

    @property
    def ownership(self) -> str:
        return self.__ownership

    @ownership.setter
    def ownership(self, value: str):
        Validator.validate(value, str, 5)
        self.__ownership = value.strip()






