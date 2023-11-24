import numpy as np
from scipy import optimize, integrate
from pathlib import Path

from .utilities import CustomBaseModel
from typing import List


class AxialInductionModel(CustomBaseModel):
    """
    Base AxialInductionModel object class. Subclasses are:
     - Constant
     - Joukowsky
     - ThrustMatch
     - InductionMatch
     - UserInput
    """

    @classmethod
    def get_subclass(cls, name):
        for _cls in cls.__subclasses__():
            if _cls.__name__.lower() == name.lower():
                return _cls
        else:
            raise AttributeError(f"{name} not found among axial induction models.")


class Constant(AxialInductionModel):
    """
    Subclass of the :py:class:`jDWM.AxialInductionModel.AxialInductionModel` object class.
    Returns a constant axial induction over the rotor given a thrust coefficient
    as input.
    """

    ct: float
    r_max: float = 3
    Nr: int = 501

    def _ct2a(self, ct):
        k1, k2, k3 = 0.246, 0.0586, 0.0883
        return k1 * ct + k2 * ct ** 2 + k3 * ct ** 3

    def function(self, **kwargs):
        self.update(**kwargs)

        r = np.linspace(0, self.r_max, self.Nr)
        a = np.zeros_like(r)
        a[r <= 1] = self._ct2a(self.ct)

        return r, a


class Joukowsky(AxialInductionModel):
    """
    Subclass of the :py:class:`jDWM.AxialInductionModel.AxialInductionModel` object class.
    """

    tsr: float
    ct: float
    a: float = 1.256
    b: float = 2
    delta: float = 0.2
    r_max: float = 3
    Nr: int = 501
    Nb: int = 3

    def function(self, **kwargs):
        self.update(**kwargs)

        r = np.linspace(0, self.r_max, self.Nr)
        a = np.zeros_like(r)
        a[r <= 1] = self.ud(r[r <= 1], self.tsr, self.ct)

        return r, a

    def ud(self, X, tsr, Ct):
        """
        axial induction (ie. dimensionless axial velocity at the rotor disk)
        along the blade, u_d/U_0, derived by jyli assuming constant axial
        induction, not sure if correct. Only valid for Ct ~< 1.
        """

        return (1 - np.sqrt(1 - Ct)) / 2 * self.FG(X, tsr)

    def F(self, x, tsr):
        """
        Prandtl tip correction, F(x).
        Equation (9) in Sorensen et al. (2019)
        """
        return (
            2
            / np.pi
            * np.arccos(np.exp(-self.Nb / 2 * np.sqrt(1 + tsr ** 2) * (1 - x)))
        )

    def G(self, x):
        """
        Root correction, G(x).
        Equation (10) in Sorensen et al. (2019)
        """
        return 1 - np.exp(-self.a * (x / self.delta) ** self.b)

    def FG(self, x, tsr):
        """
        Product of tip and root equation.
        Equation (9) and (10) in Sorensen et al. (2019)
        """
        return self.F(x, tsr) * self.G(x)


class ThrustMatch(AxialInductionModel):
    """
    Subclass of the :py:class:`jDWM.AxialInductionModel.AxialInductionModel` object class.
    """

    tsr: float
    ct: float
    r_max: float = 3
    Nr: int = 501
    Nb: int = 3
    delta: float = 0.1
    root_a: float = 1.256
    _root_b: float = None

    def update(self, **kwargs):
        super().update(**kwargs)
        self._root_b = (np.exp(self.root_a) - 1) / self.root_a

    def _tip_correction(self, x, tsr):
        return (
            2
            / np.pi
            * np.arccos(np.exp(-self.Nb / 2 * np.sqrt(1 + tsr ** 2) * (1 - x)))
        )

    def _root_correction(self, x):
        return 1 - np.exp(-self.root_a * (x / self.delta) ** self._root_b)

    def _ct2a(self, ct):
        k1, k2, k3 = 0.246, 0.0586, 0.0883
        return k1 * ct + k2 * ct ** 2 + k3 * ct ** 3

    def _a2ct(self, a):
        """
        Solves the cubic equation using the method outlined in 'The Use of Hyperbolic
        Cosines in Solving Cubic Polynomials' (2002) by G. C. Holmes.
        """
        k1, k2, k3 = 0.246, 0.0586, 0.0883
        P = (3 * k3 * k1 - k2 ** 2) / (3 * k3 ** 2)
        Q = (2 * k2 ** 3 - 9 * k3 * k2 * k1) / (27 * k3 ** 3) - a / k3

        hyp_sol = (
            -2
            * np.sqrt(P / 3)
            * np.sinh(1 / 3 * np.arcsinh(3 * Q / (2 * P) * np.sqrt(3 / P)))
        )
        return hyp_sol - k2 / (3 * k3)

    def function(self, **kwargs):
        self.update(**kwargs)

        def cost(a_hat):
            func = (
                lambda x: self._a2ct(
                    a_hat * self._tip_correction(x, self.tsr) * self._root_correction(x)
                )
                * x
            )
            return self.ct - 2 * integrate.quad(func, 0, 1)[0]

        a_hat = optimize.newton(cost, 0.3)

        r = np.linspace(0, self.r_max, self.Nr)
        a = np.zeros_like(r)
        a[r <= 1] = (
            a_hat
            * self._tip_correction(r[r <= 1], self.tsr)
            * self._root_correction(r[r <= 1])
        )

        return r, a


