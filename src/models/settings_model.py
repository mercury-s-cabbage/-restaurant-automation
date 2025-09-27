from src.models.company_model import CompanyModel
from src.core.validator import Validator
from src.core.abstract_model import AbstractModel


######################################
# Модель настроек приложения
class SettingsModel(AbstractModel):
    __company: CompanyModel = None

    # Текущая организация
    @property
    def company(self) -> CompanyModel:
        return self.__company

    @company.setter
    def company(self, value: CompanyModel):
        Validator.validate(value, CompanyModel)
        self.__company = value