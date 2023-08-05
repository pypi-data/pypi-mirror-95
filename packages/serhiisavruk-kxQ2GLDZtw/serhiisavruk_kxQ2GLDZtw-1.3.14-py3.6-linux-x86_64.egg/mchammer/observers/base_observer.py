"""
Definition of the base observer class.
"""

from abc import ABC, abstractmethod
from typing import Any
from ase import Atoms


class BaseObserver(ABC):
    """
    Base observer class.

    Parameters
    ----------
    interval : int
        the observation interval, defaults to None meaning that if the
        observer is used in a Monte Carlo simulation, then the Ensemble object
        will set the interval.
    tag : str
        human readable tag used for identifying the observer

    Attributes
    ----------
    tag : str
        human readable tag used for identifying the observer
    interval : int
        the observation interval
    """

    def __init__(self, return_type: type, interval: int = None, tag: str = 'BaseObserver') -> None:
        self.tag = tag
        self.interval = interval
        self._return_type = return_type

    @property
    def return_type(self) -> type:
        """Data type of the observed data."""
        return self._return_type

    @abstractmethod
    def get_observable(self, structure: Atoms) -> Any:
        """
        Method used for extracting data.

        Returns
        -------
        self.return_type()

        When implementing this method use the following names for the
        following types of data:

        ASE Atoms object : `structure`.
        list of chemical species : `species`.
        icet cluster expansion : `cluster_expansion`.
        mchammer calculator : `calculator`.
        """
        raise NotImplementedError
