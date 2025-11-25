#  Copyright 2025 HUBzero Foundation, LLC.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

#  HUBzero is a registered trademark of Purdue University.

#  Authors:
#  Daniel Mejia (denphi), Purdue University (denphi@denphi.com)

import numpy as np
from pint import UnitRegistry

ureg = UnitRegistry()
ureg.autoconvert_offset_to_baseunit = True
#Q_ = ureg.Quantity


class Params:
    """
    Base class for tool parameters.
    """
    def __init__(self, **kwargs):
        """
        Initialize the parameter.

        Args:
            **kwargs: Parameter attributes (id, label, description, units, default, current, disable_fix).
        """
        self.disable_fix = kwargs.get('disable_fix', False)
        self._units = None
        self.validator = None
        self._current = None
        self._default = None
        self.label = kwargs.get('label', None)
        self.description = kwargs.get('description', None)
        self.id = kwargs.get('id', None)
        self.units = kwargs.get('units', None)
        self.default = kwargs.get('default', None)
        self.current = kwargs.get('current', None)

    def fixUnits(self, newval):
        """
        Fix unit formatting.

        Args:
            newval (str): The value with units.

        Returns:
            str: The value with fixed units.
        """
        if isinstance(newval, str) and self.disable_fix == False:
            if (newval == "/cm3"):
                newval = "1/cm3"
            elif (newval == "J/smK2"):
                newval = ""
            newval = newval.replace("K", "k")
            newval = newval.replace("v", "V")
            newval = newval.replace("cm3", "cm^3")
            newval = newval.replace("cm-3", "cm^-3")
            newval = newval.replace("cm2", "cm^2")
            newval = newval.replace("cm-2", "cm^-2")
            newval = newval.replace("m3", "m^3")
            newval = newval.replace("m2", "m^2")
            newval = newval.replace("V-1", "V^-1")
            newval = newval.replace("s-1", "s^-1")
            newval = newval.replace("Vs", "(volt * sec)")
            newval = newval.replace("Vm", "(volt * meter)")
            newval = newval.replace('C', 'c')
            newval = newval.replace('/cm', 'cm^-1')
        else:
            newval = str(newval)
        return newval

    def validate_current(self, newval):
        """
        Validate the current value.

        Args:
            newval: The new value to validate.

        Returns:
            The validated value.
        """
        if (newval != None):
            if (self._units != None):
                newval = self.fixUnits(newval)
                val = ureg.parse_expression(newval)
                if isinstance(val, ureg.Quantity):
                    newval = val.to(self.validator).magnitude
                else:
                    newval = val
        return newval

    @property
    def value(self):
        value = self._current
        if (value == None):
            value = self._default
        if (self._units):
            return str(value) + str(self._units)
        else:
            return str(value)

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, newval):
        self._default = Params.validate_current(self, newval)

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, newval):
        self._current = self.validate_current(newval)

    def validate_units(self, newval):
        """
        Validate the units.

        Args:
            newval (str): The new units.

        Returns:
            str: The validated units.
        """
        if (newval == ""):
            newval = None
        if (newval != None):
            self.validator = None
            newvalidation = self.fixUnits(newval)
            self.validator = ureg.parse_expression(newvalidation)
        return newval

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, newval):
        self._units = self.validate_units(newval)

    def to_dict(self):
        """
        Convert the parameter to a dictionary.

        Returns:
            dict: The parameter dictionary.
        """
        res = {'type': 'Param'}
        res['id'] = self.id
        if (self._current is not None):
            res['current'] = self.current
        if (self.description is not None):
            res['description'] = self.description
        if (self.label is not None):
            res['label'] = self.label
        if (self.units is not None):
            res['units'] = self.units
        if (self._default is not None):
            res['default'] = self.default
        return res

    def __repr__(self):
        res = "{"
        repr = self.to_dict()
        for k, v in repr.items():
            res += k.__repr__() + " : " + v.__repr__() + ", "
        res += "}"
        return res


