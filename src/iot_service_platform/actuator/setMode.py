from abc import ABC, abstractmethod

class SetModeMixin(ABC):
    @abstractmethod
    def set_mode(self, mode: str) -> None:
        pass
    @abstractmethod
    def get_mode(self) -> str:
        pass
