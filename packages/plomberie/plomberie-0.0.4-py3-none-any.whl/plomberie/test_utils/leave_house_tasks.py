from plomberie.test_utils.test_utils import TestTask


class TakeShower(TestTask):
    pass


class PutOnUnderwear(TestTask):
    def depends_on(self):
        return TakeShower()


class PutOnSocks(TestTask):
    def depends_on(self):
        return TakeShower()


class PutOnShirt(TestTask):
    def depends_on(self):
        return TakeShower()


class PutOnJacket(TestTask):
    def depends_on(self):
        return PutOnShirt()


class PutOnPants(TestTask):
    def depends_on(self):
        return PutOnUnderwear()


class PutOnShoes(TestTask):
    def depends_on(self):
        return PutOnPants(), PutOnSocks()


class LeaveHouse(TestTask):
    def depends_on(self):
        return PutOnShoes(), PutOnJacket()
