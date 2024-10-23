from dataclasses import dataclass


@dataclass(eq=False)
class ServicesException(Exception):
    @property
    def message(self):
        return 'Appication exception accured.'
