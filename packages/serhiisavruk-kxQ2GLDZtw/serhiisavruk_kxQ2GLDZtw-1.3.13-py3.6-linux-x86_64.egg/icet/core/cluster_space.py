"""
This module provides the ClusterSpace class.
"""

import copy
import itertools
import pickle
import tarfile
import tempfile
from collections import OrderedDict
from math import log10, floor
from typing import List, Union, Tuple

import numpy as np
import spglib

from _icet import ClusterSpace as _ClusterSpace
from ase import Atoms
from ase.io import read as ase_read
from ase.io import write as ase_write
from icet.core.orbit_list import OrbitList
from icet.core.structure import Structure
from icet.core.sublattices import Sublattices
from icet.tools.geometry import (ase_atoms_to_spglib_cell,
                                 get_occupied_primitive_structure,
                                 get_position_from_lattice_site)


class ClusterSpace(_ClusterSpace):
    """This class provides functionality for generating and maintaining
    cluster spaces.

    **Note:** In icet all :class:`ase.Atoms` objects must have
    periodic boundary conditions. When carrying out cluster expansions
    for surfaces and nanoparticles it is therefore recommended to
    surround the structure with vacuum and use periodic boundary
    conditions. This can be done using e.g., :func:`ase.Atoms.center`.

    Parameters
    ----------
    structure : ase.Atoms
        atomic structure
    cutoffs : list(float)
        cutoff radii per order that define the cluster space

        Cutoffs are specified in units of Angstrom and refer to the
        longest distance between two atoms in the cluster. The first
        element refers to pairs, the second to triplets, the third
        to quadruplets, and so on. ``cutoffs=[7.0, 4.5]`` thus implies
        that all pairs distanced 7 A or less will be included,
        as well as all triplets among which the longest distance is no
        longer than 4.5 A.
    chemical_symbols : list(str) or list(list(str))
        list of chemical symbols, each of which must map to an element
        of the periodic table

        If a list of chemical symbols is provided, all sites on the
        lattice will have the same allowed occupations as the input
        list.

        If a list of list of chemical symbols is provided then the
        outer list must be the same length as the `structure` object and
        ``chemical_symbols[i]`` will correspond to the allowed species
        on lattice site ``i``.
    symprec : float
        tolerance imposed when analyzing the symmetry using spglib
    position_tolerance : float
        tolerance applied when comparing positions in Cartesian coordinates

    Examples
    --------
    The following snippets illustrate several common situations::

        >>> from ase.build import bulk
        >>> from ase.io import read
        >>> from icet import ClusterSpace

        >>> # AgPd alloy with pairs up to 7.0 A and triplets up to 4.5 A
        >>> prim = bulk('Ag')
        >>> cs = ClusterSpace(structure=prim, cutoffs=[7.0, 4.5],
        ...                   chemical_symbols=[['Ag', 'Pd']])
        >>> print(cs)

        >>> # (Mg,Zn)O alloy on rocksalt lattice with pairs up to 8.0 A
        >>> prim = bulk('MgO', crystalstructure='rocksalt', a=6.0)
        >>> cs = ClusterSpace(structure=prim, cutoffs=[8.0],
        ...                   chemical_symbols=[['Mg', 'Zn'], ['O']])
        >>> print(cs)

        >>> # (Ga,Al)(As,Sb) alloy with pairs, triplets, and quadruplets
        >>> prim = bulk('GaAs', crystalstructure='zincblende', a=6.5)
        >>> cs = ClusterSpace(structure=prim, cutoffs=[7.0, 6.0, 5.0],
        ...                   chemical_symbols=[['Ga', 'Al'], ['As', 'Sb']])
        >>> print(cs)

        >>> # PdCuAu alloy with pairs and triplets
        >>> prim = bulk('Pd')
        >>> cs = ClusterSpace(structure=prim, cutoffs=[7.0, 5.0],
        ...                   chemical_symbols=[['Au', 'Cu', 'Pd']])
        >>> print(cs)

    """

    def __init__(self,
                 structure: Atoms,
                 cutoffs: List[float],
                 chemical_symbols: Union[List[str], List[List[str]]],
                 symprec: float = 1e-5,
                 position_tolerance: float = None) -> None:

        if not isinstance(structure, Atoms):
            raise TypeError('Input configuration must be an ASE Atoms object'
                            ', not type {}'.format(type(structure)))
        if not all(structure.pbc):
            raise ValueError('Input structure must have periodic boundary conditions')
        if symprec <= 0:
            raise ValueError('symprec must be a positive number')

        self._config = {'symprec': symprec}
        self._cutoffs = cutoffs.copy()
        self._input_structure = structure.copy()
        self._input_chemical_symbols = copy.deepcopy(chemical_symbols)
        chemical_symbols = self._get_chemical_symbols()

        self._pruning_history = []

        # set up primitive
        occupied_primitive, primitive_chemical_symbols = get_occupied_primitive_structure(
            self._input_structure, chemical_symbols, symprec=self.symprec)
        self._primitive_chemical_symbols = primitive_chemical_symbols
        assert len(occupied_primitive) == len(primitive_chemical_symbols)

        # derived tolerances
        if position_tolerance is None:
            self._config['position_tolerance'] = symprec
        else:
            if position_tolerance <= 0:
                raise ValueError('position_tolerance must be a positive number')
            self._config['position_tolerance'] = position_tolerance
        effective_box_size = abs(np.linalg.det(occupied_primitive.cell)) ** (1 / 3)
        tol = self.position_tolerance / effective_box_size
        tol = min(tol, self._config['position_tolerance'] / 5)
        self._config['fractional_position_tolerance'] = round(tol, -int(floor(log10(abs(tol)))))

        # set up orbit list
        self._orbit_list = OrbitList(
            structure=occupied_primitive,
            cutoffs=self._cutoffs,
            symprec=self.symprec,
            position_tolerance=self.position_tolerance,
            fractional_position_tolerance=self.fractional_position_tolerance)
        self._orbit_list.remove_inactive_orbits(primitive_chemical_symbols)

        # call (base) C++ constructor
        _ClusterSpace.__init__(self,
                               chemical_symbols=primitive_chemical_symbols,
                               orbit_list=self._orbit_list,
                               position_tolerance=self.position_tolerance,
                               fractional_position_tolerance=self.fractional_position_tolerance)

    def _get_chemical_symbols(self):
        """ Returns chemical symbols using input structure and
        chemical symbols. Carries out multiple sanity checks. """

        # setup chemical symbols as List[List[str]]
        if all(isinstance(i, str) for i in self._input_chemical_symbols):
            chemical_symbols = [
                self._input_chemical_symbols] * len(self._input_structure)
        elif not all(isinstance(i, list) for i in self._input_chemical_symbols):
            raise TypeError("chemical_symbols must be List[str] or List[List[str]], not {}".format(
                type(self._input_chemical_symbols)))
        elif len(self._input_chemical_symbols) != len(self._input_structure):
            msg = 'chemical_symbols must have same length as structure. '
            msg += 'len(chemical_symbols) = {}, len(structure)= {}'.format(
                len(self._input_chemical_symbols), len(self._input_structure))
            raise ValueError(msg)
        else:
            chemical_symbols = copy.deepcopy(self._input_chemical_symbols)

        for i, symbols in enumerate(chemical_symbols):
            if len(symbols) != len(set(symbols)):
                raise ValueError(
                    'Found duplicates of allowed chemical symbols on site {}.'
                    ' allowed species on  site {}= {}'.format(i, i, symbols))

        if len([tuple(sorted(s)) for s in chemical_symbols if len(s) > 1]) == 0:
            raise ValueError('No active sites found')

        return chemical_symbols

    def _get_chemical_symbol_representation(self):
        """Returns a str version of the chemical symbols that is
        easier on the eyes.
        """
        sublattices = self.get_sublattices(self.primitive_structure)
        nice_str = []
        for sublattice in sublattices.active_sublattices:
            sublattice_symbol = sublattice.symbol

            nice_str.append('{} (sublattice {})'.format(
                list(sublattice.chemical_symbols), sublattice_symbol))
        return ', '.join(nice_str)

    def _get_string_representation(self,
                                   print_threshold: int = None,
                                   print_minimum: int = 10) -> str:
        """
        String representation of the cluster space that provides an overview of
        the orbits (order, radius, multiplicity etc) that constitute the space.

        Parameters
        ----------
        print_threshold
            if the number of orbits exceeds this number print dots
        print_minimum
            number of lines printed from the top and the bottom of the orbit
            list if `print_threshold` is exceeded

        Returns
        -------
        multi-line string
            string representation of the cluster space.
        """

        def repr_orbit(orbit, header=False):
            formats = {'order': '{:2}',
                       'radius': '{:8.4f}',
                       'multiplicity': '{:4}',
                       'index': '{:4}',
                       'orbit_index': '{:4}',
                       'multi_component_vector': '{:}',
                       'sublattices': '{:}'}
            s = []
            for name, value in orbit.items():
                str_repr = formats[name].format(value)
                n = max(len(name), len(str_repr))
                if header:
                    s += ['{s:^{n}}'.format(s=name, n=n)]
                else:
                    s += ['{s:^{n}}'.format(s=str_repr, n=n)]
            return ' | '.join(s)

        # basic information
        # (use largest orbit to obtain maximum line length)
        prototype_orbit = self.orbit_data[-1]
        width = len(repr_orbit(prototype_orbit))
        s = []  # type: List
        s += ['{s:=^{n}}'.format(s=' Cluster Space ', n=width)]
        s += [' {:38} : {}'.format('space group', self.space_group)]
        s += [' {:38} : {}'
              .format('chemical species', self._get_chemical_symbol_representation())]
        s += [' {:38} : {}'.format('cutoffs', ' '
                                   .join(['{:.4f}'.format(co) for co in self._cutoffs]))]
        s += [' {:38} : {}'.format('total number of parameters', len(self))]
        t = ['{}= {}'.format(k, c)
             for k, c in self.get_number_of_orbits_by_order().items()]
        s += [' {:38} : {}'.format('number of parameters by order', '  '.join(t))]
        for key, value in sorted(self._config.items()):
            s += [' {:38} : {}'.format(key, value)]

        # table header
        s += [''.center(width, '-')]
        s += [repr_orbit(prototype_orbit, header=True)]
        s += [''.center(width, '-')]

        # table body
        index = 0
        orbit_list_info = self.orbit_data
        while index < len(orbit_list_info):
            if (print_threshold is not None and
                    len(self) > print_threshold and
                    index >= print_minimum and
                    index <= len(self) - print_minimum):
                index = len(self) - print_minimum
                s += [' ...']
            s += [repr_orbit(orbit_list_info[index])]
            index += 1
        s += [''.center(width, '=')]

        return '\n'.join(s)

    def __repr__(self) -> str:
        """ String representation. """
        return self._get_string_representation(print_threshold=50)

    def print_overview(self,
                       print_threshold: int = None,
                       print_minimum: int = 10) -> None:
        """
        Print an overview of the cluster space in terms of the orbits (order,
        radius, multiplicity etc).

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

    @property
    def symprec(self) -> float:
        """ tolerance imposed when analyzing the symmetry using spglib """
        return self._config['symprec']

    @property
    def position_tolerance(self) -> float:
        """ tolerance applied when comparing positions in Cartesian coordinates """
        return self._config['position_tolerance']

    @property
    def fractional_position_tolerance(self) -> float:
        """ tolerance applied when comparing positions in fractional coordinates """
        return self._config['fractional_position_tolerance']

    @property
    def space_group(self) -> str:
        """ space group of the primitive structure in international notion (via spglib) """
        structure_as_tuple = ase_atoms_to_spglib_cell(self.primitive_structure)
        return spglib.get_spacegroup(structure_as_tuple, symprec=self._config['symprec'])

    @property
    def orbit_data(self) -> List[OrderedDict]:
        """
        list of orbits with information regarding
        order, radius, multiplicity etc
        """
        data = []
        zerolet = OrderedDict([('index', 0),
                               ('order', 0),
                               ('radius', 0),
                               ('multiplicity', 1),
                               ('orbit_index', -1),
                               ('multi_component_vector', '.'),
                               ('sublattices', '.')])
        sublattices = self.get_sublattices(self.primitive_structure)
        data.append(zerolet)
        index = 1
        while index < len(self):
            multi_component_vectors_by_orbit = self.get_multi_component_vectors_by_orbit(index)
            orbit_index = multi_component_vectors_by_orbit[0]
            mc_vector = multi_component_vectors_by_orbit[1]
            orbit = self.get_orbit(orbit_index)
            repr_sites = orbit.sites_of_representative_cluster
            orbit_sublattices = '-'.join(
                [sublattices[sublattices.get_sublattice_index(ls.index)].symbol
                 for ls in repr_sites])
            local_Mi = self.get_number_of_allowed_species_by_site(
                self._get_primitive_structure(), orbit.sites_of_representative_cluster)
            mc_vectors = orbit.get_mc_vectors(local_Mi)
            mc_permutations = self.get_multi_component_vector_permutations(
                mc_vectors, orbit_index)
            mc_index = mc_vectors.index(mc_vector)
            mc_permutations_multiplicity = len(mc_permutations[mc_index])
            cluster = self.get_orbit(orbit_index).representative_cluster

            multiplicity = len(self.get_orbit(
                orbit_index).equivalent_clusters)
            record = OrderedDict([('index', index),
                                  ('order', cluster.order),
                                  ('radius', cluster.radius),
                                  ('multiplicity', multiplicity *
                                   mc_permutations_multiplicity),
                                  ('orbit_index', orbit_index)])
            record['multi_component_vector'] = mc_vector
            record['sublattices'] = orbit_sublattices
            data.append(record)
            index += 1
        return data

    def get_number_of_orbits_by_order(self) -> OrderedDict:
        """
        Returns the number of orbits by order.

        Returns
        -------
        an ordered dictionary where keys and values represent order and number
        of orbits, respectively
        """
        count_orbits = {}  # type: dict[int, int]
        for orbit in self.orbit_data:
            k = orbit['order']
            count_orbits[k] = count_orbits.get(k, 0) + 1
        return OrderedDict(sorted(count_orbits.items()))

    def get_cluster_vector(self, structure: Atoms) -> np.ndarray:
        """
        Returns the cluster vector for a structure.

        Parameters
        ----------
        structure
            atomic configuration

        Returns
        -------
        the cluster vector
        """
        if not isinstance(structure, Atoms):
            raise TypeError('Input structure must be an ASE Atoms object')

        try:
            cv = _ClusterSpace.get_cluster_vector(
                self,
                structure=Structure.from_atoms(structure),
                fractional_position_tolerance=self.fractional_position_tolerance)
        except Exception as e:
            self.assert_structure_compatibility(structure)
            raise(e)
        return cv

    def get_coordinates_of_representative_cluster(self, orbit_index: int) -> List[Tuple[float]]:
        """
        Returns the positions of atoms in the selected orbit

        Parameters
        ----------
        orbit_index
            index of the orbit from which to calculate the positions of the atoms

        Returns
        -------
        list of positions of atoms in the selected orbit

        """
        # Raise exception if chosen orbit index not in current list of orbit indices
        if not (orbit_index in range(len(self._orbit_list))):
            raise ValueError('The input orbit index is not in the list of possible values.')

        lattice_sites = self._orbit_list.get_orbit(orbit_index).sites_of_representative_cluster
        positions = []

        for site in lattice_sites:
            pos = get_position_from_lattice_site(structure=self.primitive_structure,
                                                 lattice_site=site)
            positions.append(pos)

        return positions

    def _prune_orbit_list(self, indices: List[int]) -> None:
        """
        Prunes the internal orbit list

        Parameters
        ----------
        indices
            indices to all orbits to be removed
        """
        size_before = len(self._orbit_list)

        self._prune_orbit_list_cpp(indices)
        for index in sorted(indices, reverse=True):
            self._orbit_list.remove_orbit(index)
        self._compute_multi_component_vectors()

        size_after = len(self._orbit_list)
        assert size_before - len(indices) == size_after
        self._pruning_history.append(indices)

    @property
    def primitive_structure(self) -> Atoms:
        """ Primitive structure on which cluster space is based """
        structure = self._get_primitive_structure().to_atoms()
        # Decorate with the "real" symbols (instead of H, He, Li etc)
        for atom, symbols in zip(structure, self._primitive_chemical_symbols):
            atom.symbol = min(symbols)
        return structure

    @property
    def chemical_symbols(self) -> List[List[str]]:
        """ Species identified by their chemical symbols """
        return self._primitive_chemical_symbols.copy()

    @property
    def cutoffs(self) -> List[float]:
        """
        Cutoffs for different n-body clusters. The cutoff radius (in
        Angstroms) defines the largest interatomic distance in a
        cluster.
        """
        return self._cutoffs

    @property
    def orbit_list(self):
        """Orbit list that defines the cluster in the cluster space"""
        return self._orbit_list

    def get_possible_orbit_occupations(self, orbit_index: int) \
            -> List[List[str]]:
        """Returns possible occupation of the orbit.

        Parameters
        ----------
        orbit_index
        """
        orbit = self.orbit_list.orbits[orbit_index]

        indices = [
            lattice_site.index for lattice_site in orbit.sites_of_representative_cluster]

        allowed_species = [self.chemical_symbols[index] for index in indices]

        return list(itertools.product(*allowed_species))

    def get_sublattices(self, structure: Atoms) -> Sublattices:
        """
        Returns the sublattices of the input structure.

        Parameters
        ----------
        structure
            structure the sublattices are based on
        """
        sl = Sublattices(self.chemical_symbols,
                         self.primitive_structure,
                         structure,
                         fractional_position_tolerance=self.fractional_position_tolerance)
        return sl

    def assert_structure_compatibility(self, structure: Atoms, vol_tol: float = 1e-5) -> None:
        """ Raises error if structure is not compatible with ClusterSpace.

        Todo
        ----
        Add check for if structure is relaxed.

        Parameters
        ----------
        structure
            structure to check if compatible with ClusterSpace
        """
        # check volume
        prim = self.primitive_structure
        vol1 = prim.get_volume() / len(prim)
        vol2 = structure.get_volume() / len(structure)
        if abs(vol1 - vol2) > vol_tol:
            raise ValueError('Volume per atom of structure does not match the volume of '
                             'ClusterSpace.primitive_structure')

        # check occupations
        sublattices = self.get_sublattices(structure)
        sublattices.assert_occupation_is_allowed(structure.get_chemical_symbols())

        # check pbc
        if not all(structure.pbc):
            raise ValueError('Input structure must have periodic boundary conditions')

    def is_supercell_self_interacting(self, structure: Atoms) -> bool:
        """
        Checks whether an structure has self-interactions via periodic
        boundary conditions.

        Parameters
        ----------
        structure
            structure to be tested

        Returns
        -------
        bool
            If True, the structure contains self-interactions via periodic
            boundary conditions, otherwise False.
        """
        ol = self.orbit_list.get_supercell_orbit_list(
            structure=structure,
            fractional_position_tolerance=self.fractional_position_tolerance)
        orbit_indices = set()
        for orbit in ol.orbits:
            for sites in orbit.equivalent_clusters:
                indices = tuple(sorted([site.index for site in sites]))
                if indices in orbit_indices:
                    return True
                else:
                    orbit_indices.add(indices)
        return False

    def write(self, filename: str) -> None:
        """
        Saves cluster space to a file.

        Parameters
        ---------
        filename
            name of file to which to write
        """

        with tarfile.open(name=filename, mode='w') as tar_file:

            # write items
            items = dict(cutoffs=self._cutoffs,
                         chemical_symbols=self._input_chemical_symbols,
                         pruning_history=self._pruning_history,
                         symprec=self.symprec,
                         position_tolerance=self.position_tolerance)
            temp_file = tempfile.TemporaryFile()
            pickle.dump(items, temp_file)
            temp_file.seek(0)
            tar_info = tar_file.gettarinfo(arcname='items', fileobj=temp_file)
            tar_file.addfile(tar_info, temp_file)
            temp_file.close()

            # write structure
            temp_file = tempfile.NamedTemporaryFile()
            ase_write(temp_file.name, self._input_structure, format='json')
            temp_file.seek(0)
            tar_info = tar_file.gettarinfo(arcname='atoms', fileobj=temp_file)
            tar_file.addfile(tar_info, temp_file)
            temp_file.close()

    @staticmethod
    def read(filename: str):
        """
        Reads cluster space from filename.

        Parameters
        ---------
        filename
            name of file from which to read cluster space
        """
        if isinstance(filename, str):
            tar_file = tarfile.open(mode='r', name=filename)
        else:
            tar_file = tarfile.open(mode='r', fileobj=filename)

        # read items
        items = pickle.load(tar_file.extractfile('items'))

        # read structure
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(tar_file.extractfile('atoms').read())
        temp_file.seek(0)
        structure = ase_read(temp_file.name, format='json')

        tar_file.close()

        # ensure backward compatibility
        if 'symprec' not in items:  # pragma: no cover
            items['symprec'] = 1e-5
        if 'position_tolerance' not in items:  # pragma: no cover
            items['position_tolerance'] = items['symprec']

        cs = ClusterSpace(structure=structure,
                          cutoffs=items['cutoffs'],
                          chemical_symbols=items['chemical_symbols'],
                          symprec=items['symprec'],
                          position_tolerance=items['position_tolerance'])
        for indices in items['pruning_history']:
            cs._prune_orbit_list(indices)
        return cs

    def copy(self):
        """ Returns copy of ClusterSpace instance. """
        cs_copy = ClusterSpace(structure=self._input_structure,
                               cutoffs=self.cutoffs,
                               chemical_symbols=self._input_chemical_symbols,
                               symprec=self.symprec,
                               position_tolerance=self.position_tolerance)
        for indices in self._pruning_history:
            cs_copy._prune_orbit_list(indices)
        return cs_copy