class ParamsFactory:
    """
    Factory class for creating parameter objects.
    """
    def builder(descriptor):
        """
        Build a parameter object from a descriptor.

        Args:
            descriptor (dict): The parameter descriptor.

        Returns:
            Params: The created parameter object.
        """
        if 'type' in descriptor:
            if (descriptor['type'] == "integer"):
                return Integer(**descriptor)
            elif (descriptor['type'] == "number"):
                return Number(**descriptor)
            elif (descriptor['type'] == "choice"):
                return Choice(**descriptor)
            elif (descriptor['type'] == "string"):
                return String(**descriptor)
            elif (descriptor['type'] == "boolean"):
                return Boolean(**descriptor)
            else:
                #print (descriptor)
                return Params(**descriptor)

        else:
            return Params()


class Integer(Params):
    """
    Integer parameter.
    """
    def __init__(self, **kwargs):
        """
        Initialize the Integer parameter.

        Args:
            **kwargs: Parameter attributes (min, max, etc.).
        """
        self.disable_fix = kwargs.get('disable_fix', False)
        self._min = None
        self._max = None
        self._units = None
        self.validator = None
        self._current = None
        self._default = None
        self.label = kwargs.get('label', None)
        self.description = kwargs.get('description', None)
        self.id = kwargs.get('id', None)
        self.units = kwargs.get('units', None)
        self.default = kwargs.get('default', None)
        self.current = kwargs.get('current', None)
        self.min = kwargs.get('min', None)
        self.max = kwargs.get('max', None)

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, newval):
        if newval != None:
            self._min = int(Params.validate_current(self, newval))
        else:
            self._min = None

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, newval):
        if newval != None:
            self._max = int(Params.validate_current(self, newval))
        else:
            self._max = None

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, newval):
        if newval != None:
            self._current = int(self.validate_current(newval))
        else:
            self._current = None

    def validate_current(self, newval):
        """
        Validate the current value.

        Args:
            newval: The new value to validate.

        Returns:
            int: The validated integer value.

        Raises:
            ValueError: If value is out of range.
        """
        if (newval != None):
            newval = Params.validate_current(self, newval)
            if self._units is not None:
                units = self._units
            if self._min is not None and newval < self._min:
                raise ValueError(str(newval) + units +
                                 ", Minimum value is " + str(self._min) + units)
            if self._max is not None and newval > self._max:
                raise ValueError(str(newval) + units +
                                 ", Maximum value is " + str(self._max) + units)
        return newval

    def to_dict(self):
        """
        Convert the parameter to a dictionary.

        Returns:
            dict: The parameter dictionary.
        """
        res = Params.to_dict(self)
        if (self._min is not None):
            res['min'] = self._min
        if (self._max is not None):
            res['max'] = self._max
        res['type'] = "Integer"
        return res


