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

import xml.etree.ElementTree as ET


class OutputFactory:
    """
    Factory class for creating output objects.
    """
    def builder(element):
        """
        Build an output object from an XML element.

        Args:
            element (xml.etree.ElementTree.Element): The XML element.

        Returns:
            Output: The created output object.

        Raises:
            ValueError: If element is not an Element object.
        """
        if not isinstance(element, ET.Element):
            raise ValueError("must pass Element object")
        if 'id' in element.attrib and element.attrib["id"] != "":
            if element.tag == "curve":
                return Curve(value=element, id=element.attrib["id"], type=element.tag)
            elif element.tag == "number":
                return Number(value=element, id=element.attrib["id"], type=element.tag)
            elif element.tag == "integer":
                return Integer(value=element, id=element.attrib["id"], type=element.tag)
            elif element.tag == "string":
                return String(value=element, id=element.attrib["id"], type=element.tag)
            elif element.tag == "log":
                return String(value=element, id=element.attrib["id"], type=element.tag)
            elif element.tag == "sequence":
                return Sequence(value=element, id=element.attrib["id"], type=element.tag)
            else:
                return Output(value=element, id=element.attrib["id"], type=element.tag)
        return None


class Output:
    """
    Base class for tool outputs.
    """
    def __init__(self, **kwargs):
        """
        Initialize the Output.

        Args:
            **kwargs: Output attributes (id, type, label, description, value).
        """
        self.id = kwargs.get('id', None)
        self.type = kwargs.get('type', None)
        self.label = kwargs.get('label', None)
        self.description = kwargs.get('description', None)
        self.value = kwargs.get('value', None)

    def xmltodict_handler(self, parent_element):
        """
        Helper to convert XML element to dictionary.

        Args:
            parent_element (xml.etree.ElementTree.Element): The parent element.

        Returns:
            dict: The dictionary representation.
        """
        result = dict()
        for element in parent_element:
            if len(element):
                obj = self.xmltodict_handler(element)
            else:
                obj = element.text

            if result.get(element.tag):
                if hasattr(result[element.tag], "append"):
                    result[element.tag].append(obj)
                else:
                    result[element.tag] = [result[element.tag], obj]
            else:
                result[element.tag] = obj
        return result

    def xmltodict(self, element):
        """
        Convert XML element to dictionary.

        Args:
            element (xml.etree.ElementTree.Element): The element to convert.

        Returns:
            dict: The dictionary representation.

        Raises:
            ValueError: If element is not an Element object.
        """
        if not isinstance(element, ET.Element):
            raise ValueError("must pass Element object")
        return {element.tag: self.xmltodict_handler(element)}

    def validate_value(self, newval):
        """
        Validate and process the value.

        Args:
            newval: The new value.

        Returns:
            The processed value.
        """
        if (newval != None):
            if isinstance(newval, ET.Element):
                newval = self.xmltodict(newval)
                if self.type in newval:
                    newval = newval[self.type]
        return newval

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, newval):
        self._value = self.validate_value(newval)

    def to_dict(self):
        """
        Convert the output to a dictionary.

        Returns:
            dict: The output dictionary.
        """
        res = {'type': 'Output'}
        res['id'] = self.id
        if (self.description is not None):
            res['description'] = self.description
        if (self.label is not None):
            res['label'] = self.label
        if (self.value is not None):
            res['value'] = self.value
        return res

    def __repr__(self):
        res = "{"
        repr = self.to_dict()
        for k, v in repr.items():
            res += k.__repr__() + " : " + v.__repr__() + ", "
        res += "}"
        return res


class Curve(Output):
    """
    Curve output.
    """
    def __init__(self, **kwargs):
        """
        Initialize the Curve output.

        Args:
            **kwargs: Output attributes.
        """
        Output.__init__(self, **kwargs)

    def xmltodict_handler(self, parent_element):
        """
        Helper to convert XML element to dictionary.

        Args:
            parent_element (xml.etree.ElementTree.Element): The parent element.

        Returns:
            dict: The dictionary representation.
        """
        result = dict()
        for element in parent_element:
            if len(element):
                obj = self.xmltodict_handler(element)
            else:
                if element.tag == "xy":
                    obj = element.text
                    obj = obj.replace("--", " ")
                    obj = obj.replace("\n", " ")
                    obj = obj.strip()
                else:
                    obj = element.text

            if result.get(element.tag):
                if hasattr(result[element.tag], "append"):
                    result[element.tag].append(obj)
                else:
                    result[element.tag] = [result[element.tag], obj]
            else:
                result[element.tag] = obj
        return result

    def to_dict(self):
        """
        Convert the output to a dictionary.

        Returns:
            dict: The output dictionary.
        """
        res = Output.to_dict(self)
        res["type"] = "Curve"
        return res


class Number(Output):
    """
    Number output.
    """
    def __init__(self, **kwargs):
        """
        Initialize the Number output.

        Args:
            **kwargs: Output attributes.
        """
        Output.__init__(self, **kwargs)

    def to_dict(self):
        """
        Convert the output to a dictionary.

        Returns:
            dict: The output dictionary.
        """
        res = Output.to_dict(self)
        res["type"] = "Number"
        return res


class Integer(Output):
    """
    Integer output.
    """
    def __init__(self, **kwargs):
        """
        Initialize the Integer output.

        Args:
            **kwargs: Output attributes.
        """
        Output.__init__(self, **kwargs)

    def to_dict(self):
        """
        Convert the output to a dictionary.

        Returns:
            dict: The output dictionary.
        """
        res = Output.to_dict(self)
        res["type"] = "Integer"
        return res


class String(Output):
    """
    String output.
    """
    def __init__(self, **kwargs):
        """
        Initialize the String output.

        Args:
            **kwargs: Output attributes.
        """
        Output.__init__(self, **kwargs)

    def to_dict(self):
        """
        Convert the output to a dictionary.

        Returns:
            dict: The output dictionary.
        """
        res = Output.to_dict(self)
        res["type"] = "String"
        return res


class Sequence(Output):
    """
    Sequence output.
    """
    def __init__(self, **kwargs):
        """
        Initialize the Sequence output.

        Args:
            **kwargs: Output attributes.
        """
        Output.__init__(self, **kwargs)

    def validate_value(self, newval):
        """
        Validate and process the value.

        Args:
            newval: The new value.

        Returns:
            dict: The processed sequence dictionary.
        """
        if (newval != None):
            if isinstance(newval, ET.Element):
                elements = newval.findall('element')
                newval = {e.find("index").text.strip(): [OutputFactory.builder(
                    e[i]) for i in range(1, len(e))] for e in elements}
        return newval

    def to_dict(self):
        """
        Convert the output to a dictionary.

        Returns:
            dict: The output dictionary.
        """
        res = Output.to_dict(self)
        res["type"] = "Sequence"
        return res
