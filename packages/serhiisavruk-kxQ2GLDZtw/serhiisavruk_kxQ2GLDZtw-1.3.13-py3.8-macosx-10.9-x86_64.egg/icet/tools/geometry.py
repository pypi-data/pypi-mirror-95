import numpy as np
import spglib
from typing import List, Sequence, Tuple, TypeVar
from ase import Atoms
from ase.data import chemical_symbols
from icet.core.lattice_site import LatticeSite
from icet.core.structure import Structure

Vector = List[float]
T = TypeVar('T')


def get_scaled_positions(positions: np.ndarray,
                         cell: np.ndarray,
                         wrap: bool = True,
                         pbc: List[bool] = [True, True, True]) -> np.ndarray:
    """
    Returns the positions in reduced (or scaled) coordinates.

    Parameters
    ----------
    positions
        atomic positions in cartesian coordinates
    cell
        cell metric
    wrap
        if True, positions outside the unit cell will be wrapped into
        the cell in the directions with periodic boundary conditions
        such that the scaled coordinates are between zero and one.
    pbc
        periodic boundary conditions flags
    """

    fractional = np.linalg.solve(cell.T, positions.T).T

    if wrap:
        for i, periodic in enumerate(pbc):
            if periodic:
                # Yes, we need to do it twice.
                # See the scaled_positions.py test.
                fractional[:, i] %= 1.0
                fractional[:, i] %= 1.0

    return fractional


def get_primitive_structure(structure: Atoms,
                            no_idealize: bool = True,
                            to_primitive: bool = True,
                            symprec: float = 1e-5) -> Atoms:
    """
    Returns the primitive structure using spglib.

    Parameters
    ----------
    structure
        input atomic structure
    no_idealize
        if True lengths and angles are not idealized
    to_primitive
        convert to primitive structure
    symprec
        tolerance imposed when analyzing the symmetry using spglib
    """
    structure_copy = structure.copy()
    structure_as_tuple = ase_atoms_to_spglib_cell(structure_copy)

    ret = spglib.standardize_cell(
        structure_as_tuple, to_primitive=to_primitive,
        no_idealize=no_idealize, symprec=symprec)
    if ret is None:
        raise ValueError('spglib failed to find the primitive cell, maybe caused by large symprec.')
    lattice, scaled_positions, numbers = ret
    scaled_positions = [np.round(pos, 12) for pos in scaled_positions]
    structure_prim = Atoms(scaled_positions=scaled_positions,
                           numbers=numbers, cell=lattice, pbc=structure.pbc)
    structure_prim.wrap()

    return structure_prim


def get_fractional_positions_from_neighbor_list(
        structure: Structure, neighbor_list: List) -> List[Vector]:
    """
    Returns the fractional positions of the lattice sites in structure from
    a neighbor list.

    Parameters
    ----------
    structure
        input atomic structure
    neighbor_list
        list of lattice neighbors of the input structure
    """
    neighbor_positions = []
    fractional_positions = []
    lattice_site = LatticeSite(0, [0, 0, 0])

    for i in range(len(neighbor_list)):
        lattice_site.index = i
        position = structure.get_position(lattice_site)
        neighbor_positions.append(position)
        for neighbor in neighbor_list[i]:
            position = structure.get_position(neighbor)
            neighbor_positions.append(position)

    if len(neighbor_positions) > 0:
        fractional_positions = get_scaled_positions(
            np.array(neighbor_positions),
            structure.cell, wrap=False,
            pbc=structure.pbc)

    return fractional_positions


def get_position_from_lattice_site(structure: Atoms, lattice_site: LatticeSite):
    """
    Gets the corresponding position from the lattice site.

    Parameters
    ---------
    structure
        input atomic structure
    lattice_site
        specific lattice site of the input structure
    """
    return structure[lattice_site.index].position + \
        np.dot(lattice_site.unitcell_offset, structure.cell)


def fractional_to_cartesian(structure: Atoms,
                            frac_positions: List[Vector]) -> np.ndarray:
    """
    Turns fractional positions into cartesian positions.

    Parameters
    ----------
    structure
        input atomic structure
    frac_positions
        fractional positions
    """
    return np.dot(frac_positions, structure.cell)


