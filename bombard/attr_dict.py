"""
Dict with access to keys as attributes.

>>> d = AttrDict({'a': 'b', 'c': 'g'})
>>> d.c
'g'

Instance can be used as callable to set value to the dict
>>> d = AttrDict({})
>>> d(k='t')
>>> d.k
't'

(!) All values that you set will be repeated to `master` that you used to init the object.
>>> master = {'j': 'l'}
>>> d = AttrDict(master)
>>> d(h='q')
>>> master['h']
'q'
>>> d['w'] = 'e'
>>> master['w']
'e'

And it works without master
>>> d = AttrDict()
>>> d(f=7)
>>> d.f
7

"""

from typing import Any


class AttrDict(dict[str, Any]):
    """
    You can access all dict values as attributes.
    All changes immediately repeated in master_dict.
    """

    def __call__(self, **kwargs: Any) -> None:
        for name, val in kwargs.items():
            self[name] = val

    def __init__(self, master_dict: dict[str, Any] | None = None, **kwargs: Any) -> None:
        if master_dict is None:
            super().__init__(**kwargs)
        else:
            super().__init__(master_dict, **kwargs)
        self.__dict__ = self
        self.master_dict = master_dict

    def __setitem__(self, name: str, val: Any) -> None:
        if self.master_dict is not None:
            self.master_dict[name] = val
        super().__setitem__(
            name,
            val,
        )  # __dict__ pointed to self so all dict items became attributes


if __name__ == "__main__":
    import doctest

    doctest.testmod()
