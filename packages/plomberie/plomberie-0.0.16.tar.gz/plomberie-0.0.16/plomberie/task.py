from abc import ABC, abstractmethod
from typing import List, Awaitable, Optional

from tqdm import tqdm


class Task(ABC):
    def __init__(self):
        self.__dependencies: List[Task] = []
        self.__progress_bar: Optional[tqdm] = None

    def depends_on(self, *dependencies: 'Task') -> 'Task':
        self.__dependencies.extend(dependencies)
        return self

    def post_run(self):
        if self.__progress_bar:
            self.__progress_bar.update(100 - self.__progress_bar.n)
            self.__progress_bar.close()

    @property
    def dependencies(self) -> List['Task']:
        return self.__dependencies

    def set_progress_percent(self, out_of_100: float) -> None:
        if not self.__progress_bar:
            self.__progress_bar = tqdm(
                desc=self.__class__.__name__,
                total=100,
                ascii='#',
                bar_format='{desc}: [{bar}] {percentage:.2f}% ({elapsed}<{remaining})'
            )
        self.__progress_bar.update(out_of_100 - self.__progress_bar.n)

    @abstractmethod
    def run(self) -> Awaitable:
        pass
