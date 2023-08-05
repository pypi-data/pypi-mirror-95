#pragma once

#define _USE_MATH_DEFINES
#include <cmath>

#include "ClusterCounts.hpp"
#include "LocalOrbitListGenerator.hpp"
#include "OrbitList.hpp"
#include "PeriodicTable.hpp"
#include "Structure.hpp"
#include "VectorOperations.hpp"

/**
@brief This class handles the cluster space.
@details It provides functionality for setting up a cluster space, calculating cluster vectors as well as retrieving various types of associated information.
*/

class ClusterSpace
{
  public:
    /// Constructor.
    ClusterSpace() {};
    ClusterSpace(std::vector<std::vector<std::string>> &, const OrbitList &, const double, const double);

    /// Returns the cluster vector corresponding to the input structure.
    std::vector<double> getClusterVector(const Structure &, const double) const;

    /// Returns information concerning the association between orbits and multi-component vectors.
    std::pair<int, std::vector<int>> getMultiComponentVectorsByOrbit(const unsigned int);

    /// Returns the entire orbit list.
    OrbitList getOrbitList() const { return _orbitList; }

    /// Returns an orbit from the orbit list.
    Orbit getOrbit(const size_t index) const { return _orbitList.getOrbit(index); }

    /// Returns the native clusters.
    /// @todo What is a native cluster? Partial answer: clusters within the unit cell?
    ClusterCounts getNativeClusters(const Structure &structure) const;

    /// Returns the multi-component (MC) vector permutations for each MC vector in the set of input vectors.
    /// @todo Clean up this description.
    std::vector<std::vector<std::vector<int>>> getMultiComponentVectorPermutations(const std::vector<std::vector<int>> &, const int) const;

  public:

    /// Returns the cutoff for each order.
    std::vector<double> getCutoffs() const { return _clusterCutoffs; }

    /// Returns the primitive structure.
    Structure getPrimitiveStructure() const { return _primitiveStructure; }

    /// Returns the number of allowed components for each site.
    std::vector<int> getNumberOfAllowedSpeciesBySite(const Structure &, const std::vector<LatticeSite> &) const;

    /// Returns a list of species associated with cluster space as chemical symbols.
    std::vector<std::vector<std::string>> getChemicalSymbols() const { return _chemicalSymbols; }

    /// Returns the cluster space size, i.e. the length of a cluster vector.
    size_t getClusterSpaceSize() { return _multiComponentVectorsByOrbit.size(); }

    /// Returns the mapping between atomic numbers and the internal species enumeration scheme for each site.
    std::vector<std::unordered_map<int, int>> getSpeciesMaps() const { return _speciesMaps; }

    /// Primitive orbit list based on the structure and the global cutoffs
    /// @todo Make private.
    OrbitList _orbitList;

    /// Returns the cluster product.
    double evaluateClusterProduct(const std::vector<int> &, const std::vector<int> &, const std::vector<int> &, const std::vector<int>&) const;

    /// Returns the default cluster function.
    double evaluateClusterFunction(const int, const int, const int) const;

    /// Precomputed multicomponent vectors for each orbit in _orbitlist.
    /// @todo Make private.
    std::vector<std::vector<std::vector<int>>> _multiComponentVectors;

    /// Precomputed site permutations for each orbit in _orbitlist.
    /// @todo Make private.
    std::vector<std::vector<std::vector<std::vector<int>>>> _sitePermutations;

    /// Computes permutations and multicomponent vectors of each orbit.
    void computeMultiComponentVectors();

    /// Prunes the orbit list.
    void pruneOrbitList(std::vector<size_t> &);

    /// Primitive (prototype) structure.
    Structure _primitiveStructure;


  private:

    /// Multi-component vectors for each orbit. The first index (int)
    /// corresponds to the orbit index, the second index (vector of ints)
    /// refers to a multi-component vector.
    std::vector<std::pair<int, std::vector<int>>> _multiComponentVectorsByOrbit;


    /// Number of allowed components on each site of the primitive structure.
    std::vector<int> _numberOfAllowedSpeciesPerSite;

    /// Radial cutoffs by cluster order starting with pairs.
    std::vector<double> _clusterCutoffs;

    /// Species considered in this cluster space identified by atomic number.
    std::vector<int> _species;

    /// Map between atomic numbers and the internal species enumeration scheme for each site in the primitive structure.
    std::vector<std::unordered_map<int, int>> _speciesMaps;

    /// The allowed chemical symbols on each site in the primitive structure.
    std::vector<std::vector<std::string>> _chemicalSymbols;
};
