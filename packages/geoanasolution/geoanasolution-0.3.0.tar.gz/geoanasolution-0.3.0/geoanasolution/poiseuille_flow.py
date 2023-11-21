import math
import numpy as np
from scipy.special import hyp1f1
from ._analytical_base import GAnalyticalSolutionBase


class PoiseuilleFlow(GAnalyticalSolutionBase):
    def __init__(self):
        super().__init__()

        # necessary parameters
        self.DIFFUSION_COE = "DiffusionCoe"
        self.HEIGHT = "Height"
        self.INITIAL_VALUE = "InitialValue"
        self.VELOCITY = "Velocity"

        # initialize necessary parameters
        self._add_param(self.DIFFUSION_COE, 0)
        self._add_param(self.HEIGHT, 0)
        self._add_param(self.INITIAL_VALUE, 0)
        self._add_param(self.VELOCITY, 0)

        # calculation using parameters
        self.__m = [1.2967, 2.3811, 3.1093, 3.6969, 4.2032, 4.6548, 5.0662, 5.4467, 5.8023, 6.1373]
        self.__C_m = [1.2008, -0.2991, 0.1608, -0.1074, 0.0796, -0.0627, 0.0515, -0.0435, 0.0375, -0.0329]

    def calc(self, sample_coordinate):
        if not isinstance(sample_coordinate, np.ndarray):
            raise TypeError("The input coordinate must in the type of np.ndarray")

        coe_2 = 0
        Pe = self.get_param(self.VELOCITY) * self.get_param(self.HEIGHT) / self.get_param(self.DIFFUSION_COE)
        x_coordinate = sample_coordinate[0]/self.get_param(self.HEIGHT)
        y_coordinate = sample_coordinate[1]/self.get_param(self.HEIGHT)

        for i in range (0, 10):
            coe_0 = pow(self.__m[i], 4) * (1/Pe) * x_coordinate;
            coe_1 = pow(self.__m[i], 2) * pow(y_coordinate, 2) * 0.5
            coe_2 += self.__C_m[i] * math.exp(-1 * coe_0 - coe_1) * self.__calc_hypergeometric_function(y_coordinate, i)

        return self.get_param(self.INITIAL_VALUE) * (1 - coe_2)

    def doc(self):
        doc = "[GeoAnaSolution] Document for the Poiseuille_Flow solution. \n" \
              "* Parameters:\n" \
              "  ----------------|----------|---------|-----------------------------------------------\n" \
              "  NAME            | UNIT     | DEFAULT | INTRODUCTION\n" \
              "  ----------------|----------|---------|-----------------------------------------------\n" \
              "  DIFFUSION_COE   | W/(m.°C) | 0\n" \
              "  HEIGHT          | m        | 0       | The height of channel.\n" \
              "  INITIAL_VALUE   | °C       | 0       | The initial value at the top boundary.\n" \
              "  VELOCITY        | m/s      | 0       | The max velocity at the bottom boundary.\n" \
              "  ----------------|----------|---------|-----------------------------------------------\n" \

        print(doc)

    def __calc_hypergeometric_function(self, y_coordinate, i):
        a = (1 - pow(self.__m[i], 2)) / 4
        b = 1 / 2
        c = pow(self.__m[i], 2) * pow(y_coordinate, 2)

        return hyp1f1(a, b, c)