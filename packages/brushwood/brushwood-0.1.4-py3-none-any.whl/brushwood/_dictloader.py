"""
Functionality to create the tree from an interleaved dict-structure - such as json could be converted to
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Union, List, TYPE_CHECKING
from .leaf import Leaf

if TYPE_CHECKING:
    from brushwood import Otree


@dataclass
class ChildElementInfo:
    """
    Helper class
    """

    identifier: Any
    element: Any


def get_child_element_list(element: dict) -> List[ChildElementInfo]:
    """
    Returns the child elements (dicts) from within a given element (dict)

    Parameters
    ----------
    element: dict :
        Element of which the children should be returned

    Returns
    -------
    List:
        List of children elements
    """
    child_list = []
    for identifier, value in element.items():
        if isinstance(value, dict):
            child_list.append(ChildElementInfo(identifier, value))

    return child_list


def dict_create_leaf_structure(
    identifier: Any, element: dict, parent: Union[Leaf, None], tree: Otree
) -> Leaf:
    """
    Adds a (sub-) tree to the given tree object

    Parameters
    ----------
    identifier: Any:
        name of the first node. Give None if the first node has no identifier
    element dict:
        Interleaved dict object (so a dict wherein are also dicts being child elements)
    parent: Union[Leaf,None] :
        parent leaf of the provided element. For the root element its None
    tree: Otree :
        Tree object to which will be added

    Returns
    -------
    Leaf:
        Returns the Leaf object for the provided element (the top layer in the provided interleaved dict)
    """
    current_leaf = Leaf(
        identifier=identifier, element=element, children=[], parent=parent
    )
    tree.append(current_leaf)

    for sub_element in get_child_element_list(element):
        sub_leaf = dict_create_leaf_structure(
            identifier=sub_element.identifier,
            element=sub_element.element,
            parent=current_leaf,
            tree=tree,
        )
        current_leaf.children.append(sub_leaf)

    return current_leaf


class DictLoader:
    """Mixin for brushwood containing functionality to create the tree from interleaved dict structure - such as
    loaded json creates
    """

    liststructure: List[Leaf] = []

    @classmethod
    def create_from_dict(cls, dict_structure: dict) -> Otree:
        """
        Creates the tree from an interleaved dict

        Parameters
        ----------
        dict_structure:dict :
            Interleaved dict to create the tree from

        Returns
        -------
        Otree
            A Otree instance representing the data
        """
        newtree = cls()
        dict_create_leaf_structure(
            identifier=None, element=dict_structure, parent=None, tree=newtree
        )
        return newtree
