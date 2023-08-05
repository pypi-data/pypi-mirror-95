from typing import Union, Tuple
from unittest import TestCase

from plomberie import Task


class TaskTest(TestCase):

    def test_instances_of_same_task_class(self):
        with self.subTest('set equality'):
            self.assertEqual(len({FooTask(), FooTask()}), 1)
        with self.subTest('dict key equality'):
            a_dict = {
                FooTask(): 'foo',
                FooTask(): 'foo'
            }
            self.assertEqual(len(a_dict), 1)

    def test_instances_of_different_task_classes(self):
        with self.subTest('set inequality'):
            self.assertEqual(len({FooTask(), BarTask()}), 2)
        with self.subTest('dict key inequality'):
            a_dict = {
                FooTask(): 'foo',
                BarTask(): 'bar'
            }
            self.assertEqual(len(a_dict), 2)


class BarTask(Task):
    def depends_on(self) -> Union['Task', Tuple['Task', ...]]:
        pass

    def run(self) -> None:
        pass


class FooTask(Task):
    def depends_on(self) -> Union['Task', Tuple['Task', ...]]:
        pass

    def run(self) -> None:
        pass
