from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from core.apps.customers.services.codes import BaseCodeService
from core.apps.customers.services.customers import BaseCustomerService
from core.apps.customers.services.senders import BaseSenderService


@dataclass(eq=False)
class BaseAuthService(ABC):
    customers_service: BaseCustomerService
    codes_service: BaseCodeService
    senders_service: BaseSenderService

    @abstractmethod
    def authorize(self, phone: str):
        ...

    @abstractmethod
    def confirm(self, code: str, phone: str) -> str:
        ...


class AuthService(BaseAuthService):
    def authorize(self, phone: str):
        customer = self.customers_service.get_or_create(phone)
        code = self.codes_service.generate_code(customer)
        self.senders_service.send_code(code=code, customer=customer)

    def confirm(self, code: str, phone: str) -> str:
        customer = self.customers_service.get(phone)
        self.codes_service.validate_code(code=code, customer=customer)

        return self.customers_service.generate_token(customer)
