from enum import Enum
import math
import sys
from enum import Enum



class Data(Enum):
    R = 'r'
    X = 'x'
    Y = 'y'
    Theta = 'theta'
    Alpha = 'alpha'
    S = 's'
    Sin = 'sine'
    Cos = 'cosine'
    Tan = 'tangent'
    Csc = 'cosecant'
    Sec = 'secant'
    Cot = 'cotangent'



class Logic:

    data_values = {
        Data.R: None,
        Data.X: None,
        Data.Y: None,
        Data.Theta: None,
        Data.Alpha: None,
        Data.S: None,
        Data.Sin: None,
        Data.Cos: None,
        Data.Tan: None,
        Data.Csc: None,
        Data.Sec: None,
        Data.Cot: None
    }

    def __init__(self) -> None:

        pass