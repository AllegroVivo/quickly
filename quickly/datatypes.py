# -*- coding: utf-8 -*-
#
# This file is part of `quickly`, a library for LilyPond and the `.ly` format
#
# Copyright © 2019-2022 by Wilbert Berendsen <info@wilbertberendsen.nl>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
Some generic datatypes used by quickly.

Too small to justify separate modules but too generic to be added to some
module where they are actually used.

"""
from __future__ import annotations

from collections.abc import Iterator
from typing import Any, Self


class Properties:
    """A dictionary-like object that accesses keys as attributes.

    Adding another Properties object returns a new Properties instance
    with updated dict contents. Example::

        >>> from quickly.datatypes import Properties
        >>> p = Properties(repeat_count=3)
        >>> p
        <Properties repeat_count=3>
        >>> p.repeat_count
        3
        >>> p1 = Properties(unfold=True)
        >>> p + p1
        <Properties repeat_count=3 unfold=True>
        >>> del p.repeat_count
        >>> p
        <Properties>

    Accessing a non-existent property name returns None. Deleting a
    non-existent property does not raise an AttributeError. Setting an
    attribute to None does keep the attribute, and when adding the properties
    to another, the same property in the other will be overwritten by the newer
    one that was set to None.

    Use :func:`vars` to get a dictionary view on the properties. Use ``"key" in
    props`` to see whether an attribute is really present. An empty Properties
    object evaluates to False.

    """
    def __init__(self, **kwargs: Any):
        self.__dict__.update(kwargs)

    def __bool__(self) -> bool:
        return bool(vars(self))

    def __repr__(self) -> str:
        def fields() -> Iterator[str]:
            yield type(self).__name__
            yield " ".join(("{}={}".format(
                name, repr(value)) for name, value in vars(self).items()))
        return "<{}>".format(" ".join(f for f in fields() if f))

    def __getattr__(self, name: str) -> Any:
        return None

    def __delattr__(self, name: str) -> None:
        try:
            del self.__dict__[name]
        except KeyError:
            pass

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Properties):
            return vars(self) == vars(other)
        return NotImplemented

    def __contains__(self, name: str) -> bool:
        return name in self.__dict__

    def __add__(self, other: Properties) -> Self:
        d = vars(self) | vars(other)
        return type(self)(**d)


