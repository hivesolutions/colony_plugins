#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
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

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

# the token definitions
tokens = ("LPAREN", "RPAREN", "LBRACK", "RBRACK",
          "LBRACE", "RBRACE", "BOLD", "ITALIC",
          "UNDERLINE", "MONOSPACE", "TAG_INIT", "TAG_END",
          "SPACE", "FORCED_NEWLINE", "NAME", "NEWLINE")

# the reserved keywords
reserved = {
    "__" : "UNDERLINE"
}

reserved_values = {
}

t_LPAREN = r"\("
t_RPAREN = r"\)"

t_LBRACK = r"\["
t_RBRACK = r"\]"

t_LBRACE = r"\{"
t_RBRACE = r"\}"

t_BOLD = r"\*\*"
t_ITALIC = r"\/\/"
t_UNDERLINE = r"__"
t_MONOSPACE = r"\'\'"

t_TAG_INIT = r"\<[a-zA-Z]+\>"
t_TAG_END = r"\<\/[a-zA-Z]+\>"

t_SPACE = r"[ \t\r]+"

t_FORCED_NEWLINE = r"\\\\"

def t_NAME(t):
    r"[a-zA-Z_0-9]+"
    t.type = reserved.get(t.value, "NAME")
    t.value = reserved_values.get(t.value, t.value)
    return t

# the new line character
def t_NEWLINE(t):
    r"\n+"
    # retrives the number of newline
    newline_count = t.value.count("\n")
    t.lexer.lineno += newline_count
    t.value = newline_count
    return t

# single line comments
def t_comment(t):
    r"\#[^\n]*\n+"
    pass

# ignored characters
t_ignore = ""

# other character
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