def get_permutation(container: Sequence[T],
                    permutation: List[int]) -> Sequence[T]:
    """
    Returns the permuted version of container.
    """
    if len(permutation) != len(container):
        raise RuntimeError('Container and permutation'
                           ' not of same size {} != {}'.format(
                               len(container), len(permutation)))
    if len(set(permutation)) != len(permutation):
        raise Exception
    return [container[s] for s in permutation]


def ase_atoms_to_spglib_cell(structure: Atoms) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Returns a tuple of three components: cell metric, atomic positions, and
    atomic species of the input ASE Atoms object.
    """
    return (structure.cell, structure.get_scaled_positions(), structure.get_atomic_numbers())


def get_occupied_primitive_structure(structure: Atoms,
                                     allowed_species: List[List[str]],
                                     symprec: float) -> Tuple[Atoms, List[Tuple[str, ...]]]:
    """
    Returns an occupied primitive structure.
    Will put hydrogen on sublattice 1, Helium on sublattice 2 and
    so on

    Parameters
    ----------
    structure
        input structure
    allowed_species
        chemical symbols that are allowed on each site
    symprec
        tolerance imposed when analyzing the symmetry using spglib

    Todo
    ----
    simplify the revert back to unsorted symbols
    """
    if len(structure) != len(allowed_species):
        raise ValueError(
            'structure and chemical symbols need to be the same size.')
    sorted_symbols = sorted({tuple(sorted(s)) for s in allowed_species})

    decorated_primitive = structure.copy()
    for i, sym in enumerate(allowed_species):
        sublattice = sorted_symbols.index(tuple(sorted(sym))) + 1
        decorated_primitive[i].symbol = chemical_symbols[sublattice]

    decorated_primitive = get_primitive_structure(decorated_primitive, symprec=symprec)
    decorated_primitive.wrap()
    primitive_chemical_symbols: List[Tuple[str, ...]] = []
    for atom in decorated_primitive:
        sublattice = chemical_symbols.index(atom.symbol)
        primitive_chemical_symbols.append(sorted_symbols[sublattice - 1])

    for symbols in allowed_species:
        if tuple(sorted(symbols)) in primitive_chemical_symbols:
            index = primitive_chemical_symbols.index(tuple(sorted(symbols)))
            primitive_chemical_symbols[index] = symbols
    return decorated_primitive, primitive_chemical_symbols


def atomic_number_to_chemical_symbol(numbers: List[int]) -> List[str]:
    """Returns the chemical symbols equivalent to the input atomic
    numbers.

    Parameters
    ----------
    numbers
        atomic numbers
    """

    symbols = [chemical_symbols[number] for number in numbers]
    return symbols


def chemical_symbols_to_numbers(symbols: List[str]) -> List[int]:
    """Returns the atomic numbers equivalent to the input chemical
    symbols.

    Parameters
    ----------
    symbols
        chemical symbols
    """

    numbers = [chemical_symbols.index(symbols) for symbols in symbols]
    return numbers


def get_wyckoff_sites(structure: Atoms,
                      map_occupations: List[List[str]] = None,
                      symprec: float = 1e-5) -> List[str]:
    """Returns the Wyckoff symbols of the input structure. The Wyckoff
    sites are of general interest for symmetry analysis but can be
    especially useful when setting up, e.g., a
    :class:`SiteOccupancyObserver
    <mchammer.observers.SiteOccupancyObserver>`.
    The Wyckoff labels can be conveniently attached as an array to the
    structure object as demonstrated in the examples section below.

    By default the occupation of the sites is part of the symmetry
    analysis. If a chemically disordered structure is provided this
    will usually reduce the symmetry substantially. If one is
    interested in the symmetry of the underlying structure one can
    control how occupations are handled. To this end, one can provide
    the ``map_occupations`` keyword argument. The latter must be a
    list, each entry of which is a list of species that should be
    treated as indistinguishable. As a shortcut, if *all* species
    should be treated as indistinguishable one can provide an empty
    list. Examples that illustrate the usage of the keyword are given
    below.

    Parameters
    ----------
    structure
        input structure, note that the occupation of the sites is
        included in the symmetry analysis
    map_occupations
        each sublist in this list specifies a group of chemical
        species that shall be treated as indistinguishable for the
        purpose of the symmetry analysis
    symprec
        tolerance imposed when analyzing the symmetry using spglib

    Examples
    --------
    Wyckoff sites of a hexagonal-close packed structure::

        >>> from ase.build import bulk
        >>> structure = bulk('Ti')
        >>> wyckoff_sites = get_wyckoff_sites(structure)
        >>> print(wyckoff_sites)
        ['2d', '2d']


    The Wyckoff labels can also be attached as an array to the
    structure, in which case the information is also included when
    storing the Atoms object::

        >>> from ase.io import write
        >>> structure.new_array('wyckoff_sites', wyckoff_sites, str)
        >>> write('structure.xyz', structure)

    The function can also be applied to supercells::

        >>> structure = bulk('GaAs', crystalstructure='zincblende', a=3.0).repeat(2)
        >>> wyckoff_sites = get_wyckoff_sites(structure)
        >>> print(wyckoff_sites)
        ['4a', '4c', '4a', '4c', '4a', '4c', '4a', '4c',
         '4a', '4c', '4a', '4c', '4a', '4c', '4a', '4c']

    Now assume that one is given a supercell of a (Ga,Al)As
    alloy. Applying the function directly yields much lower symmetry
    since the symmetry of the original structure is broken::

        >>> structure.set_chemical_symbols(
        ...        ['Ga', 'As', 'Al', 'As', 'Ga', 'As', 'Al', 'As',
        ...         'Ga', 'As', 'Ga', 'As', 'Al', 'As', 'Ga', 'As'])
        >>> print(get_wyckoff_sites(structure))
        ['8g', '8i', '4e', '8i', '8g', '8i', '2c', '8i',
         '2d', '8i', '8g', '8i', '4e', '8i', '8g', '8i']

    Since Ga and Al occupy the same sublattice, they should, however,
    be treated as indistinguishable for the purpose of the symmetry
    analysis, which can be achieved via the ``map_occupations``
    keyword::

        >>> print(get_wyckoff_sites(structure, map_occupations=[['Ga', 'Al'], ['As']]))
        ['4a', '4c', '4a', '4c', '4a', '4c', '4a', '4c',
         '4a', '4c', '4a', '4c', '4a', '4c', '4a', '4c']

    If occupations are to ignored entirely, one can simply provide an
    empty list. In the present case, this turns the zincblende lattice
    into a diamond lattice, on which case there is only one Wyckoff
    site::

        >>> print(get_wyckoff_sites(structure, map_occupations=[]))
        ['8a', '8a', '8a', '8a', '8a', '8a', '8a', '8a',
         '8a', '8a', '8a', '8a', '8a', '8a', '8a', '8a']
    """
    structure_copy = structure.copy()
    if map_occupations is not None:
        if len(map_occupations) > 0:
            new_symbols = []
            for symb in structure_copy.get_chemical_symbols():
                for group in map_occupations:
                    if symb in group:
                        new_symbols.append(group[0])
                        break
        else:
            new_symbols = len(structure) * ['H']
        structure_copy.set_chemical_symbols(new_symbols)
    dataset = spglib.get_symmetry_dataset(ase_atoms_to_spglib_cell(structure_copy), symprec=symprec)
    n_unitcells = np.linalg.det(dataset['transformation_matrix'])

    equivalent_atoms = list(dataset['equivalent_atoms'])
    wyckoffs = {}
    for index in set(equivalent_atoms):
        multiplicity = list(dataset['equivalent_atoms']).count(index) / n_unitcells
        multiplicity = int(round(multiplicity))
        wyckoffs[index] = '{}{}'.format(multiplicity, dataset['wyckoffs'][index])

    return [wyckoffs[equivalent_atoms[a.index]] for a in structure_copy]
