"""
Classes and functions related to a leaf.

Leaf being every object within the tree; A leaf could have leafs itself
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List, Union


@dataclass
class Leaf:
    """A leaf in the tree or a branch of it.

    Acts as wrapper around the actual object in the tree and contains some additional attributes.

    All the attributes of the actual object (the one the leaf represents) are directly possible by accessing the leaf.


    Notes
    _____

    The original object for which the leaf object is being created is stored in the element attribute.
    The reason is that additional attributes need to be stored to ease the processing of the tree, at the same time
    the original objects should not be changed - therefore the leaf container is being created.
    The leaf container contains the additional attributes (like parent, children, identifier), all accesses to
    attributes and methods of the original object are handed through the leaf object to the original object in element.
    This has been realized by modifying the __getattr__ method of the Leaf object.

    Example
    _______


    The following dict::
        {
            "type":"car"
            "engine":{
                        "power: electric"
                        "kW": 100
                    }
            power_source: {
                            "type": "battery"
                            "kWh": 80
            "color": "blue"
            "max_speed": "100"

    Will be a leaf object::
        Leaf:
            identifier = AttributName
            type = "car"
            color = "blue"
            max_speed = "100"
            children = [engine, power_source]
            parent = Leafobject_of_parent

    Added has been:

      * identifier -> The name is taken from the attribute name the object was stored in
      * parent -> Points to the parent leaf (representing the object the current one was part of)
      * children -> The List of children; As in this case all dicts are handled as separate object, power_source and
                    engine became children of the object and are stored in their own leaf objects
      * element -> stores the original object as it was

    All the other attributes of the object (like color, max_speed) and also all methods of it are directly accessible
    by leaf-object.attribute/ leaf-object.method as if the actual object in element would be accessed. All the
    operations to the attributes/methods are actually done to that object.
    """

    identifier: Any
    """The "name" of the object, usually taken from the attribute it was stored in"""
    element: Any
    """The actual original object"""
    children: List[Leaf]
    parent: Union[Leaf, None]
    handle_dict_keys_as_attrs = True
    """If element is a dict map attribute queries to getting the value from the key with same name"""

    def _getattr_dict(self, attr):
        """Work around for accessing attributes in case of element is a dict (-> in case of json relevant)"""
        try:
            return self.element.get(attr)
        except KeyError as e:
            raise AttributeError from e

    def __getattr__(self, attr):
        """
        Pass through for attribute access to self.element
        """
        if isinstance(self.element, dict):
            return self._getattr_dict(attr)

        return getattr(self.element, attr)
