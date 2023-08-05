from abc import ABC, abstractmethod
from typing import Union, Tuple


class Task(ABC):
    def depends_on(self) -> Union['Task', Tuple['Task', ...]]:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    def set_progress_percent(self, out_of_100: float) -> None:
        pass

    def __hash__(self) -> int:
        return hash(self.__class__)

    def __eq__(self, other: 'Task') -> bool:
        return self.__hash__() == other.__hash__()

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return str(self)
