from abc import ABC, abstractmethod

class SwitchOnOffMixin(ABC):
    @abstractmethod
    def switch_on(self) -> None:
        pass

    @abstractmethod
    def switch_off(self) -> None:
        pass

    @abstractmethod
    def is_on(self) -> bool:
        pass