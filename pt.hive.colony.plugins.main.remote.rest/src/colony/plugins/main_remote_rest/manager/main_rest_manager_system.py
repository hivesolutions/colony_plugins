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

__revision__ = "$LastChangedRevision: 7147 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-12-21 16:50:46 +0000 (seg, 21 Dez 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re
import urllib

import main_rest_manager_exceptions

HANDLER_BASE_FILENAME = "/colony_mod_python/rest/"
""" The handler base filename """

HANDLER_EXTENSION = "py"
""" The handler extension """

HANDLER_FILENAME = "rest.py"
""" The handler filename """

LIST_METHODS_NAME = "system.listMethods"
""" The list methods name """

APACHE_CONTAINER = "apache"
""" The apache container """

HANDLER_NAME = "rest"
""" The handler name """

DEFAULT_ENCODER = "utf-8"
""" The default encoder """

URL_REGEX_VALUE = "(?P<protocol>\w+\:\/\/)?(?P<base_name>[^\:\/\?#]+)(?P<port>\:\d+)?(?P<resource_reference>(\/[^\?#]+)*)\/?(\?(?P<options>([^#])*))?(?P<location>#(.*))?"
""" The url regex value """

URL_REGEX = re.compile(URL_REGEX_VALUE)
""" The url regex """

class MainRestManager:
    """
    The main rest manager class.
    """

    main_rest_manager_plugin = None
    """ The main rest manager plugin """

    service_methods = []
    """ The service methods list """

    service_methods_map = {}
    """ The service methods map """

    def __init__(self, main_rest_manager_plugin):
        """
        Constructor of the class.

        @type main_rest_manager_plugin: MainRestManagerPlugin
        @param main_rest_manager_plugin: The main rest manager plugin.
        """

        self.main_rest_manager_plugin = main_rest_manager_plugin

        self.service_objects = []
        self.service_methods_map = {}

    def get_handler_filename(self):
        return HANDLER_FILENAME

    def is_request_handler(self, request):
        # retrieves the request filename
        request_filename = request.uri

        # in case the handler base filename is in the start of the request filename
        if request_filename.find(HANDLER_BASE_FILENAME) == 0:
            return True
        else:
            return False

    def handle_request(self, request):
        # retrieves the request filename
        request_filename = request.uri

        # retrieves the handler base filename length
        handler_base_filename_length = len(HANDLER_BASE_FILENAME)

        # retrieves the resource path
        resource_path = request_filename[handler_base_filename_length:]

        # splits the resource path
        resource_path_splitted = resource_path.split("/")

        if not resource_path_splitted[0] == "services":
            return False

        # retrieves the midle path name
        middle_path_name = resource_path_splitted[1:-1]

        # retrieves the last path name
        last_path_name = resource_path_splitted[-1]

        # splits the last path name
        last_path_name_splitted = last_path_name.split(".")

        # retrieves the last path name splitted length
        last_path_name_splitted_length = len(last_path_name_splitted)

        # sets the default last path initial extension
        last_path_initial_extension = None

        # in case there is an extension defined
        if last_path_name_splitted_length == 2:
            # retrieves the last path initial name and extension
            last_path_initial_name, last_path_initial_extension = last_path_name_splitted
        # in case there is no extension defined
        elif last_path_name_splitted_length == 1:
            # retrieves the last path initial name
            last_path_initial_name, = last_path_name_splitted
        else:
            raise main_rest_manager_exceptions.BadServiceRequest("invalid value last path name value %s: " + last_path_name_splitted)

        # retrieves the method name list
        method_name_list = middle_path_name + [last_path_initial_name]

        # creates the real method name, joining the method name parts
        method_name = ".".join(method_name_list)

        # in case there is a list methods request
        if method_name == LIST_METHODS_NAME:
            result = self.service_methods
        # tries to call the requested method
        elif method_name in self.service_methods_map:
            # retrieves the rpc method
            rpc_method = self.service_methods_map[method_name]

            # creates the arguments map
            arguments_map = {}

            # iterates over all the variable names in the function
            # variables
            for variable_name in rpc_method.func_code.co_varnames:
                if variable_name in request.attributes_map:
                    # retrieves the variable value from the attributes map
                    variable_value = request.attributes_map[variable_name]

                    # unquotes the variable value
                    variable_value = urllib.unquote(variable_value)

                    # sets the variable value in the arguments map
                    arguments_map[variable_name] = variable_value

            # calls the rpc method with the arguments map
            result = rpc_method(**arguments_map)
        # in case the method name is not valid
        else:
            raise main_rest_manager_exceptions.InvalidMethod("the method name " + method_name + " is not valid")

        # retrieves the encoder name
        encoder_name = last_path_initial_extension

        # serializes the result for the given encoder name retrieving the content type
        # and the translated result
        content_type, result_translated = self.translate_result(result, encoder_name)

        # sets the content type for the request
        request.content_type = content_type

        # writes the result translated
        request.write(result_translated)

        # flushes the request, sending the output to the client
        request.flush()

        # returns true
        return True

    def is_active(self):
        # retrieves the plugin manager
        manager = self.main_rest_manager_plugin.manager

        # in case the current container is apache
        if manager.container == APACHE_CONTAINER:
            return True
        else:
            return False

    def get_handler_name(self):
        return HANDLER_NAME

    def get_handler_port(self):
        return 80

    def get_handler_properties(self):
        return {"handler_base_filename" : HANDLER_BASE_FILENAME, "handler_extension" : HANDLER_EXTENSION}

    def update_service_methods(self, updated_rpc_service_plugin = None):
        if updated_rpc_service_plugin:
            updated_rpc_service_plugins = [updated_rpc_service_plugin]
        else:
            # clears the service methods list
            self.service_methods = []

            # clears the service map
            self.service_methods_map = {}

            # retrieves the updated rpc service plugins
            updated_rpc_service_plugins = self.main_rest_manager_plugin.rpc_service_plugins

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
        Translates the given encoded data data into a python request.

        @type data: String
        @param data: The encoded data to be translated into a python request.
        @rtype: Any
        @return: The translated python request.
        """

        # returns the translated request
        return data

    def translate_result(self, result, encoder_name = None):
        """
        Translates the given python result into the encoding defined.

        @type result: Any
        @param result: The python result to be translated into encoded data.
        @type method_name: String
        @param method_name: The name of the encoder to be used.
        @rtype: Tuple
        @return: The content type and the translated data.
        """

        # retrieves the rest encoder plugins
        rest_encoder_plugins = self.main_rest_manager_plugin.rest_encoder_plugins

        # in case the encoder name is defined
        if encoder_name:
            # iterates over all the rest encoder plugins
            for rest_encoder_plugin in rest_encoder_plugins:
                if rest_encoder_plugin.get_encoder_name() == encoder_name:
                    # retrieves the content type from the rest encoder plugin
                    content_type = rest_encoder_plugin.get_content_type()

                    # calls the the encoder plugin to encode the result
                    result_encoded = rest_encoder_plugin.encode_value(result)

                    # returns the content type and the encoded result
                    return content_type, result_encoded

            # raises the invalid encoder exception
            raise main_rest_manager_exceptions.InvalidEncoder("the " + encoder_name + " encoder is invalid")
        else:
            # sets the default content type
            content_type = "text/plain"

            # retrieves the result encoded with the default encoder
            result_encoded = str(result)

            # returns the content type and the encoded result
            return content_type, result_encoded

class RestRequest:
    """
    The rest request class.
    """

    request = None
    """ The associated request """

    def __init__(self, request):
        pass
