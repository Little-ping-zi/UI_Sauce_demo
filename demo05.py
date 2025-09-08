import unittest


class demo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.count = 4

    @classmethod
    def tes_example(cls):
        # cls.count = 3
        print(cls.count)

    def tes_actual(self):
        # number = self.__class__.count
        # print(number)
        print(self.count)


    def tes_fanother(self):
        print(self.count)


# if __name__ == '__main__':
#     unittest.main()
demo1 = demo()
demo1.tes_example()
demo1.tes_actual()