"""
This module provides the ClusterExpansion class.
"""

import pandas as pd
import numpy as np
import pickle
import tempfile
import tarfile
import re

from icet import ClusterSpace
from icet.core.structure import Structure
from typing import List, Union
from ase import Atoms


class ClusterExpansion:
    """Cluster expansions are obtained by combining a cluster space with a set
    of parameters, where the latter is commonly obtained by optimization.
    Instances of this class allow one to predict the property of interest for
    a given structure.

    **Note:** Each element of the parameter vector corresponds to an
    effective cluster interaction (ECI) multiplied by the multiplicity of the
    underlying orbit.

    Attributes
    ----------
    cluster_space : icet.ClusterSpace
        cluster space that was used for constructing the cluster expansion
    parameters : np.ndarray
        parameter vector

    Example
    -------
    The following snippet illustrates the initialization and usage of
    a ClusterExpansion object. Here, the parameters are taken to be a list
    of ones. Usually, they would be obtained by training with
    respect to a set of reference data::

       >>> from ase.build import bulk
       >>> from icet import ClusterSpace, ClusterExpansion

       >>> # create cluster expansion with fake parameters
       >>> prim = bulk('Au')
       >>> cs = ClusterSpace(prim, cutoffs=[7.0, 5.0],
       ...                   chemical_symbols=[['Au', 'Pd']])
       >>> parameters = len(cs) * [1.0]
       >>> ce = ClusterExpansion(cs, parameters)

       >>> # make prediction for supercell
       >>> sc = prim.repeat(3)
       >>> for k in [1, 4, 7]:
       >>>     sc[k].symbol = 'Pd'
       >>> print(ce.predict(sc))
    """

    def __init__(self, cluster_space: ClusterSpace, parameters: np.array,
                 metadata: dict = None) -> None:
        """
        Initializes a ClusterExpansion object.

        Parameters
        ----------
        cluster_space
            cluster space to be used for constructing the cluster expansion
        parameters
            parameter vector
        metadata : dict
            metadata dictionary, user-defined metadata to be stored together
            with cluster expansion. Will be pickled when CE is written to file.
            By default contains icet version, username, hostname and date.

        Raises
        ------
        ValueError
            if cluster space and parameters differ in length
        """
        if len(cluster_space) != len(parameters):
            raise ValueError('cluster_space ({}) and parameters ({}) must have'
                             ' the same length'.format(len(cluster_space), len(parameters)))
        self._cluster_space = cluster_space.copy()
        if isinstance(parameters, list):
            parameters = np.array(parameters)
        self._parameters = parameters

        # add metadata
        if metadata is None:
            metadata = dict()
        self._metadata = metadata
        self._add_default_metadata()

    def predict(self, structure: Union[Atoms, Structure]) -> float:
        """
        Predicts the property of interest (e.g., the energy) for the input
        structure using the cluster expansion.

        Parameters
        ----------
        structure
            atomic configuration

        Returns
        -------
        float
            property value of predicted by the cluster expansion
        """
        cluster_vector = self._cluster_space.get_cluster_vector(structure)
        prop = np.dot(cluster_vector, self.parameters)
        return prop

    def get_cluster_space_copy(self) -> ClusterSpace:
        """ Gets copy of cluster space on which cluster expansion is based """
        return self._cluster_space.copy()

    def to_dataframe(self) -> pd.DataFrame:
        """Returns representation of the cluster expansion in the form of a
        DataFrame containing orbit information and effective cluster interactions
        (ECIs)."""
        rows = self._cluster_space.orbit_data
        for row, param in zip(rows, self.parameters):
            row['parameter'] = param
            row['eci'] = param / row['multiplicity']
        return pd.DataFrame(rows)

    @property
    def orders(self) -> List[int]:
        """ orders included in cluster expansion """
        return list(range(len(self._cluster_space.cutoffs) + 2))

    @property
    def parameters(self) -> List[float]:
        """ parameter vector; each element of the parameter vector corresponds
        to an effective cluster interaction (ECI) multiplied by the
        multiplicity of the respective orbit """
        return self._parameters

    @property
    def metadata(self) -> dict:
        """ metadata associated with cluster expansion """
        return self._metadata

    @property
    def symprec(self) -> float:
        """ tolerance imposed when analyzing the symmetry using spglib
        (inherited from the underlying cluster space) """
        return self._cluster_space.symprec

    @property
    def position_tolerance(self) -> float:
        """ tolerance applied when comparing positions in Cartesian coordinates
        (inherited from the underlying cluster space) """
        return self._cluster_space.position_tolerance

    @property
    def fractional_position_tolerance(self) -> float:
        """ tolerance applied when comparing positions in fractional coordinates
        (inherited from the underlying cluster space) """
        return self._cluster_space.fractional_position_tolerance

    @property
    def primitive_structure(self) -> Atoms:
        """ primitive structure on which cluster expansion is based """
        return self._cluster_space.primitive_structure.copy()

    def plot_ecis(self, orders=None):
        """ Plot ECIs for given orders, default plots for all orders """

        if orders is None:
            orders = self.orders
        df = self.to_dataframe()

        # plotting
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.axhline(y=0.0, c='k', lw=1)
        for order in orders:
            df_order = df.loc[df['order'] == order]
            ax.plot(df_order.radius, df_order.eci, 'o', ms=8, label='order {}'.format(order))
        ax.legend(loc='best')
        ax.set_xlabel('Radius')
        ax.set_ylabel('ECI')
        plt.show()

    def __len__(self) -> int:
        return len(self._parameters)

    def _get_string_representation(self, print_threshold: int = None,
                                   print_minimum: int = 10):
        """ String representation of the cluster expansion. """
        cluster_space_repr = self._cluster_space._get_string_representation(
            print_threshold, print_minimum).split('\n')
        # rescale width
        par_col_width = max(len('{:9.3g}'.format(max(self._parameters, key=abs))), len('ECI'))
        width = len(cluster_space_repr[0]) + 2 * (len(' | ') + par_col_width)

        s = []  # type: List
        s += ['{s:=^{n}}'.format(s=' Cluster Expansion ', n=width)]
        s += [t for t in cluster_space_repr if re.search(':', t)]

        # additional information about number of nonzero parameters
        df = self.to_dataframe()
        orders = self.orders
        nzp_by_order = [np.count_nonzero(df[df.order == order].eci) for order in orders]
        assert sum(nzp_by_order) == np.count_nonzero(self.parameters)
        s += [' {:38} : {}'.format('total number of nonzero parameters', sum(nzp_by_order))]
        line = ' {:38} :'.format('number of nonzero parameters by order')
        for order, nzp in zip(orders, nzp_by_order):
            line += ' {}= {} '.format(order, nzp)
        s += [line]

        # table header
        s += [''.center(width, '-')]
        t = [t for t in cluster_space_repr if 'index' in t]
        t += ['{s:^{n}}'.format(s='parameter', n=par_col_width)]
        t += ['{s:^{n}}'.format(s='ECI', n=par_col_width)]
        s += [' | '.join(t)]
        s += [''.center(width, '-')]

        # table body
        index = 0
        while index < len(self):
            if (print_threshold is not None and
                    len(self) > print_threshold and
                    index >= print_minimum and
                    index <= len(self) - print_minimum):
                index = len(self) - print_minimum
                s += [' ...']
            pattern = r'^{:4}'.format(index)
            t = [t for t in cluster_space_repr if re.match(pattern, t)]
            parameter = self._parameters[index]
            t += ['{s:^{n}}'.format(s=f'{parameter:9.3g}', n=par_col_width)]
            eci = parameter / self._cluster_space.orbit_data[index]['multiplicity']
            t += ['{s:^{n}}'.format(s=f'{eci:9.3g}', n=par_col_width)]
            s += [' | '.join(t)]
            index += 1
        s += [''.center(width, '=')]

        return '\n'.join(s)

    def __repr__(self) -> str:
        """ string representation """
        return self._get_string_representation(print_threshold=50)

    def print_overview(self,
                       print_threshold: int = None,
                       print_minimum: int = 10) -> None:
        """
        Print an overview of the cluster expansion in terms of the orbits (order,
        radius, multiplicity, corresponding ECI etc).

        Parameters
        ----------
        print_threshold
            if the number of orbits exceeds this number print dots
        print_minimum
            number of lines printed from the top and the bottom of the orbit
            list if `print_threshold` is exceeded
        """
        print(self._get_string_representation(print_threshold=print_threshold,
                                              print_minimum=print_minimum))

    def prune(self, indices: List[int] = None, tol: float = 0) -> None:
        """
        Removes orbits from the cluster expansion (CE), for which the absolute
        values of the corresponding parameters are zero or close to zero. This
        commonly reduces the computational cost for evaluating the CE and is
        therefore recommended prior to using it in production. If the method
        is called without arguments orbits will be pruned, for which the ECIs
        are strictly zero. Less restrictive pruning can be achieved by setting
        the `tol` keyword.

        Parameters
        ----------
        indices
            indices of parameters to remove from the cluster expansion.
        tol
            all orbits will be pruned for which the absolute parameter value(s)
            is/are within this tolerance
        """

        # find orbit indices to be removed
        if indices is None:
            indices = [i for i, param in enumerate(
                self.parameters) if np.abs(param) <= tol and i > 0]
        df = self.to_dataframe()
        indices = list(set(indices))

        if 0 in indices:
            raise ValueError('Orbit index cannot be 0 since the zerolet may not be pruned.')
        orbit_candidates_for_removal = df.orbit_index[np.array(indices)].tolist()
        safe_to_remove_orbits, safe_to_remove_params = [], []
        for oi in set(orbit_candidates_for_removal):
            if oi == -1:
                continue
            orbit_count = df.orbit_index.tolist().count(oi)
            oi_remove_count = orbit_candidates_for_removal.count(oi)
            if orbit_count <= oi_remove_count:
                safe_to_remove_orbits.append(oi)
                safe_to_remove_params += df.index[df['orbit_index'] == oi].tolist()

        # prune cluster space
        self._cluster_space._prune_orbit_list(indices=safe_to_remove_orbits)
        self._parameters = self._parameters[np.setdiff1d(
            np.arange(len(self._parameters)), safe_to_remove_params)]
        assert len(self._parameters) == len(self._cluster_space)

    def write(self, filename: str) -> None:
        """
        Writes ClusterExpansion object to file.

        Parameters
        ---------
        filename
            name of file to which to write
        """
        self._cluster_space.write(filename)

        items = dict()
        items['parameters'] = self.parameters

        # TODO: remove if condition once metadata is firmly established
        if hasattr(self, '_metadata'):
            items['metadata'] = self._metadata

        with tarfile.open(name=filename, mode='w') as tar_file:
            cs_file = tempfile.NamedTemporaryFile()
            self._cluster_space.write(cs_file.name)
            tar_file.add(cs_file.name, arcname='cluster_space')

            # write items
            temp_file = tempfile.TemporaryFile()
            pickle.dump(items, temp_file)
            temp_file.seek(0)
            tar_info = tar_file.gettarinfo(arcname='items', fileobj=temp_file)
            tar_file.addfile(tar_info, temp_file)
            temp_file.close()

    @staticmethod
    def read(filename: str):
        """
        Reads ClusterExpansion object from file.

        Parameters
        ---------
        filename
            file from which to read
        """
        with tarfile.open(name=filename, mode='r') as tar_file:
            cs_file = tempfile.NamedTemporaryFile()
            cs_file.write(tar_file.extractfile('cluster_space').read())
            cs_file.seek(0)
            cs = ClusterSpace.read(cs_file.name)
            items = pickle.load(tar_file.extractfile('items'))

        ce = ClusterExpansion.__new__(ClusterExpansion)
        ce._cluster_space = cs
        ce._parameters = items['parameters']

        # TODO: remove if condition once metadata is firmly established
        if 'metadata' in items:
            ce._metadata = items['metadata']

        assert list(items['parameters']) == list(ce.parameters)
        return ce

    def _add_default_metadata(self):
        """Adds default metadata to metadata dict."""
        import getpass
        import socket
        from datetime import datetime
        from icet import __version__ as icet_version

        self._metadata['date_created'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self._metadata['username'] = getpass.getuser()
        self._metadata['hostname'] = socket.gethostname()
        self._metadata['icet_version'] = icet_version
