from typing import Type, Optional
from unittest import TestCase

from timeout_decorator import timeout

from plomberie import Manager
from plomberie.exceptions import CircularDependencyException
from plomberie.test_utils.circular_dependency_task import TaskA
from plomberie.test_utils.leave_house_tasks import LeaveHouse, PutOnShoes, PutOnJacket, TakeShower
from plomberie.test_utils.test_utils import call_sequence, TestTask


class ManagerTest(TestCase):
    def test_leave_house(self):
        manager = Manager()
        manager.launch(LeaveHouse())

        with self.subTest('Leave house last'):
            self.assertEqual(call_sequence[-1], LeaveHouse)

        with self.subTest('Put on shoes and jacket before leaving'):
            self.__assert_sequence(PutOnShoes, LeaveHouse)
            self.__assert_sequence(PutOnJacket, LeaveHouse)

        with self.subTest('Take a shower first'):
            self.assertEqual(call_sequence[0], TakeShower)

        with self.subTest('Complete all tasks'):
            self.assertEqual(len(call_sequence), 8)

    @timeout(1)
    def test_circular_dependency(self):
        manager = Manager()
        self.assertRaises(CircularDependencyException, lambda: manager.launch(TaskA()))

    def __assert_sequence(self, first_test_task_class: Type[TestTask], second_test_task_class: Type[TestTask]) -> None:
        index_of_first = self.__get_call_index(first_test_task_class)
        index_of_second = self.__get_call_index(second_test_task_class)
        self.assertLess(index_of_first, index_of_second)

    @staticmethod
    def __get_call_index(test_task_class: Type[TestTask]) -> Optional[int]:
        return next((i for i, t in enumerate(call_sequence) if t == test_task_class), None)
