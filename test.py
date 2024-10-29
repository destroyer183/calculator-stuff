from enum import Enum

class Test(Enum):
    test1 = 'test1'
    test2 = 'test2'
    test3 = 'test3'



for test in Test:
    print(f"value: {test}")