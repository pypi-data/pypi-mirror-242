"""
Filter checking on certain conditions - basically everything not fitting somewhere else and is more or
 less self-contained
"""

from ._abstract_base import SingleResultFilter
from ..leaf import Leaf


class AttributeHasValue(SingleResultFilter):
    """Checks that the element has a certain attribute with a certain value

    The none-existence or wrong type of the attribute evaluates to False
    """

    def __init__(self, attribute, value, raise_exceptions: bool = False):
        """

        Parameters
        ----------
        attribute :
            Attribute to check for
        value :
            Value the attribute has to have
        raise_exceptions:bool, default=False:
            If set to False instead of raising AttributeError (if the attribute does not exist) or TypeError
             (if it's not the expected type) evaluate to False
        """
        self.attribute = attribute
        self.value = value
        self.raise_exceptions: bool = raise_exceptions

    def __call__(self, leaf: Leaf) -> bool:
        """
        Returns True if the leaf has the given attribute having the given value

        Parameters
        ----------
        leaf:Leaf :
            The leaf to be checked

        Returns
        -------
        bool
            Returns True if the leaf has the given attribute having the given value

        """
        try:
            return getattr(leaf, self.attribute) == self.value
        except (TypeError, AttributeError) as e:
            if self.raise_exceptions:
                raise
        return False


class Not(SingleResultFilter):
    """Negates the provided Filter

    Most filters check for a given condition, this filter negates those filter -> so the condition should not be given
    for the leaf to be in the result set.

    Example: NotFilter(attribute_has_value("flavor", "vanilla"))
    In this case the leaf will be returned if the flavor attribute is everything but "vanilla"
    """

    def __init__(self, filter: SingleResultFilter):
        """

        Parameters
        ----------
        filter:SingleResultFilter :
            Filter to be negated
        """
        self.filter = filter

    def __call__(self, leaf: Leaf):
        """
        Runs the (negated) filter for a given leaf

        Parameters
        ----------
        leaf:Leaf :
            Leaf to check

        Returns
        -------
        bool
            True if the actual filter returns False and False if the actual filter returns True
        """
        return not self.filter(leaf)
