from typing import Dict, List

import pandas as pd

from _icet import ClusterCounts as _ClusterCounts
from ase import Atoms
from icet.core.cluster import Cluster
from icet.core.local_orbit_list_generator import LocalOrbitListGenerator
from icet.core.orbit import Orbit
from icet.core.structure import Structure
from mchammer.observers.base_observer import BaseObserver
import copy


class ClusterCountObserver(BaseObserver):
    """
    This class represents a cluster count observer.

    A cluster count observer enables one to keep track of the
    occupation of clusters along the trajectory sampled by a Monte
    Carlo (MC) simulation. For example, using this observer, several
    canonical MC simulations could be carried out at different
    temperatures and the temperature dependence of the number of
    nearest neigbhors of a particular species could be accessed with
    this observer.

    Parameters
    ----------
    cluster_space : icet.ClusterSpace
     cluster space to define the clusters to be counted
    structure : ase.Atoms
        defines the lattice that the observer will work on
    interval : int
        observation interval during the Monte Carlo simulation
    max_orbit : int
        only include orbits up to the orbit with this index
        (default is to include all orbits)

    Attributes
    ----------
    tag : str
        human readable observer name
    interval : int
        the observation interval, defaults to None meaning that if the
        observer is used in a Monte Carlo simulation, then the Ensemble object
        will set the interval.
    """

    def __init__(self, cluster_space, structure: Atoms,
                 interval: int = None,
                 max_orbit: int = None) -> None:
        super().__init__(interval=interval, return_type=dict, tag='ClusterCountObserver')

        self._cluster_space = cluster_space
        local_orbit_list_generator = LocalOrbitListGenerator(
            orbit_list=cluster_space.orbit_list,
            structure=Structure.from_atoms(structure),
            fractional_position_tolerance=cluster_space.fractional_position_tolerance)

        self._full_orbit_list = local_orbit_list_generator.generate_full_orbit_list()
        self._cluster_counts_cpp = _ClusterCounts()

        if max_orbit is None:
            self._max_orbit = len(self._full_orbit_list)
        else:
            self._max_orbit = max_orbit

        self._cluster_keys = []  # type: List[Orbit]
        for i, orbit in enumerate(self._full_orbit_list.orbits):
            cluster = orbit.representative_cluster
            cluster.tag = i
            self._cluster_keys.append(cluster)

        self._empty_counts = self._get_empty_counts()

    def _get_empty_counts(self) -> Dict[Cluster, Dict[List[str], int]]:
        """ Returns the object which will be filled with counts. """
        counts = {}
        for i, cluster in enumerate(self._cluster_keys):
            order = len(cluster)
            possible_occupations = self._cluster_space.get_possible_orbit_occupations(cluster.tag)
            assert order == len(possible_occupations[0]), '{} is not {}, {}'.format(
                order, len(possible_occupations[0]), possible_occupations)

            counts[cluster] = {occupation: 0 for occupation in possible_occupations}
        return counts

    def _generate_counts(self, structure: Atoms) -> None:
        """Counts the occurrence of different clusters and stores this
        information in a pandas dataframe.

        Parameters
        ----------
        structure
            input atomic structure.
        """
        self._cluster_counts_cpp.count_orbit_list(Structure.from_atoms(structure),
                                                  self._full_orbit_list, True, True,
                                                  self._max_orbit)

        # Getting the empty counts sometimes constitutes a large part of the total time.
        # Thus copy a previously constructed dictionary.
        # Since Cluster is not picklable, we need to do a slightly awkward manual copy.
        empty_counts = {cluster: copy.deepcopy(item)
                        for cluster, item in self._empty_counts.items()}
        pandas_rows = []

        # std::unordered_map<Cluster, std::map<std::vector<int>, int>>
        cluster_counts = self._cluster_counts_cpp.get_cluster_counts()

        for cluster_key, chemical_number_counts_dict in cluster_counts.items():

            for chemical_symbols in empty_counts[cluster_key].keys():

                count = chemical_number_counts_dict.get(chemical_symbols, 0)
                pandas_row = {}
                pandas_row['dc_tag'] = '{}_{}'.format(cluster_key.tag, '_'.join(chemical_symbols))
                pandas_row['occupation'] = chemical_symbols
                pandas_row['cluster_count'] = count
                pandas_row['orbit_index'] = cluster_key.tag
                pandas_row['order'] = len(cluster_key)
                pandas_row['radius'] = cluster_key.radius
                pandas_rows.append(pandas_row)
        self.count_frame = pd.DataFrame(pandas_rows)
        self._cluster_counts_cpp.reset()

    def get_observable(self, structure: Atoms) -> dict:
        """
        Returns the value of the property from a cluster expansion model
        for a given atomic configuration.

        Parameters
        ----------
        structure
            input atomic structure
        """
        self._generate_counts(structure)

        count_dict = {row['dc_tag']: row['cluster_count']
                      for i, row in self.count_frame.iterrows()}
        return count_dict
