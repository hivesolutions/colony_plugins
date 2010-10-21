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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

TYPE_VALUE = "type"
""" The type value """

VALUE_VALUE = "value"
""" The value value """

EXTRA_TYPE_VALUE = "extra_type"
""" The extra type value """

TYPE_NUMBER_VALUE = "type_number"
""" The type number value """

TYPE_CONSTRUCTED_VALUE = "type_constructed"
""" The type constructed value """

TYPE_CLASS_VALUE = "type_class"
""" The type class value """

BIND_VALUE = "bind"
""" The bind value """

EOC_TYPE = 0x00
""" The eoc (end of content) type """

BOOLEAN_TYPE = 0x01
""" The boolean type """

INTEGER_TYPE = 0x02
""" The integer type """

BIT_STRING_TYPE = 0x03
""" The bit string type """

OCTET_STRING_TYPE = 0x04
""" The octet string type """

ENUMERATED_TYPE = 0x0a
""" The enumerated type """

SEQUENCE_TYPE = 0x10
""" The sequence type """

PRIMITIVE_MODE = 0x00
""" The primitive mode """

CONSTRUCTED_MODE = 0x01
""" The constructed mode """

UNIVERSAL_CLASS = 0x00
""" The universal class """

APPLICATION_CLASS = 0x01
""" The application class """

CONTEXT_SPECIFIC_CLASS = 0x02
""" The context specific class """

PRIVATE_CLASS = 0x03
""" The private class """

LDAP_REQUEST_TYPE_MAP = {BIND_VALUE : 0x00, "unbind" : 0x02,
                         "search" : 0x03, "modify" : 0x06,
                         "add" : 0x08, "delete" : 0x0a,
                         "modify_dn" : 0x00, "compare" : 0x00,
                         "abandon" : 0x00, "extended" : 0x00}
""" The map of ldap request types """

LDAP_RESPONSE_TYPE_MAP = {BIND_VALUE : 0x01, "search_result_enttry" : 0x04,
                          "search_result_reference" : 0x13, "search_result_done" : 0x05,
                          "modify" : 0x07, "add" : 0x09, "delete" : 0x0b}
""" The map of ldap response types """

class ProtocolOperation:

    def __init__(self):
        pass

    def process_value(self, value):
        # retrieves the protocol operation extra type
        protocol_operation_extra_type = value[EXTRA_TYPE_VALUE]

        # retrieves the protocol operation extra type number
        protocol_operation_extra_type_number = protocol_operation_extra_type[TYPE_CLASS_VALUE]

        # retrieves the protocol operation class from the type
        # class map using the protocol operation extra type number
        protocol_operation_class = TYPE_CLASS_MAP[protocol_operation_extra_type_number]

        # creates a new protocol operation structure
        protocol_operation_structure = protocol_operation_class()

        # processes the value using the value, retrieving the protocol operation
        protocol_operation = protocol_operation_structure.process_value(value)

        # returns the protocol operation
        return protocol_operation

class LdapResult(ProtocolOperation):

    result_code = None

    matched_dn = None

    error_message = None

    referral = None

    def __init__(self, result_code = None, matched_dn = None, error_message = None, referral = None):
        ProtocolOperation.__init__(self)
        self.result_code = result_code
        self.error_message = error_message
        self.referral = referral

    def process_value(self, value):
        # retrieves the ldap result value
        ldap_result_value = value[VALUE_VALUE]

        # retrieves the result code and the result code value
        result_code = ldap_result_value[0]
        result_code_value = result_code[VALUE_VALUE]

        # retrieves the matched dn and the matched dn value
        matched_dn = ldap_result_value[1]
        matched_dn_value = matched_dn[VALUE_VALUE]

        # retrieves the error message and the error message value
        error_message = ldap_result_value[2]
        error_message_value = error_message[VALUE_VALUE]

        # sets the current values
        self.result_code = result_code_value
        self.matched_dn = matched_dn_value
        self.error_message = error_message_value

        # returns the self value
        return self

class BindResponse(LdapResult):
    pass

class BindRequest(ProtocolOperation):

    version = None

    name = None

    authentication = None

    def __init__(self, version = None, name = None, authentication = None):
        ProtocolOperation.__init__(self)
        self.version = version
        self.name = name
        self.authentication = authentication

    def get_value(self):
        # retrieves the bind request type
        bind_request_type = LDAP_REQUEST_TYPE_MAP[BIND_VALUE]

        # creates the version integer value
        version = {TYPE_VALUE: INTEGER_TYPE, VALUE_VALUE : self.version}

        # creates the name octet string value
        name = {TYPE_VALUE: OCTET_STRING_TYPE, VALUE_VALUE : self.name}

        # retrieves the authentication value
        authentication = self.authentication.get_value()

        # creates the protocol operation contents (list)
        protocol_operation_contents = [version, name, authentication]

        # creates the bind operation sequence value
        bind_operation = {TYPE_VALUE: SEQUENCE_TYPE, VALUE_VALUE : protocol_operation_contents,
                          EXTRA_TYPE_VALUE : {TYPE_NUMBER_VALUE : bind_request_type,
                                              TYPE_CONSTRUCTED_VALUE : CONSTRUCTED_MODE,
                                              TYPE_CLASS_VALUE : APPLICATION_CLASS}}

        # returns the bind operation (value)
        return bind_operation

class Authentication:

    def __init__(self):
        pass

class SimpleAuthentication(Authentication):

    value = None

    def __init__(self, value):
        Authentication.__init__(self)
        self.value = value

    def get_value(self):
        # creates the authentication octet string value
        authentication = {TYPE_VALUE: OCTET_STRING_TYPE, VALUE_VALUE : self.value,
                          EXTRA_TYPE_VALUE : {TYPE_NUMBER_VALUE : 0,
                                              TYPE_CLASS_VALUE : CONTEXT_SPECIFIC_CLASS}}

        # returns the authentication (value)
        return authentication

TYPE_CLASS_MAP = {LDAP_REQUEST_TYPE_MAP[BIND_VALUE] : BindRequest,
                  LDAP_RESPONSE_TYPE_MAP[BIND_VALUE] : BindResponse}
""" The map associating a type with a class map """
