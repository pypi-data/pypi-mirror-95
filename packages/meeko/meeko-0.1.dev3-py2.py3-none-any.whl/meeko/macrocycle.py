#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Meeko macrocycle builder
#

import os
import sys
from collections import defaultdict
from operator import itemgetter

from openbabel import openbabel as ob

from .utils import obutils


class FlexMacrocycle:
    def __init__(self, min_ring_size=8, max_ring_size=10, force_double_bond=False, min_score=50):
        """Initialize macrocycle typer.
        
        Args:
            min_ring_size (int): minimum size of the ring (default: 8)
            max_ring_size (int): maximum size of the ring (default: 10)
            force_double_bond (bool): (default: False)
            min_score (int): minimum score (default: 50)

        """
        self._min_ring_size = min_ring_size
        self._max_ring_size = max_ring_size
        # accept also double bonds (if nothing better is found)
        self._force_double_bond = force_double_bond
        self._min_score = min_score

        self._mol = None
        self._accepted_rings = None
        self._conj_bond_list = None
        self._breakable = None

    def _collect_rings(self):
        """ retrieve rings and collect them by their size and properties"""
        self._accepted_rings = []
        for ring_id in list(self._mol.setup.rings.keys()):
            # aromatics
            if ring_id in self._mol.setup.rings_aromatic:
                continue
            # wrong size
            size = len(ring_id)
            if (size > self._max_ring_size) or (size < self._min_ring_size):
                #print("Wrong size [ %2d ]" % size, ring_id)
                continue
            # accepted
            self._accepted_rings.append(ring_id)
            #] = members

    def _detect_conj_bonds(self):
        """ detect bonds in conjugated systems
        """
        # TODO this should be removed once atom typing will be done
        self._conj_bond_list = []
        pattern = "[R0]=[R0]-[R0]=[R0]"
        found = self._mol.setup.smarts.find_pattern(pattern)
        if found is None:
            return
        for f in found:
            atom1 = self._mol.GetAtom(f[1])
            atom2 = self._mol.GetAtom(f[2])
            bond = self._mol.GetBond(atom1,atom2)
            self._conj_bond_list.append(bond.GetIdx())

    def _score_bond(self, atom_idx1, atom_idx2):
        """ provide a score for the likeness of the bond to be broken"""
        score = 100
        atom1 = self._mol.GetAtom(atom_idx1)
        atom2 = self._mol.GetAtom(atom_idx2)
        bond = self._mol.GetBond(atom1,atom2)
        # print("\nSCORE BOND: [%d, %d]" % (atom_idx1, atom_idx2))
        # test bond order
        bond_order = bond.GetBondOrder()
        if bond.IsAromatic():
            #print("-> [ X ] aromatic bond violation")
            return -1
        if (not bond_order == 1):
            # triple bond tolerated but not preferred (TODO true?)
            if bond_order == 3:
                score -= 30
                #print("-> [ - ] sp bond penalty")
            # double bond optionally accepted (but penalized)
            elif (bond_order == 2):
                if self._force_double_bond:
                    #print("-> [ - ] sp2 bond penalty")
                    score -= 50
                else:
                    #print("-> [ X ] sp2 violation")
                    # print("    => SCORE[%d]" % -1)
                    return -1
        if bond.GetIdx() in self._conj_bond_list:
            score -= 30
            # print("-> [ - ] conjugated bond penalty")
        # atom in more than one *flexible* ring are not acceptable
        # patch pre-botta
        # a_rings1 = set(self._mol.setup.ring_atom_to_ring[atom_idx1])
        # a_rings2 = set(self._mol.setup.ring_atom_to_ring[atom_idx2])
        a_rings1 = set(self._mol.setup.ring_atom_to_ring(atom_idx1))
        a_rings2 = set(self._mol.setup.ring_atom_to_ring(atom_idx2))
        if len(a_rings1 & a_rings2)>1:
            # PRE-BOTTA
            # v1, v2 = [self._mol.setup.ring_atom_to_ring[x] for x in atom_idx1, atom_idx2]
            v1, v2 = [self._mol.setup.ring_atom_to_ring(x) for x in (atom_idx1, atom_idx2)]
            v1 = ",".join([str(x) for x in v1])
            v2 = ",".join([str(x) for x in v2])
            #print("-> [ X ] multi-ring bond violation, (atom1 %d->%s rings | atom2 %d->%s rings)" % (atom_idx1, v1, atom_idx2, v2))
            #print("=> SCORE[%d]" % -1, "#")
            return -1
        # privilege carbon-carbon bonds (check this, with the new glue atoms we have no issues)
        if (not atom1.GetAtomicNum()==6) or (not atom2.GetAtomicNum()==6):
            score -= 20
            v1, v2 = atom1.GetAtomicNum(), atom2.GetAtomicNum()
            #print("-> [ - ] non-carbon penalty (%d, %d)" % (v1,v2))
        # discourage chiral atoms
        if atom1.IsChiral() or atom2.IsChiral():
            score -= 20
            v1, v2 = int(atom1.IsChiral()), int(atom2.IsChiral())
            #print("-> [ - ] chiral penalty (%d, %d)" % (v1,v2))
        #print("=> [%d] final score" % score)
        return score

    def _generate_closure_pseudo(self, bond_id):
        """ calculate position and parameters of the pseudoatoms for the closure"""
        closure_pseudo = []
        for idx in (0,1):
            target = bond_id[1 - idx]
            anchor = bond_id[0 - idx]
            coord = self._mol.setup.get_coord(target)
            closure_pseudo.append({
                'coord': coord,
                'anchor_list': [anchor],
                'charge': 0.0,
                'atom_type': 'G',
                'bond_type': 0,
                'rotatable': False})

        return closure_pseudo

    def _find_13_14_neighs(self, bond_id):
        """
        find 1-3 and 1-4 atom neighbors of atoms involved in the bond
        the parameters of these atoms will need to be adapted (softened)
        to simulate the conditions at closure
        """
        neighs = {}
        for idx in (0, 1):
            a_idx = bond_id[1 - idx]
            b_idx = bond_id[0 - idx]
            neigh_13 = []
            for n3 in self._mol.setup.graph[b_idx]:
                if n3 in bond_id:
                    continue
                neigh_13.append(n3)
            neigh_14 = []
            for n3 in neigh_13:
                for n4 in self._mol.setup.graph[n3]:
                    if n4 in bond_id:
                        continue
                    if n4 in neigh_13:
                        continue
                    neigh_14.append(n4)
            neighs[a_idx] = {'neigh_13': neigh_13, 'neigh_14': neigh_14}

        return neighs

    def _analyze_rings(self, verbose=False):
        """ find breaking points for rings
            following guidelines defined in [1]
            The optimal bond has the following properties:
            - does not involve a chiral atom
            - is not double/triple (?)
            - is between two carbons
            (preferably? we can now generate pseudoAtoms on the fly!)
            - is a bond present only in one ring

             [1] Forli, Botta, J. Chem. Inf. Model., 2007, 47 (4)
              DOI: 10.1021/ci700036j
        """
        self._breakable = self._mol.setup.ring_bond_breakable

        # look for breakable bonds in each ring
        for ring_members in self._accepted_rings:
            ring_size = len(ring_members)

            for idx in range(ring_size):
                atom_idx1 = ring_members[idx % ring_size]
                atom_idx2 = ring_members[(idx + 1) % ring_size]
                score = self._score_bond(atom_idx1, atom_idx2)

                if score > 0:
                    bond_id = self._mol.setup.get_bond_id(atom_idx1, atom_idx2)
                    closure_pseudo = self._generate_closure_pseudo(bond_id)
                    neigh_13_14 = self._find_13_14_neighs(bond_id)
                    self._breakable[bond_id] = {'score': score,
                                          'ring_id': ring_members,
                                          'closure_pseudo': closure_pseudo,
                                          'neigh_13_14': neigh_13_14,
                                          'active': False
                                          }

    def search_macrocycle(self, mol, verbose=False):
        """Search for macrocycle in the molecule
        
        Args:
            mol (OBMol): OBMol that was prepared with Meeko

        """
        self._accepted_rings = []
        self._conj_bond_list = []
        self._breakable = {}
        self._mol = mol

        self._collect_rings()
        self._detect_conj_bonds()
        self._analyze_rings(verbose)

    def show_macrocycle_scores(self):
        if self._mol is not None:
            print("\n==============[ MACROCYCLE SCORES ]================")
            bond_by_ring = defaultdict(list)

            for bond_id, data in list(self._mol.setup.ring_bond_breakable.items()):
                ring_id = data['ring_id']
                bond_by_ring[ring_id].append(bond_id)

            for ring_id, bonds in list(bond_by_ring.items()):
                data = []
                print("-----------[ ring id: %s | size: %2d ]-----------" % (",".join([str(x) for x in ring_id]), len(ring_id)))

                for b in bonds:
                    score = self._breakable[b]['score']
                    data.append((b, score))

                data = sorted(data, key=itemgetter(1), reverse=True)

                for b_count, b in enumerate(data):
                    bond = self._mol.GetBond(b[0][0], b[0][1])
                    begin = bond.GetBeginAtomIdx()
                    end = bond.GetEndAtomIdx()
                    info = (b_count, begin, end, b[1], "#" * int(b[1] / 5), "-" * int(20 - b[1] / 5))
                    print("[ %2d] Bond [%3d --%3d] s:%3d [%s%s]" % info)
