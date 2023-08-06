import collections
import math
from time import perf_counter_ns

import pint
from numpy import dtype, float16, float32, float64, uint16, uint32, uint64, int16, int32, int64, uint8, int8, ndarray

from kamzik3 import units
from kamzik3.constants import *
from kamzik3.constants import SAVE_CHANGE
from kamzik3.snippets.snippetDataAccess import is_equal


class SetFunction(object):

    def __init__(self, attribute, callback=None):
        self.attribute = attribute
        self.callback = callback

    def __enter__(self):
        self.attribute.with_set_function = True
        self.attribute.set_callback = self.callback
        return self.attribute

    def __exit__(self, value_type, value, traceback):
        self.attribute.with_set_function = False
        self.attribute.set_callback = None


class Attribute(dict):
    attribute_keys = {VALUE, TYPE, UNIT, READONLY, DESCRIPTION}
    integer_types = (int8, int16, int32, int64, uint8, uint16, uint32, uint64)
    float_types = (float16, float32, float64)
    unsigned_types = (uint8, uint16, uint32, uint64)
    with_set_function = False
    last_stream_time = last_update_time = perf_counter_ns()
    last_update_time_diff = 0
    numerical = False
    set_token = 0
    set_callback = None
    min_stream_timeout = 100 * 1e6

    def attribute_copy(self):
        """
        Copy current Attribute.
        :return: Attribute
        """
        return Attribute(**self)

    def __init__(self, attribute_id=None, default_value=None, min_value=None, max_value=None, unit=None,
                 set_function=None, default_type=u"str", decimals=0, readonly=False, description=None,
                 set_value_when_set_function=True, tolerance=(0, 0), factor=1, offset=0, save_change=False, **kwargs):
        dict.__init__(self)
        self._callbacks = {}
        self.attribute_id = attribute_id
        self.set_function = set_function
        self.default_type = default_type
        self[OFFSET] = offset
        self[FACTOR] = factor
        # Set attribute value flag when using set function.
        # This flag prevents change of attribute's value before value is actually set on device side.
        self.set_value_when_set_function = set_value_when_set_function
        if unit is None:
            unit = u""
        self[UNIT] = unit
        self.min_stream_timeout = kwargs.get("min_stream_timeout", 100) * 1e6
        default_type = kwargs.get(TYPE, default_type)
        if default_type == TYPE_LIST:
            self[TYPE] = TYPE_LIST
        elif isinstance(default_type, (list, collections.abc.KeysView)):
            self[TYPE] = TYPE_LIST
            self[TYPE_LIST_VALUES] = list(default_type)
        elif default_type == TYPE_ARRAY or isinstance(default_type, ndarray):
            self[TYPE] = TYPE_ARRAY
        else:
            default_type = dtype(default_type)
            self[TYPE] = dtype(default_type).name
            if default_type in self.integer_types:
                self[DECIMALS] = 0
                if min_value is None and default_type in self.unsigned_types:
                    self[MIN] = 0
                else:
                    self[MIN] = int(min_value) if min_value is not None else -math.inf
                self[MAX] = int(max_value) if max_value is not None else math.inf
                self.numerical = True
            elif default_type in self.float_types:
                self[DECIMALS] = decimals
                self[MIN] = float(min_value) if min_value is not None else -math.inf
                self[MAX] = float(max_value) if max_value is not None else math.inf
                self.numerical = True
        if self.numerical:
            self[TOLERANCE] = [float(tolerance[0]), float(tolerance[1])]
        self[READONLY] = readonly
        self[DESCRIPTION] = description
        self[VALUE] = default_value
        self[SETPOINT] = None
        self[PREVIOUS] = None
        self[SAVE_CHANGE] = save_change
        self.update(kwargs)

    def _update_set_time(self):
        """
        Value of attribute was update.
        Set last_update_time and last_update_time_diff for future reference.
        :return: None
        """
        update_time = perf_counter_ns()
        self.last_update_time_diff = update_time - self.last_update_time
        self.last_update_time = update_time

    def __setitem__(self, k, v):
        if k == VALUE:
            try:
                self[PREVIOUS] = self[VALUE]
            except KeyError:
                pass
            if isinstance(v, units.Quantity):
                try:
                    v = v.to(self[UNIT]).m
                except AttributeError:
                    v = v.m
        elif k == TOLERANCE:
            # Make sure that tolerance is float
            v = [float(t) for t in v]
        elif k == UNIT and v is not None:
            if v == u"%":
                v = u"percent"
            if v not in ("", None):
                if units.parse_unit_name(v) == ():
                    units.define(u"{}=1".format(v))
                    units.derived_units.append(v)
        try:
            if is_equal(self[k], v):
                return
        except KeyError:
            pass

        if k == VALUE and self.set_function and self.with_set_function:
            self[SETPOINT] = v
            setpoint = self.remove_offset_factor(v)
            # Release set function flag
            self.with_set_function = False
            if self.set_value_when_set_function:
                # Store actual attribute[k] value into dictionary
                super(Attribute, self).__setitem__(k, v)
            # Call set function
            if hasattr(self.set_function, "callback"):
                self.set_token = self.set_function(setpoint, callback=self.set_callback)
            else:
                # We don't have callback in a function, so just call it plain without callback
                self.set_token = self.set_function(setpoint)
            if not self.set_value_when_set_function:
                return
            self._update_set_time()
        else:
            # Store actual attribute[k] value into dictionary
            super(Attribute, self).__setitem__(k, v)
            self._update_set_time()

        self.handle_callbacks(k, v)

    def handle_callbacks(self, k, v):
        """
        When any parameter of attribute is set, call all relevant callbacks that are attached to the parameter.
        :param k: str
        :param v: str
        :return: None
        """
        # Call all relevant callbacks
        for callback, (max_update_rate, updated_at, key_filter) in self._callbacks.copy().items():
            # Check update rate, continue if it's less than max_update_rate
            if k == VALUE and max_update_rate is not None and (self.last_update_time - updated_at) <= max_update_rate:
                continue
            # Check if key_filter is set
            if key_filter is None:
                # Key can be any value, therefore callback with key and value
                callback(k, v)
            elif k == key_filter:
                # Since we have filter set, callback with just value
                callback(v)
            else:
                continue
            try:
                # Set last callback time
                self._callbacks[callback][1] = perf_counter_ns()
            except KeyError:
                # Callback no longer exists, skipping
                pass

    @staticmethod
    def from_dict(dictionary):
        """
        Create Attribute from provided dictionary.
        :param dictionary: dict
        :return: Attribute
        """
        if isinstance(dictionary, dict):
            if Attribute.is_attribute(dictionary):
                if dictionary[UNIT] not in ("", None):
                    try:
                        units.get_name(dictionary[UNIT])
                    except pint.errors.UndefinedUnitError:
                        units.define(u"{}=1".format(dictionary[UNIT]))
                        units.derived_units.append(dictionary[UNIT])
                return Attribute(**dictionary)
            else:
                for key, attribute in dictionary.items():
                    dictionary[key] = Attribute.from_dict(attribute)
            return dictionary
        else:
            return dictionary

    @staticmethod
    def is_attribute(dictionary):
        """
        Check if provided dictionary is convertible to Attribute.
        :param dictionary: dict
        :return: bool
        """
        try:
            return Attribute.attribute_keys.issubset(dictionary.keys())
        except (AttributeError, TypeError, ValueError):
            return False

    def attach_callback(self, callback, max_update_rate=None, key_filter=None):
        """
        Attach callback to Attribute.
        :param callback: callable function
        :param max_update_rate: max update rate in ms
        :return: None
        """
        assert callable(callback)

        if callback not in self._callbacks:
            if max_update_rate is not None:
                max_update_rate *= 1e6
            self._callbacks[callback] = [max_update_rate, perf_counter_ns(), key_filter]

    def detach_callback(self, callback):
        """
        Detach callback from attribute.
        :param callback: callable function
        :return: None
        """
        assert callable(callback)
        try:
            del self._callbacks[callback]
        except KeyError:
            pass  # Callback no longer exists

    def apply_offset_factor(self, value=None):
        """
        Apply offset and factor to attribute value.
        :param value: numerical value
        :return: mixed
        """
        if value is None:
            value = self[VALUE]

        if value is not None and self.numerical:
            return (value + self[OFFSET]) * self[FACTOR]
        elif self.default_type is bool:
            return self[FACTOR] == value
        else:
            return value

    def remove_offset_factor(self, value=None):
        """
        Remove offset and factor from attribute value.
        :param value: numerical value
        :return: mixed
        """
        if value is None:
            value = self[VALUE]

        if value is not None and self.numerical:
            return (value / self[FACTOR]) - self[OFFSET]
        elif self.default_type is bool:
            return self[FACTOR] == value
        else:
            return value

    def read_and_reset_token(self):
        """
        Return token and reset it back to 0.
        :return: int
        """
        token = self.set_token
        self.set_token = 0
        return token

    @staticmethod
    def list_attribute(attribute):
        """
        Create list from input attribute.
        Many methods relies on the fact that attribute is stored as list.
        :param attribute: mixed
        :return: list
        """
        if isinstance(attribute, list):
            return attribute
        elif isinstance(attribute, tuple):
            return list(attribute)
        else:
            return [attribute]

    def convert_units(self, value):
        """
        Convert input value to current attribute unit.
        :param value: units.Quantity
        :return: value or units.Quantity
        """
        assert isinstance(value, units.Quantity)
        if value.dimensionless:
            if self[UNIT] is None:
                return value
            else:
                return units.Quantity("{} {}".format(value.m, self[UNIT]))

        return value.to(self[UNIT])

    def within_limits(self, value):
        """
        Check if value is within limits.
        :param value:  units.Quantity
        :return: bool
        """
        assert isinstance(value, units.Quantity)
        return self.minimum() <= value <= self.maximum()

    def value(self):
        """
        Get attribute's value.
        :return: Quantity
        """
        if self.numerical:
            try:
                return units.Quantity(self[VALUE], self[UNIT])
            except (pint.UndefinedUnitError, AttributeError):
                return units.Quantity(self[VALUE])
            except TypeError:
                return self[VALUE]
        else:
            return self[VALUE]

    def minimum(self):
        """
        Get attribute's minimum value.
        :return: Quantity
        """
        if self.numerical:
            try:
                return units.Quantity(self[MIN], self[UNIT])
            except (pint.UndefinedUnitError, AttributeError):
                return units.Quantity(self[MIN])
            except TypeError:
                return self[MIN]
        else:
            return self[MIN]

    def maximum(self):
        """
        Get attribute's maximum value.
        :return: Quantity
        """
        if self.numerical:
            try:
                return units.Quantity(self[MAX], self[UNIT])
            except (pint.UndefinedUnitError, AttributeError):
                return units.Quantity(self[MAX])
            except TypeError:
                return self[MAX]
        else:
            return self[MAX]

    def negative_tolerance(self):
        """
        Get attribute's negative tolerance in units.
        :return: Quantity
        """
        if self.numerical:
            try:
                return units.Quantity(self[TOLERANCE][0], self[UNIT])
            except (pint.UndefinedUnitError, AttributeError):
                return units.Quantity(self[TOLERANCE][0])
            except TypeError:
                return self[TOLERANCE][0]
        else:
            return self[TOLERANCE][0]

    def positive_tolerance(self):
        """
        Get attribute's positive tolerance in units.
        :return: Quantity
        """
        if self.numerical:
            try:
                return units.Quantity(self[TOLERANCE][1], self[UNIT])
            except (pint.UndefinedUnitError, AttributeError):
                return units.Quantity(self[TOLERANCE][1])
            except TypeError:
                return self[TOLERANCE][1]
        else:
            return self[TOLERANCE][1]

    def offset(self):
        """
        Get attribute's value offset in units.
        :return: Quantity
        """
        if self.numerical:
            try:
                return units.Quantity(self[OFFSET], self[UNIT])
            except (pint.UndefinedUnitError, AttributeError):
                return units.Quantity(self[OFFSET])
            except TypeError:
                return self[OFFSET]
        else:
            return self[OFFSET]

    def setpoint(self):
        """
        Get attribute's setpoint in units.
        :return: Quantity
        """
        if self.numerical:
            try:
                return units.Quantity(self[SETPOINT], self[UNIT])
            except (pint.UndefinedUnitError, AttributeError):
                return units.Quantity(self[SETPOINT])
            except TypeError:
                return self[SETPOINT]
        else:
            return self[SETPOINT]

    def unit(self):
        """
        Get current unit.
        :return: str
        """
        return self[UNIT]
