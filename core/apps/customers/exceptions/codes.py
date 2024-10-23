from dataclasses import dataclass

from core.apps.common.exceptions import ServicesException


@dataclass(eq=False)
class CodeException(ServicesException):
    @property
    def message(self):
        return 'Auth code exception occurred.'


@dataclass(eq=False)
class CodeNotFoundException(CodeException):
    code: str

    @property
    def message(self):
        return 'Code not found.'


@dataclass(eq=False)
class CodesNotEuqleException(CodeException):
    code: str
    cache_code: str
    customer_phone: str

    @property
    def message(self):
        return 'Codes not euqal.'
