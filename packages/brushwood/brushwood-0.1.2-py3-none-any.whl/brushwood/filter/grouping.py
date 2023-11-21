"""
Filters that group results
"""

from typing import List
from ._abstract_base import SingleResultFilter
from ..leaf import Leaf


class All(SingleResultFilter):
    """Checks that the provided list of filters all evaluate to True"""

    def __init__(self, filter: List[SingleResultFilter]):
        """

        Parameters
        ----------
        filter:List[SingleResultFilter] :
            List of Filters to check against
        """
        self.filter_list = filter

    def __call__(self, leaf: Leaf):
        """
        Checks that the provided list of filters all evaluate to True for the given Leaf

        Parameters
        ----------
        leaf:Leaf :
            Leaf to check

        Returns
        -------
        bool
            True if all filters evaluated to True, else False
        """
        for filter in self.filter_list:
            if not filter(leaf):
                return False
        return True


class Any(SingleResultFilter):
    """Checks that at least one of the provided filters evaluates to True

    Note
    ____
    Filtering will stop as soon as one filter evaluated to True.
    It makes sense to sort the provided filters by likelihood to match descending
    """

    def __init__(self, filter: List[SingleResultFilter]):
        """

        Parameters
        ----------
        filter:List[SingleResultFilter] :
            List of filters to check against
        """
        self.filter_list = filter

    def __call__(self, leaf: Leaf):
        """
        Checks if any of the given filters matches against the

        Parameters
        ----------
        leaf:Leaf :
            Leaf to check against

        Returns
        -------
        bool
            True if any filter evaluated to True, else False
        """
        for filter in self.filter_list:
            if filter(leaf):
                return True
        return False
