class company_model:
    __name: str = ""
    __inn: int
    __acc: int
    __corr_acc: int
    __bic: int
    __prop: str = ""

    @property
    def name(self) -> str:
        return self.__name

    @property
    def inn(self) -> int:
        return self.__inn

    @property
    def acc(self) -> int:
        return self.__acc

    @property
    def corr_acc(self) -> int:
        return self.__corr_acc

    @property
    def bic(self) -> int:
        return self.__bic

    @property
    def prop(self) -> str:
        return self.__prop

    @name.setter
    def name(self, value:str):
        if value.strip() != "":
            self.__name = value.strip()

    @inn.setter
    def inn(self, value: int):
        if len(str(value)) == 12 and value.is_integer():
            self.__inn = value

    @acc.setter
    def acc(self, value: int):
        if len(str(value)) == 11 and value.is_integer():
            self.__acc = value
    @corr_acc.setter
    def corr_acc(self, value: int):
        if len(str(value)) == 11 and value.is_integer():
            self.__corr_acc = value

    @bic.setter
    def bic(self, value: int):
        if len(str(value)) == 9 and value.is_integer():
            self.__bic = value

    @prop.setter
    def prop(self, value: str):
        if len(str(value)) <= 5 and value.isalpha():
            self.__prop = value