class Number(Params):
    """
    Number (float) parameter.
    """
    def __init__(self, **kwargs):
        """
        Initialize the Number parameter.

        Args:
            **kwargs: Parameter attributes (min, max, etc.).
        """
        self.disable_fix = kwargs.get('disable_fix', False)
        self._units = None
        self.validator = None
        self._current = None
        self._default = None
        self._min = None
        self._max = None
        self.label = kwargs.get('label', None)
        self.description = kwargs.get('description', None)
        self.id = kwargs.get('id', None)
        self.units = kwargs.get('units', None)
        self.default = kwargs.get('default', None)
        self.current = kwargs.get('current', None)
        self.min = kwargs.get('min', None)
        self.max = kwargs.get('max', None)

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, newval):
        if newval != None:
            self._min = float(Params.validate_current(self, newval))
        else:
            self._min = None

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, newval):
        if newval != None:
            self._max = float(Params.validate_current(self, newval))
        else:
            self._max = None

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, newval):
        if newval != None:
            self._current = float(self.validate_current(newval))
        else:
            self._current = None

    def validate_current(self, newval):
        """
        Validate the current value.

        Args:
            newval: The new value to validate.

        Returns:
            float: The validated float value.

        Raises:
            ValueError: If value is out of range.
        """
        if (newval != None):
            newval = Params.validate_current(self, newval)
            units = ""
            if self._units is not None:
                units = self._units
            if self._min is not None and newval < self._min:
                raise ValueError(str(newval) + units +
                                 ", Minimum value is " + str(self._min) + units)
            if self._max is not None and newval > self._max:
                raise ValueError(str(newval) + units +
                                 ", Maximum value is " + str(self._max) + units)
        return newval

    def to_dict(self):
        """
        Convert the parameter to a dictionary.

        Returns:
            dict: The parameter dictionary.
        """
        res = Params.to_dict(self)
        if (self._min is not None):
            res['min'] = self._min
        if (self._max is not None):
            res['max'] = self._max
        res['type'] = "Number"
        return res


class Choice(Params):
    """
    Choice parameter (selection from options).
    """
    def __init__(self, **kwargs):
        """
        Initialize the Choice parameter.

        Args:
            **kwargs: Parameter attributes (options, etc.).
        """
        # always set these first
        self.options = kwargs.get('options', [])
        Params.__init__(self, **kwargs)


    def validate_current(self, newval):
        """
        Validate the current value.

        Args:
            newval: The new value to validate.

        Returns:
            The validated value.

        Raises:
            ValueError: If value is not a valid option.
        """
        if (newval != None):
            newval = Params.validate_current(self, newval)
            if len(self.options) > 0 and newval not in self.options:
                if newval not in [p[0] for p in self.options]:
                    if newval not in [p[1] for p in self.options]:
                        raise ValueError(
                        str(newval) + " value should be one of the posible options" + json.dumps(self.options))
            return newval
        return newval

    def to_dict(self):
        """
        Convert the parameter to a dictionary.

        Returns:
            dict: The parameter dictionary.
        """
        res = Params.to_dict(self)
        if (self.options is not None):
            res['options'] = self.options
        res['type'] = "Choice"
        return res


class String(Params):
    """
    String parameter.
    """
    def __init__(self, **kwargs):
        """
        Initialize the String parameter.

        Args:
            **kwargs: Parameter attributes.
        """
        Params.__init__(self, **kwargs)

    def validate_current(self, newval):
        """
        Validate the current value.

        Args:
            newval: The new value to validate.

        Returns:
            str: The validated string value.
        """
        if (newval != None):
            newval = Params.validate_current(self, newval)
            return str(newval)
        return newval

    def to_dict(self):
        """
        Convert the parameter to a dictionary.

        Returns:
            dict: The parameter dictionary.
        """
        res = Params.to_dict(self)
        res['type'] = "String"
        return res


class Boolean(Params):
    """
    Boolean parameter.
    """
    def __init__(self, **kwargs):
        """
        Initialize the Boolean parameter.

        Args:
            **kwargs: Parameter attributes.
        """
        Params.__init__(self, **kwargs)

    def validate_current(self, newval):
        """
        Validate the current value.

        Args:
            newval: The new value to validate.

        Returns:
            str: "yes" or "no".

        Raises:
            ValueError: If value is not a valid boolean.
        """
        if (newval != None):
            newval = Params.validate_current(self, newval)
            if (newval in ["yes", 1, "si", True, "true", "on"]):
                return "yes"
            elif (newval in ["no", 0, "no", False, "false", "off"]):
                return "no"
            else:
                raise ValueError("values should be a valid boolean")
        return newval

    def to_dict(self):
        """
        Convert the parameter to a dictionary.

        Returns:
            dict: The parameter dictionary.
        """
        res = Params.to_dict(self)
        res['type'] = "Boolean"
        return res
