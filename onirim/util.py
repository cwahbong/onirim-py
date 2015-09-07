"""
Util class here.
"""

import enum

class AutoNumberEnum(enum.Enum):
    """
    Create an auto numbered enumeration. Just define enumeration class as before
    but assign the values to an empty tuple.

    Example:
        The following defines a auto numbered enumeration class ``A`` with two
        values ``b`` and ``c``::

            class A(AutoNumberEnum):
                b = ()
                c = ()
    """

    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj
