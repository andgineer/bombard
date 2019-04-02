"""
Dict with access to keys as attributes.

    >>> d = AttrDict({'a': 'b', 'c': 'd'})
    >>> d.c
    ...   f

"""


class AttrDict(dict):
    """
    You can access all dict values as attributes.
    All changes immediately repeated in master_dict.
    """
    def __init__(self, master_dict: dict, **kwargs):
        super().__init__(master_dict, **kwargs)
        self.__dict__ = self
        self.master_dict = master_dict

    def add(self, **kwargs):
        for name, val in kwargs.items():
            self.master_dict[name] = val
            self[name] = val  # add to __dict__ too?