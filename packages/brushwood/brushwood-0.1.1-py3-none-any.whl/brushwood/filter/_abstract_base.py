"""
Contains fundamental base filters from which implementation should inherit
"""

from abc import ABC, abstractmethod
from typing import List
from ..leaf import Leaf


class BaseFilter(ABC):
    """
    Mother of all filters

    Notes:
    ______
    Basically it's a pre-configureable function.

    There are 2 steps in which that works

    At the time of instanciation (so the __init__) method the parameters for the filter will be provided - like for
    example an attribute name and an attribute value which should be searched for. So the things the filter should
    actually filter for.
    This is the part the "end" user will face.

    On calling-time (when the filter is actually applied) the object will be called like a function and therefore
    the __call__ method will be addressed.
    That method will take the leaf on which the filter should be applied and applies it -> returning True or False
    depending on the filter matched (True - take the leaf into the results) or not (False - exclude the leaf from the
     results).
    This method will be called by another filter or the get_filtered_by method of Otree, so the user could not
    apply there/at the time configuration parameters.
    Therefore there is this 2 step approach.
    """

    @abstractmethod
    def __call__(self, leaf: Leaf):
        """
        Function call method

        Will be called when the object is being called as function to apply to a certain leaf.

        Parameters
        ----------
        leaf:Leaf : The leaf the filter should be applied to

        Returns
        -------
        Depending on filter type.
        Usually a list of True/False value or a single True/False value.
        """
        pass


class SingleResultFilter(BaseFilter):
    """Base class for all user-facing filters.

    When called returns True (filter passed, element should be in results) or False (element didn't match filter)
    """

    @abstractmethod
    def __call__(self, leaf: Leaf) -> bool:
        pass


class MultiResultFilter(SingleResultFilter):
    """
    Filters which return a list of results.
    The usually are the base for some other filter which return just one result -> so they are not intended to
    be used by the user directly
    """

    def __call__(self, leaf: Leaf) -> List[bool]:
        """

        Parameters
        ----------
        leaf:Leaf : The leaf to apply the filter on

        Returns
        -------
        List of bools.
        """
        pass
