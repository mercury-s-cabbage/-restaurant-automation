from src.models.company_model import CompanyModel
from src.core.validator import validator
from src.core.abstract_model import abstact_model


######################################
# Модель настроек приложения
class SettingsModel(abstact_model):
    __company: CompanyModel = None

    # Текущая организация
    @property
    def company(self) -> CompanyModel:
        return self.__company

    @company.setter
    def company(self, value: CompanyModel):
        validator.validate(value, CompanyModel)
        self.__company = value