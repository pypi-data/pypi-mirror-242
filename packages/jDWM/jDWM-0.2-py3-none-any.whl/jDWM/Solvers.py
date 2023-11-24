import numpy as np
from .utilities import CustomBaseModel, Ainslie

from scipy import linalg


class Solver(CustomBaseModel):
    """
    Base Solver object class. Subclasses are:
     - python
     - implicit
     - explicit
    """

    @classmethod
    def get_subclass(cls, name):
        for _cls in cls.__subclasses__():
            if _cls.__name__.lower() == name.lower():
                return _cls
        else:
            raise AttributeError(f"{name} not found among solvers.")


class python(Solver):
    """

    """

    def evolve(self, r, U, V, visc, dx, dr):
        return Ainslie.evolve(r, U, V, visc, dx, dr)


class implicit(Solver):
    """

    """

    def evolve(self, r, U, V, visc, dx, dr):
        return Ainslie.evolve(r, U, V, visc, dx, dr)


class explicit(Solver):
    """

    """

    def evolve(self, r, U, V, visc, dx, dr):
        return Ainslie.evolve_explicit(r, U, V, visc, dx, dr)
