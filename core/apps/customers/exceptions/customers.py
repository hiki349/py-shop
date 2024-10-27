from dataclasses import dataclass

from core.apps.common.exceptions import ServicesException


@dataclass(eq=False)
class CustomerTokenInvalid(ServicesException):
    token: str

    @property
    def message(self):
        return 'Customer token is invalid.'
