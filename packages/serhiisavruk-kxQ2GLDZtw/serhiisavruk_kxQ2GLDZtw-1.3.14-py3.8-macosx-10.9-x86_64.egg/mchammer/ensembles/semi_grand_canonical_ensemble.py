"""
Definition of the semi-grand canonical ensemble class.
"""

from ase import Atoms
from ase.data import atomic_numbers, chemical_symbols
from ase.units import kB
from collections import OrderedDict
from typing import Dict, Union, List

from .. import DataContainer
from ..calculators.base_calculator import BaseCalculator
from .thermodynamic_base_ensemble import ThermodynamicBaseEnsemble


class SemiGrandCanonicalEnsemble(ThermodynamicBaseEnsemble):
    """Instances of this class allow one to simulate systems in the
    semi-grand canonical (SGC) ensemble (:math:`N\\Delta\\mu_i VT`), i.e. at
    constant temperature (:math:`T`), total number of sites (:math:`N=\\sum_i
    N_i`), relative chemical potentials (:math:`\\Delta\\mu_i=\\mu_i - \\mu_1`,
    where :math:`i` denotes the species), and volume (:math:`V`).

    The probability for a particular state in the SGC ensemble for a
    :math:`m`-component system can be written

    .. math::

        \\rho_{\\text{SGC}} \\propto \\exp\\Big[ - \\big( E
        + \\sum_{i>1}^m \\Delta\\mu_i N_i \\big) \\big / k_B T \\Big]

    with the *relative* chemical potentials :math:`\\Delta\\mu_i = \\mu_i -
    \\mu_1` and species counts :math:`N_i`. Unlike the :ref:`canonical ensemble
    <canonical_ensemble>`, the number of the respective species (or,
    equivalently, the concentrations) are allowed to vary in the SGC ensemble.
    A trial step thus consists of randomly picking an atom and changing its
    identity with probability

    .. math::

        P = \\min \\Big\\{ 1, \\, \\exp \\big[ - \\big( \\Delta E
        + \\sum_i \\Delta \\mu_i \\Delta N_i \\big) \\big / k_B T \\big]
        \\Big\\},

    where :math:`\\Delta E` is the change in potential energy caused by the
    swap.

    There exists a simple relation between the differences in chemical
    potential and the canonical free energy :math:`F`. In a binary system, this
    relationship reads

    .. math:: \\Delta \\mu = - \\frac{1}{N} \\frac{\\partial F}{\\partial c} (
        N, V, T, \\langle c \\rangle).

    Here :math:`c` denotes concentration (:math:`c=N_i/N`) and :math:`\\langle
    c \\rangle` the average concentration observed in the simulation. By
    recording :math:`\\langle c \\rangle` while gradually changing
    :math:`\\Delta \\mu`, one can thus in principle calculate the difference in
    canonical free energy between the pure phases (:math:`c=0` or :math:`1`)
    and any concentration by integrating :math:`\\Delta \\mu` over that
    concentration range. In practice this requires that the average recorded
    concentration :math:`\\langle c \\rangle` varies continuously with
    :math:`\\Delta \\mu`. This is not the case for materials with multiphase
    regions (such as miscibility gaps), because in such regions :math:`\\Delta
    \\mu` maps to multiple concentrations. In a Monte Carlo simulation, this is
    typically manifested by discontinuous jumps in concentration. Such jumps
    mark the phase boundaries of a multiphase region and can thus be used to
    construct the phase diagram. To recover the free energy, however, such
    systems require sampling in other ensembles, such as the
    :ref:`variance-constrained semi-grand canonical ensemble <sgc_ensemble>`.

    Parameters
    ----------
    structure : :class:`Atoms <ase.Atoms>`
        atomic configuration to be used in the Monte Carlo simulation;
        also defines the initial occupation vector
    calculator : :class:`BaseCalculator <mchammer.calculators.ClusterExpansionCalculator>`
        calculator to be used for calculating the potential changes
        that enter the evaluation of the Metropolis criterion
    temperature : float
        temperature :math:`T` in appropriate units [commonly Kelvin]
    chemical_potentials : Dict[str, float]
        chemical potential for each species :math:`\\mu_i`; the key
        denotes the species, the value specifies the chemical potential in
        units that are consistent with the underlying cluster expansion
    boltzmann_constant : float
        Boltzmann constant :math:`k_B` in appropriate
        units, i.e. units that are consistent
        with the underlying cluster expansion
        and the temperature units [default: eV/K]
    user_tag : str
        human-readable tag for ensemble [default: None]
    random_seed : int
        seed for the random number generator used in the Monte Carlo
        simulation
    dc_filename : str
        name of file the data container associated with the ensemble
        will be written to; if the file exists it will be read, the
        data container will be appended, and the file will be
        updated/overwritten
    data_container_write_period : float
        period in units of seconds at which the data container is
        written to file; writing periodically to file provides both
        a way to examine the progress of the simulation and to back up
        the data [default: 600 s]
    ensemble_data_write_interval : int
        interval at which data is written to the data container; this
        includes for example the current value of the calculator
        (i.e. usually the energy) as well as ensembles specific fields
        such as temperature or the number of atoms of different species
    trajectory_write_interval : int
        interval at which the current occupation vector of the atomic
        configuration is written to the data container.
    sublattice_probabilities : List[float]
        probability for picking a sublattice when doing a random flip.
        This should be as long as the number of sublattices and should
        sum up to 1.

    Example
    -------
    The following snippet illustrate how to carry out a simple Monte Carlo
    simulation in the semi-canonical ensemble. Here, the parameters of the
    cluster expansion are set to emulate a simple Ising model in order to
    obtain an example that can be run without modification. In practice, one
    should of course use a proper cluster expansion::

        >>> from ase.build import bulk
        >>> from icet import ClusterExpansion, ClusterSpace
        >>> from mchammer.calculators import ClusterExpansionCalculator

        >>> # prepare cluster expansion
        >>> # the setup emulates a second nearest-neighbor (NN) Ising model
        >>> # (zerolet and singlet ECIs are zero; only first and second neighbor
        >>> # pairs are included)
        >>> prim = bulk('Au')
        >>> cs = ClusterSpace(prim, cutoffs=[4.3], chemical_symbols=['Ag', 'Au'])
        >>> ce = ClusterExpansion(cs, [0, 0, 0.1, -0.02])

        >>> # set up and run MC simulation (T=600 K, delta_mu=0.8 eV/atom)
        >>> structure = prim.repeat(3)
        >>> calc = ClusterExpansionCalculator(structure, ce)
        >>> mc = SemiGrandCanonicalEnsemble(structure=structure, calculator=calc,
        ...                                temperature=600,
        ...                                dc_filename='myrun_sgc.dc',
        ...                                chemical_potentials={'Ag': 0, 'Au': 0.8})
        >>> mc.run(100)  # carry out 100 trial swaps

    """

    def __init__(self,
                 structure: Atoms,
                 calculator: BaseCalculator,
                 temperature: float,
                 chemical_potentials: Dict[str, float],
                 boltzmann_constant: float = kB,
                 user_tag: str = None,
                 random_seed: int = None,
                 dc_filename: str = None,
                 data_container: str = None,
                 data_container_write_period: float = 600,
                 ensemble_data_write_interval: int = None,
                 trajectory_write_interval: int = None,
                 sublattice_probabilities: List[float] = None) -> None:

        self._ensemble_parameters = dict(temperature=temperature)

        # add chemical potentials to ensemble parameters
        # TODO: add check that chemical symbols in chemical potentials are allowed
        self._chemical_potentials = get_chemical_potentials(chemical_potentials)
        for atnum, chempot in self.chemical_potentials.items():
            mu_sym = 'mu_{}'.format(chemical_symbols[atnum])
            self._ensemble_parameters[mu_sym] = chempot

        self._boltzmann_constant = boltzmann_constant

        super().__init__(
            structure=structure, calculator=calculator, user_tag=user_tag,
            random_seed=random_seed,
            dc_filename=dc_filename,
            data_container=data_container,
            data_container_class=DataContainer,
            data_container_write_period=data_container_write_period,
            ensemble_data_write_interval=ensemble_data_write_interval,
            trajectory_write_interval=trajectory_write_interval,
            boltzmann_constant=boltzmann_constant)

        if sublattice_probabilities is None:
            self._flip_sublattice_probabilities = self._get_flip_sublattice_probabilities()
        else:
            self._flip_sublattice_probabilities = sublattice_probabilities

    @property
    def temperature(self) -> float:
        """ temperature :math:`T` (see parameters section above) """
        return self.ensemble_parameters['temperature']

    def _do_trial_step(self):
        """ Carries out one Monte Carlo trial step. """
        sublattice_index = self.get_random_sublattice_index(
            probability_distribution=self._flip_sublattice_probabilities)
        return self.do_sgc_flip(self.chemical_potentials, sublattice_index=sublattice_index)

    @property
    def chemical_potentials(self) -> Dict[int, float]:
        """
        chemical potentials :math:`\\mu_i` (see parameters section above)
        """
        return self._chemical_potentials

    def _get_ensemble_data(self) -> Dict:
        """Returns the data associated with the ensemble. For the SGC
        ensemble this specifically includes the species counts.
        """
        # generic data
        data = super()._get_ensemble_data()

        # species counts
        data.update(self._get_species_counts())

        return data


def get_chemical_potentials(chemical_potentials: Union[Dict[str, float], Dict[int, float]]) \
        -> Dict[int, float]:
    """ Gets values of chemical potentials."""
    if not isinstance(chemical_potentials, dict):
        raise TypeError('chemical_potentials has the wrong type: {}'
                        .format(type(chemical_potentials)))

    cps = OrderedDict([(key, val) if isinstance(key, int)
                       else (atomic_numbers[key], val)
                       for key, val in chemical_potentials.items()])

    return cps