class InductionMatch(AxialInductionModel):
    """
    Subclass of the :py:class:`jDWM.AxialInductionModel.AxialInductionModel` object class.
    """

    tsr: float
    ct: float
    r_max: float = 3
    Nr: int = 501
    Nb: int = 3
    delta: float = 0.1
    root_a: float = 1.256
    _root_b: float = None

    def update(self, **kwargs):
        super().update(**kwargs)
        self._root_b = (np.exp(self.root_a) - 1) / self.root_a

    def _tip_correction(self, x, tsr):
        return (
            2
            / np.pi
            * np.arccos(np.exp(-self.Nb / 2 * np.sqrt(1 + tsr ** 2) * (1 - x)))
        )

    def _root_correction(self, x):
        return 1 - np.exp(-self.root_a * (x / self.delta) ** self._root_b)

    def _ct2a(self, ct):
        k1, k2, k3 = 0.246, 0.0586, 0.0883
        return k1 * ct + k2 * ct ** 2 + k3 * ct ** 3

    def function(self, **kwargs):
        self.update(**kwargs)
        a_mean = self._ct2a(self.ct)

        func = (
            lambda x: (self._tip_correction(x, self.tsr) * self._root_correction(x)) * x
        )
        a_hat = a_mean / (2 * integrate.quad(func, 0, 1)[0])

        r = np.linspace(0, self.r_max, self.Nr)
        a = np.zeros_like(r)
        a[r <= 1] = (
            a_hat
            * self._tip_correction(r[r <= 1], self.tsr)
            * self._root_correction(r[r <= 1])
        )

        return r, a


class InductionMatch2(AxialInductionModel):
    """
    Subclass of the :py:class:`jDWM.AxialInductionModel.InductionMatch` object class.
    """

    tsr: float
    a_target: float
    r_max: float = 3
    Nr: int = 501
    Nb: int = 3
    delta: float = 0.1
    root_a: float = 1.256
    _root_b: float = None

    def update(self, **kwargs):
        super().update(**kwargs)
        self._root_b = (np.exp(self.root_a) - 1) / self.root_a

    def _tip_correction(self, x, tsr):
        return (
            2
            / np.pi
            * np.arccos(np.exp(-self.Nb / 2 * np.sqrt(1 + tsr ** 2) * (1 - x)))
        )

    def _root_correction(self, x):
        return 1 - np.exp(-self.root_a * (x / self.delta) ** self._root_b)

    def _ct2a(self, ct):
        k1, k2, k3 = 0.246, 0.0586, 0.0883
        return k1 * ct + k2 * ct ** 2 + k3 * ct ** 3

    def function(self, **kwargs):
        self.update(**kwargs)
        a_mean = self.a_target
        # Effect of varying fidelity turbine models on wake loss prediction
        func = (
            lambda x: (self._tip_correction(x, self.tsr) * self._root_correction(x)) * x
        )
        a_hat = a_mean / (2 * integrate.quad(func, 0, 1)[0])

        r = np.linspace(0, self.r_max, self.Nr)
        a = np.zeros_like(r)
        a[r <= 1] = (
            a_hat
            * self._tip_correction(r[r <= 1], self.tsr)
            * self._root_correction(r[r <= 1])
        )

        return r, a


class UserInput(AxialInductionModel):
    """
    Subclass of the :py:class:`jDWM.AxialInductionModel.AxialInductionModel` object class.
    """

    axial_r: np.ndarray = None
    axial_a: np.ndarray = None

    def function(self, **kwargs):
        self.update(**kwargs)

        if any(x is None for x in [self.axial_r, self.axial_a]):
            raise AttributeError(
                "axial_r and/or axial_a are note set in the AxialInductionModel."
            )
        assert len(self.axial_r) == len(self.axial_a)

        return self.axial_r, self.axial_a
