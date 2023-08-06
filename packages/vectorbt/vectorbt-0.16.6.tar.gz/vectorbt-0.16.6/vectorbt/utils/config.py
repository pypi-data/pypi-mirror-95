"""Utilities for configuration."""

import numpy as np
import pandas as pd
from copy import copy


def merge_dicts(*dicts):
    """Merge dicts."""
    x, y = dicts[0], dicts[1]
    if x is None:
        x = {}
    if y is None:
        y = {}

    if len(x) == 0:
        z = y.copy()
    elif len(y) == 0:
        z = x.copy()
    else:
        z = {}
        overlapping_keys = x.keys() & y.keys()
        for k in overlapping_keys:
            if isinstance(x[k], dict) and isinstance(y[k], dict):
                z[k] = merge_dicts(x[k], y[k])
            else:
                z[k] = y[k]
        for k in x.keys() - overlapping_keys:
            z[k] = x[k]
        for k in y.keys() - overlapping_keys:
            z[k] = y[k]

    if len(dicts) > 2:
        return merge_dicts(z, *dicts[2:])
    return z


def copy_dict(dct):
    """Copy dict using shallow-deep copy hybrid.
    
    Traverses all nested dicts and copies each value using shallow copy."""
    dct_copy = dict()
    for k, v in dct.items():
        if isinstance(v, dict):
            dct_copy[k] = copy_dict(v)
        else:
            dct_copy[k] = copy(v)
    return dct_copy


_RaiseKeyError = object()


class Config(dict):
    """Extends dict with config features."""

    def __init__(self, *args, frozen=False, read_only=False, **kwargs):
        super().__init__(*args, **kwargs)
        self._frozen = frozen
        self._read_only = read_only
        self._init_config = copy_dict(self) if not read_only else None

    @property
    def frozen(self):
        """Whether this dict's keys are frozen."""
        return self._frozen

    @property
    def read_only(self):
        """Whether this dict is read-only."""
        return self._read_only

    @property
    def init_config(self):
        """Initial config."""
        return self._init_config

    def __setitem__(self, k, v):
        if self.read_only:
            raise TypeError("Config is read-only")
        if self.frozen:
            if k not in self:
                raise KeyError(f"Key '{k}' is not valid")
        super().__setitem__(k, v)

    def __delitem__(self, k):
        if self.read_only:
            raise TypeError("Config is read-only")
        super().__delitem__(k)

    def pop(self, k, v=_RaiseKeyError):
        if self.read_only:
            raise TypeError("Config is read-only")
        if v is _RaiseKeyError:
            return super().pop(k)
        return super().pop(k, v)

    def popitem(self):
        if self.read_only:
            raise TypeError("Config is read-only")
        return super().popitem()

    def clear(self):
        if self.read_only:
            raise TypeError("Config is read-only")
        return super().clear()

    def update(self, *args, force_update=False, **kwargs):
        other = dict(*args, **kwargs)
        if force_update:
            super().update(other)
        if self.read_only:
            raise TypeError("Config is read-only")
        if self.frozen:
            for k in other:
                if k not in self:
                    raise KeyError(f"Key '{k}' is not valid")
        super().update(other)

    def copy(self):
        return type(self)(self)

    def merge_with(self, other, **kwargs):
        """Merge this and other dict into a new config."""
        return self.__class__(merge_dicts(self, other), **kwargs)

    def reset(self):
        """Reset config to initial config."""
        if self.read_only:
            raise TypeError("Config is read-only")
        self.update(copy_dict(self.init_config), force_update=True)


class Configured:
    """Class with an initialization config."""

    def __init__(self, **config):
        self._config = Config(config, read_only=True)

    @property
    def config(self):
        """Initialization config (read-only)."""
        return self._config

    def copy(self, **new_config):
        """Create a new instance based on the config.

        !!! warning
            This "copy" operation won't return a copy of the instance but a new instance
            initialized with the same config. If the instance has writable attributes,
            their values won't be copied over."""
        return self.__class__(**self.config.merge_with(new_config))

    def __eq__(self, other):
        """Objects are equals if their configs are equal."""
        if type(self) != type(other):
            return False
        my_config = self.config
        other_config = other.config
        if my_config.keys() != other_config.keys():
            return False
        for k, v in my_config.items():
            other_v = other_config[k]
            if isinstance(v, pd.Series) or isinstance(other_v, pd.Series):
                try:
                    pd.testing.assert_series_equal(v, other_v)
                except:
                    return False
            elif isinstance(v, pd.DataFrame) or isinstance(other_v, pd.DataFrame):
                try:
                    pd.testing.assert_frame_equal(v, other_v)
                except:
                    return False
            elif isinstance(v, pd.Index) or isinstance(other_v, pd.Index):
                try:
                    pd.testing.assert_index_equal(v, other_v)
                except:
                    return False
            elif isinstance(v, np.ndarray) or isinstance(other_v, np.ndarray):
                if v.dtype.fields is not None and other_v.dtype.fields is not None:  # records
                    if v.dtype.fields != other_v.dtype.fields:
                        return False
                    for field in v.dtype.names:
                        try:
                            np.testing.assert_array_equal(v[field], other_v[field])
                        except:
                            return False
                else:
                    try:
                        np.testing.assert_array_equal(v, other_v)
                    except:
                        return False
            else:
                if v != other_v:
                    return False
        return True
