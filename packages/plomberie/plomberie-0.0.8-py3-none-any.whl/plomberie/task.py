from abc import ABC, abstractmethod
from typing import List, Tuple


class Task(ABC):
    def __init__(self):
        self.__dependencies: List[Task] = []

    def depends_on(self, *dependencies: 'Task') -> None:
        self.__dependencies.extend(dependencies)

    @property
    def dependencies(self) -> List['Task']:
        return self.__dependencies

    def set_progress_percent(self, out_of_100: float) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass
