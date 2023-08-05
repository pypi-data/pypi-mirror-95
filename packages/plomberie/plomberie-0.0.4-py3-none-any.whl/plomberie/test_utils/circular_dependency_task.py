from plomberie.test_utils.test_utils import TestTask


class TaskA(TestTask):
    def depends_on(self):
        return TaskB()


class TaskB(TestTask):
    def depends_on(self):
        return TaskC()


class TaskC(TestTask):
    def depends_on(self):
        return TaskA()
