"""
Tree object and related methods
"""

from __future__ import annotations
from typing import List
from .filter._abstract_base import SingleResultFilter
from .filter.grouping import All
from .leaf import Leaf
from ._dictloader import DictLoader


class Brushwood(DictLoader):
    """Tree"""

    def __init__(self):
        self.liststructure: List[Leaf] = []

    def append(self, leaf: Leaf):
        """
        Append a leaf to the tree

        Parameters
        ----------
        leaf:Leaf :
            Leaf to add
        """
        self.liststructure.append(leaf)

    def get_filtered_by(self, filter: List[SingleResultFilter]) -> Brushwood:
        """Returns a tree filtered by given filters

        All the filters need to pass for an element to be added to the tree

        Parameters
        ----------
        filter:List[SingleResultFilter] :

        Returns
        -------
        Otree:
            The filtered part of tree as Otree
        """
        newtree = Brushwood()

        for leaf in self.liststructure:
            groupfilter = All(filter)
            if groupfilter(leaf):
                newtree.liststructure.append(leaf)
        return newtree
