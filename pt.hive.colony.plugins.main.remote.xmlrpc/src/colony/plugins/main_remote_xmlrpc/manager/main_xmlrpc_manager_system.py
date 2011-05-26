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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import types
import xmlrpclib

import main_xmlrpc_manager_exceptions

HANDLER_BASE_FILENAME = "colony_mod_python/xmlrpc"
""" The handler base filename """

HANDLER_EXTENSION = "py"
""" The handler extension """

HANDLER_FILENAME = "xmlrpc.py"
""" The handler filename """

LIST_METHODS_NAME = "system.listMethods"
""" The list methods name """

APACHE_CONTAINER = "apache"
""" The apache container """

HANDLER_NAME = "xmlrpc"
""" The handler name """

HANDLER_PORT = 80
""" The handler port """

DEFAULT_ENCODER = "utf-8"
""" The default encoder """

class MainXmlrpcManager:
    """
    The main xml rpc manager class.
    """

    main_xmlrpc_manager_plugin = None
    """ The main xml rpc manager plugin """

    service_methods = []
    """ The service methods list """

    service_methods_map = {}
    """ The service methods map """

    def __init__(self, main_xmlrpc_manager_plugin):
        """
        Constructor of the class.

        @type main_xmlrpc_manager_plugin: MainXmlrpcManagerPlugin
        @param main_xmlrpc_manager_plugin: The main xml rpc manager plugin.
        """

        self.main_xmlrpc_manager_plugin = main_xmlrpc_manager_plugin

        self.service_objects = []
        self.service_methods_map = {}

    def get_handler_filename(self):
        return HANDLER_FILENAME

    def is_request_handler(self, request):
        # retrieves the simple filename from the complete path filename
        simple_filename = request.uri.split("/")[-1]

        # compares the simple file name with the handler file name
        if simple_filename == HANDLER_FILENAME:
            return True
        else:
            return False

    def handle_request(self, request):
        # sets the content type for the request
        request.content_type = "text/xml;charset=utf-8"

        # retrieves the post data
        post_data = request.read()

        # the translated request
        translated_request = self.translate_request(post_data)

        # retrieves the parameters and method name of the request
        parameters, method_name = translated_request

        # in case there is a list methods request
        if method_name == LIST_METHODS_NAME and parameters == []:
            result = self.service_methods
            error = None
        # tries to call the requested method
        elif method_name in self.service_methods_map:
            # retrieves the rpc method
            rpc_method = self.service_methods_map[method_name]

            # retrieves the number of arguments for the rpc method
            rpc_method_number_arguments = rpc_method.func_code.co_argcount - 1

            # retrieves the number of parameters sent
            number_parameters = len(parameters)

            # in case the number of sent arguments is the expected
            if not number_parameters == rpc_method_number_arguments:
                result = None
                error = main_xmlrpc_manager_exceptions.InvalidNumberArguments("the number of sent arguments is " + str(number_parameters) + ", expected " + str(rpc_method_number_arguments))
            else:
                try:
                    # calls the rpc method with the given arguments
                    result = rpc_method(*parameters)
                    error = None
                except Exception, exception:
                    # prints info message about exception
                    self.main_xmlrpc_manager_plugin.info("There was an exception handling xml rpc the request: " + unicode(exception))

                    result = None
                    error = exception
        # in case the method name is not valid
        else:
            result = None
            error = main_xmlrpc_manager_exceptions.InvalidMethod("the method name " + method_name + " is not valid")

        # serializes the result into xml
        result_request = self.translate_result(result, method_name, error)

        # writes the serialized result into the buffer
        request.write(result_request)

        # flushes the request, sending the output to the client
        request.flush()

    def is_active(self):
        """
        Tests if the service is active.

        @rtype: bool
        @return: If the service is active.
        """

        # retrieves the plugin manager
        manager = self.main_xmlrpc_manager_plugin.manager

        # in case the current container is apache
        if manager.container == APACHE_CONTAINER:
            return True
        else:
            return False

    def get_handler_name(self):
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def get_handler_port(self):
        """
        Retrieves the handler port.

        @rtype: int
        @return: The handler port.
        """

        return HANDLER_PORT

    def get_handler_properties(self):
        """
        Retrieves the handler properties.

        @rtype: Dictionary
        @return: The handler properties.
        """

        return {
            "handler_base_filename" : HANDLER_BASE_FILENAME,
            "handler_extension" : HANDLER_EXTENSION
        }

    def update_service_methods(self, updated_rpc_service_plugin = None):

        if updated_rpc_service_plugin:
            updated_rpc_service_plugins = [updated_rpc_service_plugin]
        else:
            # clears the service methods list
            self.service_methods = []

            # clears the service map
            self.service_methods_map = {}

            # retrieves the updated rpc service plugins
            updated_rpc_service_plugins = self.main_xmlrpc_manager_plugin.rpc_service_plugins

        for rpc_service_plugin in updated_rpc_service_plugins:
            # retrieves all the method names for the current rpc service
            available_rpc_methods = rpc_service_plugin.get_available_rpc_methods()

            # retrieves all the method alias for the current rpc service
            available_rpc_methods_alias = rpc_service_plugin.get_rpc_methods_alias()

            # in case the plugin contains the rpc method metadata
            if rpc_service_plugin.contains_metadata_key("rpc_method"):
                # retrieves the metadata values for the rpc method
                metadata_values = rpc_service_plugin.get_metadata_key("rpc_method")

                # iterates over all the metadata values
                for metadata_value in metadata_values:
                    # retrieves the method name of the rpc method
                    method_name = metadata_value["method_name"]

                    # retrieves the alias for the rpc method
                    alias = metadata_value["alias"]

                    # retrieves the method for the rpc method from the plugin instance
                    method = getattr(rpc_service_plugin, method_name)

                    # adds the method to the list of available rpc methods
                    available_rpc_methods.append(method)

                    # adds the alias to the list of available rpc methods alias
                    available_rpc_methods_alias[method] = alias

            # retrieves the list of all the available rpc methods
            available_rpc_methods_string = [value.__name__ for value in available_rpc_methods]

            # iterates over all the rpc method alias keys
            for available_rpc_method_alias_key in available_rpc_methods_alias:
                available_rpc_methods_alias_string = available_rpc_methods_alias[available_rpc_method_alias_key]
                available_rpc_methods_string.extend(available_rpc_methods_alias_string)

            self.service_methods.extend(available_rpc_methods_string)

            # retrieves the service id
            service_id = rpc_service_plugin.get_service_id()

            # retrieves the list of service alias
            service_alias = rpc_service_plugin.get_service_alias()

            # creates a list with all the possible service names
            service_names = [service_id] + service_alias

            # iterates over all the possible service names
            for service_name in service_names:
                for available_rpc_method_string in available_rpc_methods_string:
                    composite_available_rpc_method_string = service_name + "." + available_rpc_method_string
                    self.service_methods.append(composite_available_rpc_method_string)

            # iterates over all the available rpc methods to generate the service methods map
            for available_rpc_method in available_rpc_methods:
                # creates the service method names list
                service_method_names = []

                # creates the service method basic names list
                service_method_basic_names = []

                # adds the available rpc method to the service method names list
                service_method_names.append(available_rpc_method.__name__)

                # adds the available rpc method to the service basic method names list
                service_method_basic_names.append(available_rpc_method.__name__)

                # retrieves all the alias to the current service methods
                alias_service_method_names = [value for value in available_rpc_methods_alias[available_rpc_method]]

                # adds the available rpc method alias to the service method names list
                service_method_names.extend(alias_service_method_names)

                # adds the available rpc method alias to the service basic method names list
                service_method_basic_names.extend(alias_service_method_names)

                # iterates over all the service names
                for service_name in service_names:
                    for service_method_basic_name in service_method_basic_names:
                        service_method_complex_name = service_name + "." + service_method_basic_name
                        service_method_names.append(service_method_complex_name)

                # iterates over all the service method names
                for service_method_name in service_method_names:
                    # adds the available rpc method to the map with the service method name as key
                    self.service_methods_map[service_method_name] = available_rpc_method

    def translate_request(self, data):
        """
        Translates the given xml data data into a python request.

        @type data: String
        @param data: The xml data to be translated into a python request.
        @rtype: Any
        @return: The translated python request.
        """

        try:
            # encodes the data with the default encoder
            data_encoded = data.encode(DEFAULT_ENCODER)

            # loads the encoded data
            request = xmlrpclib.loads(data_encoded)
        except:
            raise main_xmlrpc_manager_exceptions.ServiceRequestNotTranslatable(data)

        # returns the translated request
        return request

    def translate_result(self, result, method_name, error):
        """
        Translates the given python result into xml data.

        @type result: Any
        @param result: The python result to be translated into xml data.
        @type method_name: String
        @param method_name: The name of the remotely called method.
        @type error: Error
        @param error: The error for the current request.
        @rtype: String
        @return: The translated xml data.
        """

        # in case there is an error
        if not error == None:
            error_fault = xmlrpclib.Fault(error.__class__.__name__, str(error))
            data = xmlrpclib.dumps(error_fault, None, True)
            return data

        try:
            # in case the result is not None serializes the result
            if result != None:
                return_tuple = tuple([result])
            # otherwise it must be converted to a valid xml-rpc data type (bool)
            else:
                return_tuple = tuple([True])

            # in case the result is an instance
            if type(result) == types.InstanceType:
                # retrieves the class name
                class_name = result.__class__.__name__

                # retrieves the module name
                module_name = result.__module__

                # retrieves the full class name
                full_class_name = module_name + "." + class_name

                result.class_name = class_name
                result.full_class_name = full_class_name

            data = xmlrpclib.dumps(return_tuple, None, True, allow_none = True)
        except main_xmlrpc_manager_exceptions.XmlEncodeException, exception:
            error_fault = xmlrpclib.Fault("XmlEncodeException", "Result Object Not Serializable")
            data = xmlrpclib.dumps(error_fault, None, True)
        except Exception, exception:
            error_fault = xmlrpclib.Fault("XmlEncodeException", "Result Object Not Serializable: " + unicode(exception))
            data = xmlrpclib.dumps(error_fault, None, True)

        # returns the xml data
        return data
