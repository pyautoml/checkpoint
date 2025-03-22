from abc import ABC, abstractmethod

class AbstractPathModel(ABC):
    @abstractmethod
    def verify_path() -> str:
        pass
