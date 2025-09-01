from abc import ABC, abstractmethod

class SetValueMixin(ABC):
    @abstractmethod
    def set_value(self, value: float) -> None:
        pass
    @abstractmethod
    def get_value(self) -> float:
        pass