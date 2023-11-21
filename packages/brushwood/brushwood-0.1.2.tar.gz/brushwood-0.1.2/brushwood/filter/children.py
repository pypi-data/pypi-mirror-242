"""
Filters on the children of a leaf
"""

from __future__ import annotations
from abc import abstractmethod
from typing import Union
from ._abstract_base import SingleResultFilter
from ..leaf import Leaf


class AboveMaxLevelError(Exception):
    """The depth has reached the limit defined by max_level and no further levels will be checked"""

    pass


class BelowStartLevelError(Exception):
    """The current level is below start_level parameter and can't therefore be checked"""


class _BaseChildrenMatch(SingleResultFilter):
    """
    Base Class (all Classes applying filters to children should inherit from this)

    Runs the given filter against the children of the element

    Notes
    _____
     __call__ needs to implement calling run_filter_on_child and run_child_filter_for_child in a loop
     against every single children of the current leaf.
     run_filter_on_child runs the filter provided to the object against a child of the object - so runs the actual
     filter against one child
     run_child_filter_for_child runs a copy of the child-filter (so of me/the object itself) for one child, by that
     the grant-children of the leaf will be checked (as that will run_filter_on_child on the grant-child) and their
     children (as run_child_filter_for_child will be called for them) - so in the end the whole subtree is being
     checked
     Reason for the 2-step approach is that - depending on what the concrete filter should implement - it could make
     sense (be more efficient) to check first one or the other for all children or for each single children.
    """

    def __init__(
        self,
        filter: SingleResultFilter,
        start_level: int = 0,
        max_level: Union[int, None] = 0,
    ):
        """**Attention:** Read the hints for start_level and max_level carefully.

        Parameters
        ----------
        filter :
            Filter to be run
        start_level :
            relative level of children where to start the check - 0 are the children of the
            current level, 1 would be the children of the children.
            Check hints at max_level parameter.
        max_level :
            The level (including it) where to stop. None means check till the end of the tree.
            If there are less than max_levels this will NOT result in an error. In fact even if there are
            no children at all (and the filter could therefore not be applied) this results in True ->
            passing the leaf.
            If you need to have x levels of children present add min_level_children filter to check that
            explicitly -> and_filter(min_level_children(1), check_children(somefilter, 1, 5))
        filter: SingleResultFilter :
            A filter which the child elements need to match
        start_level:int, default=0
             The depth where to start applying the filter -> 0=direct children of the current leaf
        max_level:Union[int : None], default=0
             The depth (including that level) where to stop cheching children. 0 means children of the current leaf.
             0 would check the children of current leaf, but not traverse deeper checking the children's children
        """
        self.filter = filter

        if start_level < 0:
            raise ValueError(f"Parameter start_level below 0 - '{start_level}'")
        if max_level is not None and max_level < 0:
            raise ValueError(
                f"Parameter max_level below 0 - '{max_level}'. Can be None or positive int."
            )
        if max_level is not None and start_level > max_level:
            raise ValueError(
                f"Parameter start_level ({start_level}) > parameter max_level ({max_level}). Start level"
                f"will never be reached."
            )

        self.start_level = start_level
        self.max_level = max_level

    def run_filter_on_child(self, child_leaf: Leaf) -> bool:
        """
        Runs the (actual) filter for the given child-leaf

        Parameters
        ----------
        leaf :
            Child leaf to check

        Returns
        -------
        bool
            True if filter applied (leaf should be taken into results), False if not
        """

        if self.start_level > 0:
            raise BelowStartLevelError()

        return self.filter(child_leaf)

    def _get_childfilter_for_children(self) -> _BaseChildrenMatch:
        """
        Creates child filter for next level.

        Filter will be copied, max_level and start_level reduced by 1 -> as current checked level consumed one
        of the levels.

        Returns
        -------
        _BaseChildrenMatch
            A copy of the current filter's object's class with adjusted parameters
        """
        if hasattr(self, "_follow_child_filter"):
            return self._follow_child_filer

        assert self.max_level is not None and self.max_level < 1, (
            f"self.max_level < 1, it is '{self.max_level}'. Makes no sense to instantiate "
            f"a Child_filter for levels which will not be checked - this function should "
            f"not have been called"
        )

        start_level = self.start_level - 1 if self.start_level > 0 else 0
        max_level = (
            self.max_level
            if self.max_level is None or self.max_level == 0
            else self.max_level - 1
        )

        self._follow_child_filter = self.__class__(self.filter, start_level, max_level)
        return self._follow_child_filter

    def run_child_filter_for_child(self, child_leaf: Leaf) -> bool:
        """
        Runs the child filter (a copy of the current object) for a child leaf

        By doing so the (actual) filter will be applied to the children of the child leaf - the grant children
        of the current leaf.
        As the same will happen for the grant-childrens children the whole sub tree will have been checked at
        some point.

        Parameters
        ----------
        child_leaf:Leaf :
            Child leaf to check

        Returns
        -------
        bool:
            Depending on the result of the filter applied to the grand children (and their children)
        """
        if self.max_level is not None and self.max_level == 0:
            raise AboveMaxLevelError()

        next_level_children_filter = self._get_childfilter_for_children()
        return next_level_children_filter(child_leaf)

    @abstractmethod
    def __call__(self, leaf: Leaf) -> bool:
        """

        Parameters
        ----------
        leaf:Leaf
            The leaf to be checked

        Returns
        -------
        bool:
            True if the leaf should be taken into the result set, False if not
        """
        pass


class AllChildrenMatch(_BaseChildrenMatch):
    """True if the filter applies (returns True) on every child and their children (till the end of tree) of the leaf.

    Attention: If a level of children does not exist (even the first one to check) the filter will still return True.
    The existence needs to be assured by other means.
    """

    def __call__(self, leaf: Leaf) -> bool:
        """
        True if the filter applies (returns True) on every child and their children (till the end of tree) of the leaf.

        Parameters
        ----------
        leaf:Leaf :
            Leaf to be checked

        Returns
        -------
        bool
            True if for all the children (and their descents) the filter matched
        """
        for child_leaf in leaf.children:
            try:
                if not (
                    self.run_filter_on_child(child_leaf)
                    and self.run_child_filter_for_child(child_leaf)
                ):
                    return False
            except (AboveMaxLevelError, BelowStartLevelError):
                continue
        return True


class AnyChildrenMatch(_BaseChildrenMatch):
    """True if any descent, so also children of children, matches the provided filter

    The filtering will stop as soon as one child matches the filter
    """

    def __call__(self, leaf: Leaf) -> bool:
        """
        True if the filter applies (returns True) on any descent of the leaf

        Parameters
        ----------
        leaf:Leaf :
            Leaf to be checked

        Returns
        -------
        bool
            True if the filter applies (returns True) on any descent of the leaf. False if all descents have been
            checked and for none the filter matched
        """
        for child_leaf in leaf.children:
            try:
                if self.run_filter_on_child(
                    child_leaf
                ) or self.run_child_filter_for_child(child_leaf):
                    return True
            except (AboveMaxLevelError, BelowStartLevelError):
                continue
        return False
