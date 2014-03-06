#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re

QUOTED_SINGLE = 1
QUOTED_DOUBLE = 2
FLOAT = 3
INTEGER = 4
BOOL_TRUE = 5
BOOL_FALSE = 6
NONE = 7

NAME_REGEX = re.compile(r"[a-zA-Z_][\sa-zA-Z0-9_\.\/\(\)\:,'\"\|]*")
""" The regular expression that is going to be used in the matching
of variable names/parts should comply with both the name of the variable,
possible filtering pipeline and method calls """

LITERAL_REGEX= re.compile(
    "(?P<quoted_single>['][^']+['])|" + \
    "(?P<quoted_double>[\"][^\"]+[\"])|" + \
    "(?P<float>-?[0-9]+\.[0-9]*)|" + \
    "(?P<integer>-?[0-9]+)|" + \
    "(?P<true_boolean>True)|" + \
    "(?P<false_boolean>False)|" + \
    "(?P<none>None)"
)
""" Regular expression to be used in the parsing of literal values, named
groups are used for the conditional retrieval of each of the types """

class AstNode(object):
    """
    The ast node class, this is the top level abstract
    value from which the various nodes should inherit.
    """

    value = None
    """ The value, this should be the match value
    that original the node (raw value) latter this
    may be used directly in the visit """

    child_nodes = []
    """ The list of nodes that are considered to be
    children of the current node, the maximum number
    of children is not limited """

    def __init__(self):
        self.child_nodes = []

    def __repr__(self):
        return "<ast_node child_nodes:%d>" % len(self.child_nodes)

    def accept(self, visitor):
        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept(visitor)

    def accept_post_order(self, visitor):
        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_post_order(visitor)

        visitor.visit(self)

    def accept_double(self, visitor):
        """
        Accepts the visitor running the iteration logic,
        using double visiting, meaning that the node will
        be visited two times, one before the children visit
        and one time after.

        @type visitor: Visitor
        @param visitor: The visitor object, that is going to
        be used for the visiting operation.
        """

        visitor.visit_index = 0
        visitor.visit(self)

        if visitor.visit_childs:
            for child_node in self.child_nodes:
                child_node.accept_double(visitor)

        visitor.visit_index = 1
        visitor.visit(self)

    def set_value(self, value):
        self.value = value

    def add_child_node(self, child_node):
        self.child_nodes.append(child_node)

    def remove_child_node(self, child_node):
        self.child_nodes.remove(child_node)

class RootNode(AstNode):
    """
    The root node class, this should be used only for
    the root and aggregating node and with no value set.
    """

    def __init__(self):
        AstNode.__init__(self)

class LiteralNode(AstNode):
    """
    The literal node class, used for the representation of
    literal (textual) parts of the template. This is used
    for the inter-parts between the "logical" nodes and
    must be visited with a simple printing operation.
    """

    def __init__(self, value = None):
        AstNode.__init__(self)
        self.value = value

class OutputNode(AstNode):
    """
    The output node class that represent a match that
    is representative of an output request. An example
    of such request would be {{ 'hello world' }}.

    This is equivalent to the more complex single node
    configured as an out operation.
    """

    def __init__(self, value = None):
        AstNode.__init__(self)
        self.value = value
        self.attributes = dict()
        self.process_value()

    def process_value(self):
        value = self.value[2:-2]
        value = value.strip()

        match = NAME_REGEX.match(value)
        if match:
            value = match.group()
            self.attributes["value"] = dict(
                value = value,
                type = "variable"
            )

        match = LITERAL_REGEX.match(value)
        if match:
            value = match.group()
            index = match.lastindex

            if index == QUOTED_SINGLE: value = value.strip("'")
            elif index == QUOTED_DOUBLE: value = value.strip("\"")
            elif index == FLOAT: value = float(value)
            elif index == INTEGER: value = int(index)
            elif index == BOOL_TRUE: value = True
            elif index == BOOL_FALSE: value = False
            elif index == NONE: value = None

            self.attributes["value"] = dict(
                value = value,
                type = "literal"
            )

    def get_attributes(self):
        return self.attributes

    def accept(self, visitor):
        visitor.process_accept(self, "out")

