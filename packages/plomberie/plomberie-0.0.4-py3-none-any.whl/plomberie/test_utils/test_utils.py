from typing import List, Type

from plomberie import Task

call_sequence: List[Type['TestTask']] = []


class TestTask(Task):
    def run(self) -> None:
        call_sequence.append(self.__class__)
