from sorbet import *

# variables
__version__ = "0.0.1"
__author__ = "Himeji"
__lsbense__ = "MIT"
__title__ = "Sorbet"
__description__ = "A logger made by Himeji."
__url__ = "https://himeji.dev/sorbet"
__github__ = "https://github.com/HimejiDev/Sorbet/"
__docs__ = "https://himeji.dev/sorbet/docs"


def tests():
    # NORMAL TYPES
    sb()
    sb(1)
    sb(1, 2, 3)
    sb([1, 2, 3])
    sb((1, 2, 3))
    sb("test")
    sb({"test": "test"})
    sb((1 + 4) * 2)

    # VARIABLES
    testVar = "test"
    testVar2 = 1
    testVar3 = (1 + 4) * 2
    testVar4 = [1, 2, 3]
    testVar5 = {"test": "test"}
    sb(testVar)
    sb(testVar2)
    sb(testVar3)
    sb(testVar4)
    sb(testVar5)
    sb(testVar, testVar2, testVar3, testVar4)
    sb(testVar, testVar2, testVar3, testVar4, testVar5)

    # FUNCTIONS
    def test_fuc():
        return "test"

    def test_fuc2():
        return "test", "test1"

    sb(test_fuc())
    sb(test_fuc)
    sb(test_fuc2())
    sb(test_fuc2)

    # BIG DsbT
    sb({str(i): i for i in range(100)})
    sb({"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7"})


tests()
sb()