class MatchNode(AstNode):
    """
    The match node class, that represents a node that
    contains a type in the initial part of the value
    and then a series of key to value attributes.
    """

    value_type = None
    """ The value type for the match node this is
    the type of node operation that is going to be
    performed, this value may assume any value
    (eg: out, for, if, else, etc.) """

    attributes = {}
    """ Map describing the complete set of attributes
    (configuration) for the current node, this is a
    set of key value mappings """

    regex = None
    """ The attribute regular expression, that is going
    to be used in the matching of variable based attributes """

    literal_regex = None
    """ The attribute literal regular expression, this value
    is going to be used in the matching of literal attributes """

    def __init__(self, value = None, regex = None, literal_regex = None):
        AstNode.__init__(self)

        self.value = value
        self.regex = regex
        self.literal_regex = literal_regex

        self.attributes = {}

        self.process_value_type()
        self.process_attributes()

    def process_value_type(self):
        match = self.get_start_match()
        match_value = match.get_value()

        match_value_s = match_value.split()
        self.value_type = match_value_s[0][2:]

    def process_attributes(self):
        # retrieve the match value part of the node, this is the string
        # value that is going to be matched against the regular expressions
        # to try to find the various attributes of the node
        match = self.get_start_match()
        match_value = match.get_value()

        # uses both the currently set regular expression and literal
        # regular expression to find the matches for both of these
        # values that will then be processed as attributes
        attributes_matches = self.regex.finditer(match_value)
        literal_matches = self.literal_regex.finditer(match_value)

        # iterates over all the attributes matches to construct the
        # attribute dictionary structure for each of them, note that
        # these matches are only for the variable based values
        for match in attributes_matches:
            # retrieves the attribute value and splits it around
            # the equals operator, and then constructs the dictionary
            # that represents the attribute setting it on the map
            attribute = match.group()
            name, value = attribute.split("=")
            self.attributes[name] = dict(
                value = value,
                type = "variable"
            )

        # iterates over the complete set of literal matches to create
        # the attribute structure for each of them the data type for
        # the literal value will be retrieve from the group index of
        # the match to be used (the regular expression must comply)
        for match in literal_matches:
            attribute = match.group()
            name, value = attribute.split("=")
            index = match.lastindex

            if index == QUOTED_SINGLE: value = value.strip("'")
            elif index == QUOTED_DOUBLE: value = value.strip("\"")
            elif index == FLOAT: value = float(value)
            elif index == INTEGER: value = int(index)
            elif index == BOOL_TRUE: value = True
            elif index == BOOL_FALSE: value = False
            elif index == NONE: value = None

            self.attributes[name] = dict(
                value = value,
                type = "literal"
            )

    def get_value_type(self):
        return self.value_type

    def set_value_type(self, value_type):
        self.value_type = value_type

    def get_attributes(self):
        return self.attributes

    def set_attributes(self, attributes):
        self.attributes = attributes

class SingleNode(MatchNode):
    """
    The single node class, that contains a single value
    and that should have a simple visiting operation.
    """

    def __init__(self, value = None, regex = None, literal_regex = None):
        MatchNode.__init__(self, value, regex, literal_regex)

    def get_start_match(self):
        return self.value

    def accept(self, visitor):
        value_type = self.get_value_type()
        visitor.process_accept(self, value_type)

class CompositeNode(MatchNode):
    """
    The composite node class, that represents a node that contains
    multiple children nodes and for which a visit may be a complex
    task of visiting multiple nodes.
    """

    def __init__(self, value = None, regex = None, literal_regex = None):
        MatchNode.__init__(self, value, regex, literal_regex)

    def get_start_match(self):
        return self.value[0]

    def accept(self, visitor):
        value_type = self.get_value_type()
        visitor.process_accept(self, value_type)
