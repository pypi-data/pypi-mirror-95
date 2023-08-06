import datetime
import math

from pint import UndefinedUnitError

from kamzik3 import units
from kamzik3.constants import *


def _base_unit(unit):
    try:
        prefix, base_unit, suffix = tuple(units.parse_unit_name(unit))[0]
    except (IndexError, UndefinedUnitError, AttributeError, StopIteration):
        prefix, base_unit, suffix = None, unit, None
    return prefix, base_unit, suffix


def get_attribute_unit_range(attribute):
    prefix, base_unit, suffix = _base_unit(attribute[UNIT])
    if base_unit in ("ampere", "volt", "meter", "degree", "radian", "hertz", "percent"):
        sorted_prefixes = (
            'y', 'z', 'a', 'f', 'p', 'n', 'u', 'm', "", 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'
        )
    elif base_unit == "second":
        return ["ms", "s", "min"]
    elif base_unit in ("degree_Celsius", "kelvin", "degree_Fahrenheit"):
        return ["degC", "degF", "K"]
    elif base_unit in ("bar", "Pa", "atm"):
        return ["mbar", "bar", "Pa", "kPa", "atm"]
    elif base_unit == "revolutions_per_minute":
        return ["rpm", "rps"]
    else:
        sorted_prefixes = (
            'y', 'z', 'a', 'f', 'p', 'n', 'u', 'm', 'c', 'd', "", 'da', 'h', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'
        )
    try:
        converter = units._prefixes[prefix]._converter
        if converter == 1:
            scale = 1
        else:
            scale = converter.scale
    except KeyError:
        scale = 1

    try:
        min_unit = scale * 10 ** -attribute[DECIMALS]
        abs_min, abs_max = abs(attribute[MIN]), abs(attribute[MAX])
        max_unit = scale * (abs_max if abs_max > abs_min else abs_min)
    except TypeError:
        raise TypeError

    unit_range = []
    for prefix in sorted_prefixes:
        converter = units._prefixes[prefix]._converter
        if converter == 1:
            scale = 1
        else:
            scale = converter.scale
        if min_unit <= scale <= max_unit:
            unit_range.append(units.get_symbol("{}{}".format(prefix, base_unit)))

    return unit_range


def get_decimals_diff(old_unit, new_unit):
    old_scale = math.log(units.get_base_units(old_unit)[0], 10)
    new_scale = math.log(units.get_base_units(new_unit)[0], 10)
    return int(round(old_scale - new_scale))


def device_units(device, attribute, value):
    try:
        value = value.replace(u"%", u"percent")
    except AttributeError:
        pass
    device_unit = device.get_attribute(attribute)[UNIT]
    # try:
    converted_value = units.Quantity(value)
    # No unit for value
    if converted_value.unitless:
        # Return in value in device units
        try:
            pint_value = units.Quantity(value)
            if pint_value.u == units.dimensionless:
                return units.Quantity(pint_value.m, device_unit)
            else:
                return pint_value.to(device_unit)
        except AttributeError:
            return units.Quantity(float(units.Quantity(value).m))
    else:
        # Return converted value
        return converted_value.to(device_unit)
    # except DimensionalityError:
    #     # Values are not convertable among each other
    #     return units.Quantity(value, device_unit)


MAX_SECONDS = 3.154e+9


def get_scaled_time_duration(seconds, short=False):
    if seconds < 0:
        return
    if seconds >= MAX_SECONDS:
        return "> 100 Years"

    if not short:
        sec, msec, min, day, hour, month, year = "Sec", "MSec", "Min", "Day", "Hour", "Month", "Year"
    else:
        sec, msec, min, day, hour, month, year = "s", "ms", "m", "D", "h", "M", "Y"

    d = datetime.datetime(1, 1, 1) + datetime.timedelta(seconds=seconds)

    if seconds < 60:
        milliseconds = int(d.microsecond / 1000)
        if milliseconds > 0:
            time_estimate = "{} {} {} {}".format(d.second, sec, milliseconds, msec)
        else:
            time_estimate = "{} {}".format(d.second, sec)
    elif 60 <= seconds < 3600:
        time_estimate = "{} {} {} {}".format(d.minute, min, d.second, sec)
    elif 3600 <= seconds < 24 * 3600:
        time_estimate = "{} {} {} {}".format(d.hour, hour, d.minute, min)
    elif 24 * 3600 <= seconds < 24 * 3600 * 28:
        time_estimate = "{} {} {} {} {} {}".format(d.day - 1, day, d.hour, hour, d.minute, min)
    elif 24 * 3600 * 28 <= seconds < 24 * 3600 * 28 * 12:
        time_estimate = "{} {} {} {} {} {}".format(d.month - 1, month, d.day, day, d.hour, hour)
    else:
        time_estimate = "{} {} {} {} {} {}".format(d.year - 1, year, d.month, month, d.day, day)

    return time_estimate


def seconds_to_datetime(seconds):
    if seconds > MAX_SECONDS:
        seconds = MAX_SECONDS

    return datetime.datetime.fromtimestamp(seconds).strftime("%d.%m.%Y %H:%M:%S")


def get_printable_size(byte_size):
    """
    A bit is the smallest unit, it's either 0 or 1
    1 byte = 1 octet = 8 bits
    1 kB = 1 kilobyte = 1000 bytes = 10^3 bytes
    1 KiB = 1 kibibyte = 1024 bytes = 2^10 bytes
    1 KB = 1 kibibyte OR kilobyte ~= 1024 bytes ~= 2^10 bytes (it usually means 1024 bytes but sometimes it's 1000... ask the sysadmin ;) )
    1 kb = 1 kilobits = 1000 bits (this notation should not be used, as it is very confusing)
    1 ko = 1 kilooctet = 1000 octets = 1000 bytes = 1 kB

    Also Kb seems to be a mix of KB and kb, again it depends on context.

    In linux, a byte (B) is composed by a sequence of bits (b). One byte has 256 possible values.

    More info : http://www.linfo.org/byte.html
    """
    BASE_SIZE = 1024.00
    MEASURE = ["B", "KB", "MB", "GB", "TB", "PB"]

    def _fix_size(size, size_index):
        if not size:
            return "0"
        elif size_index == 0:
            return str(size)
        else:
            return "{:.3f}".format(size)

    current_size = byte_size
    size_index = 0

    while current_size >= BASE_SIZE and len(MEASURE) != size_index:
        current_size = current_size / BASE_SIZE
        size_index = size_index + 1

    size = _fix_size(current_size, size_index)
    measure = MEASURE[size_index]
    return size + " " + measure
