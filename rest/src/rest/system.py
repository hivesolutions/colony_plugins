#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re
import os
import time
import shelve
import datetime
import threading

import colony

import exceptions

REGEX_COMILATION_LIMIT = 99
""" The regex compilation limit """

HANDLER_BASE_FILENAME = "/dynamic/rest/"
""" The handler base filename this is the base path
that is considered to be the prefix of the request """

HANDLER_EXTENSION = "py"
""" The handler extension """

HANDLER_FILENAME = "rest.py"
""" The handler filename """

HANDLER_NAME = "rest"
""" The handler name, to be used as the primary
identifier for the current handling infra-structure """

HANDLER_PORT = 80
""" The handler port, this is the default port value
meaning that additional configuration values may
change the port that is going to be used at runtime """

DOMAIN_VALUE = "domain"
""" The domain value """

SECURE_VALUE = "secure"
""" The secure value """

LOCALHOST_VALUES = (
    "localhost",
    "127.0.0.1"
)
""" The localhost values """

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
""" The date format """

DEFAULT_EXPIRATION_DATE = "Thu, 01 Jan 1970 00:00:00 GMT"
""" The default expiration date """

DEFAULT_LANG_VALUE = "en"
""" The default lang value """

DEFAULT_EXPIRATION_DELTA_TIMESTAMP = 31536000
""" The default expiration delta timestamp """

DEFAULT_TIMEOUT = 259200
""" The default timeout (seventy two hours of life)
note that a "touch" operation on the session will
extend the session lifetime and ensure that there's
always the same time until expiration """

DEFAULT_MAXIMUM_TIMEOUT = DEFAULT_TIMEOUT * 64
""" The default maximum timeout (sixty four
times the timeout value) this is the hard limit on
the amount of time until for the expiration meaning
that this is the limit for the touch operation """

DEFAULT_TOUCH_SECURE_DELTA = 360
""" The default time delta used to introduce a security
factor in the timestamp used in the touching of the
(modified) date """

class Rest(colony.System):
    """
    The rest (manager) class, the top level system class
    that handles the incoming rest requests.
    """

    matching_regex_list = []
    """ The list of matching regex to be used in
    route matching, this value will be iterated to
    try to find a good match for the incoming request """

    matching_regex_base_values_map = {}
    """ The map containing the base values for the
    various matching regex """

    rest_service_routes_map = {}
    """ The rest service routes map """

    plugin_id_plugin_map = {}
    """ The plugin id plugin map """

    regex_index_plugin_id_map = {}
    """ The regex index plugin id map """

    service_methods = []
    """ The service methods list """

    service_methods_map = {}
    """ The service methods map """

    session_c = None
    """ The reference to the class that is going to be
    used for session creation and loading, this may
    not be defined and for such situations the default
    class is going to be used (in memory) """

    def __init__(self, plugin, session_c = None):
        colony.System.__init__(self, plugin)
        self.session_c = session_c or ShelveSession
        self.matching_regex_list = []
        self.matching_regex_base_values_map = {}
        self.rest_service_routes_map = {}
        self.plugin_id_plugin_map = {}
        self.regex_index_plugin_id_map = {}
        self.service_methods = []
        self.service_methods_map = {}
        self.session_c.load()

    def get_handler_filename(self):
        """
        Retrieves the handler filename.

        @rtype: String
        @return: The handler filename.
        """

        return HANDLER_FILENAME

    def is_request_handler(self, request):
        """
        Retrieves if it's an handler for the given request.

        @type request: Request
        @param request: The request to be used in the test.
        @rtype: bool
        @return: If it's an handler for the given request.
        """

        # retrieves the request filename
        request_filename = request.uri

        # in case the handler base filename is in the start of the
        # request filename this is the correct handler for the request
        # otherwise it's not and an invalid value is returned
        if request_filename.find(HANDLER_BASE_FILENAME) == 0: return True
        else: return False

    def handle_request(self, request):
        """
        Handles the given request, this is the main entry point
        for the handling of the request and the responsible for
        the creation and routing of the rest request.

        Multiple types of handling are possible ranging from remote
        procedure call ones to simple service ones.

        @type request: Request
        @param request: The request to be handled.
        """

        # retrieves the rest encoder plugins, these values are going
        # to be set in the rest request that is going to be created
        rest_encoder_plugins = self.plugin.rest_encoder_plugins

        # retrieves the request filename as the uri of the provided
        # (native) request object
        request_filename = request.uri

        # retrieves the handler base filename length and removed that
        # part of the filename from it to create the resource path and
        # splits it around its own components
        handler_base_filename_length = len(HANDLER_BASE_FILENAME)
        resource_path = request_filename[handler_base_filename_length:]
        resource_path_splitted = resource_path.split("/")

        # retrieves the rest resource name and path name and then
        # splits the last name into its own components
        resource_name = resource_path_splitted[0]
        middle_path_name = resource_path_splitted[1:-1]
        last_path_name = resource_path_splitted[-1]
        last_path_name_splitted = last_path_name.rsplit(".", 1)
        last_path_name_splitted_length = len(last_path_name_splitted)

        # sets the default last path initial extension
        last_path_initial_extension = None

        # in case there is an extension defined in the path the name
        # and the extension are extracted from the split value
        if last_path_name_splitted_length >= 2:
            last_path_initial_name = last_path_name_splitted[0]
            last_path_initial_extension = last_path_name_splitted[1]

        # otherwise in case there's at least a name defined it's extracted
        # from the splitted value to be evaluated
        elif last_path_name_splitted_length == 1:
            last_path_initial_name, = last_path_name_splitted

        # as a fallback procedure an exception must be raised indicating
        # that the provided path for evaluation is invalid as it's not
        # defined according to the specification
        else:
            raise exceptions.InvalidPath(
                "invalid last path name value size: " +\
                str(last_path_name_splitted_length)
            )

        # retrieves the encoder name
        encoder_name = last_path_initial_extension

        # constructs the rest path list
        path_list = middle_path_name + [last_path_initial_name]

        # creates the rest request object that is going to be used
        # for the rest level handling this object encapsulates the
        # underlying server oriented object
        rest_request = RestRequest(self, request)

        try:
            # updates the rest request session
            # loading the appropriate session in
            # case it exists
            rest_request.update_session()
        except:
            # logs a debug message about the fact that
            # no valid session could be loaded
            self.plugin.debug("Session is invalid no session loaded or updated")

        # "touches" the rest request updating it's internal timing
        # structures, note that this operation is mandatory
        rest_request.touch()

        # sets a series of attributes in the rest request that may be
        # used latter for a series of operations
        rest_request.set_resource_name(resource_name)
        rest_request.set_path_list(path_list)
        rest_request.set_encoder_name(encoder_name)
        rest_request.set_rest_encoder_plugins(rest_encoder_plugins)

        # in case the request is meant to be handled by services a
        # special case is selected and a special handling is performed
        if resource_name == "services":
            # handles the request with the services request handler
            # and then return immediately as the request is handled
            self.handle_rest_request_services(rest_request)
            return

        # otherwise it's a "general" request and the typical handling
        # strategy is going to be performed (as usual)
        else:
            # iterates over all the matching regex in the matching regex list
            for matching_regex in self.matching_regex_list:
                # retrieves the resource path match and in case there is
                # no valid resource path match, must continue the loop
                resource_path_match = matching_regex.match(resource_path)
                if not resource_path_match: continue

                # retrieves the base value for the matching regex
                base_value = self.matching_regex_base_values_map[matching_regex]

                # retrieves the index of the captured group
                group_index = resource_path_match.lastindex

                # calculates the rest service plugin index from the base value,
                # the group index and subtracts one value
                rest_service_plugin_index = base_value + group_index - 1

                # retrieves the plugin id from the rest service plugin index
                plugin_id = self.regex_index_plugin_id_map[rest_service_plugin_index]

                # retrieves the rest service plugin using the plugin id
                rest_service_plugin = self.plugin_id_plugin_map[plugin_id]

                # handles the rest request to the rest service plugin
                rest_service_plugin.handle_rest_request(rest_request)

                # returns immediately
                return

        # raises the rest request not handled exception
        raise exceptions.RestRequestNotHandled("no rest service plugin could handle the request")

    def handle_rest_request_services(self, rest_request):
        """
        Handles the rest request meant for services, these
        are special requests where the path of the request
        should be considered to be a method name and the
        parameter of the request arguments to the remote
        method. This is considered legacy operation mode
        and it's not recommended.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be handled,
        this request is going to be used for the resolution
        process of the remote method and for the passing of
        the proper parameters/arguments into it.
        """

        # retrieves the (underlying) request for the current
        # rest request, this value may be used latter for the
        # access to internal structures and then retrieves the
        # name of the "encoder" for the current request
        request = rest_request.get_request()
        encoder_name = rest_request.get_encoder_name()

        # retrieves the complete set of strings (items) that make
        # part of the current request's path and then joins them
        # with the "token" separator as the method name
        path_list = rest_request.get_path_list()
        method_name = ".".join(path_list)

        # in case there is a list methods request, this is considered
        # to be a special call and the result is "automatically" set
        # as the current set of service methods
        if method_name == "system.listMethods": result = self.service_methods

        # in case the method is current registered in the service methods
        # and is a valid method, the typical work flow is performed
        elif method_name in self.service_methods_map:
            # retrieves the rpc method using the provided method
            # name (this will fail in case the method does not exists)
            rpc_method = self.service_methods_map[method_name]

            # creates the arguments map, that will hold the various
            # arguments for the method call created from the request
            arguments_map = {}

            # iterates over all the variable names in the function
            # variables to try to map the arguments and the arguments
            for variable_name in rpc_method.func_code.co_varnames:
                if not variable_name in request.attributes_map: continue

                # retrieves the variable value from the attributes map,
                # unquotes the variable value and sets the variable
                # value in the arguments map (as expected)
                variable_value = request.attributes_map[variable_name]
                variable_value = colony.unquote_plus(variable_value)
                arguments_map[variable_name] = variable_value

            # calls the rpc method with the arguments map created using
            # the various attributes from the request
            result = rpc_method(**arguments_map)

        # in case the method name is not valid must raise an exception
        # indicating the problem on the method name
        else: raise exceptions.InvalidMethod("the method name " + method_name + " is not valid")

        # serializes the result for the given encoder name retrieving
        # the content type and the translated result, these values are
        # going to be set in the request (as expected by specification)
        content_type, result_translated = self.translate_result(result, encoder_name)

        # sets the default (success) status code the content type
        # and the result (data) itself in the request, then runs
        # the flush operation on the request (to update it)
        rest_request.set_status_code(200)
        rest_request.set_content_type(content_type)
        rest_request.set_result_translated(result_translated)
        rest_request.flush()

    def is_active(self):
        """
        Tests if the service is active.

        @rtype: bool
        @return: If the service is active.
        """

        # retrieves the plugin manager
        manager = self.plugin.manager

        # in case the current container is apache
        # the service is considered to be active
        is_apache = manager.container == "apache"
        if is_apache: return True
        else: return False

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

        return dict(
            handler_base_filename = HANDLER_BASE_FILENAME,
            handler_extension = HANDLER_EXTENSION
        )

    def load_rest_service_plugin(self, rest_service_plugin):
        """
        Loads the rest service plugin, in the rest manager.

        @type rest_service_plugin: Plugin
        @param rest_service_plugin: The rest service plugin to be loaded.
        """

        # retrieves the rest service plugin id
        rest_service_plugin_id = rest_service_plugin.id

        # retrieves the rest service plugin routes and registers them
        # under the proper routes map setting then the plugin in the
        # proper identifier to instance resolution map
        routes_list = rest_service_plugin.get_routes()
        self.rest_service_routes_map[rest_service_plugin_id] = routes_list
        self.plugin_id_plugin_map[rest_service_plugin_id] = rest_service_plugin

        # updates the matching regex because the loading of the plugin
        # may have changed the global regex (new partial regex)
        self._update_matching_regex()

    def unload_rest_service_plugin(self, rest_service_plugin):
        """
        Unloads the rest service plugin, from the rest manager.

        @type rest_service_plugin: Plugin
        @param rest_service_plugin: The rest service plugin to be unloaded.
        """

        # retrieves the rest service plugin id
        rest_service_plugin_id = rest_service_plugin.id

        # deletes the route list associated with the plugin to be unloaded
        # and removed the identifier to instance resolution map
        del self.rest_service_routes_map[rest_service_plugin_id]
        del self.plugin_id_plugin_map[rest_service_plugin_id]

        # updates the matching regex because some of the regex expressions
        # may have been removed by the unload operation of the plugin
        self._update_matching_regex()

    def update_service_methods(self, updated_rpc_service_plugin = None):
        if updated_rpc_service_plugin:
            updated_rpc_service_plugins = [updated_rpc_service_plugin]
        else:
            # clears the service methods list and map and
            # retrieves the updated rpc service plugins
            self.service_methods = []
            self.service_methods_map = {}
            updated_rpc_service_plugins = self.plugin.rpc_service_plugins

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

            # extends the service methods list with the available rpc methods string
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

        return data

    def translate_result(self, result, encoder_name = None):
        """
        Translates the given python result into the encoding defined.

        This method will try to find the correct encoder according to
        the requested name failing with an exception in case no rest
        encoder plugin is loaded for the requested naming.

        @type result: Any
        @param result: The python result to be translated into encoded data.
        @type method_name: String
        @param method_name: The name of the encoder to be used.
        @rtype: Tuple
        @return: The content type and the translated data.
        """

        # retrieves the rest encoder plugins
        rest_encoder_plugins = self.plugin.rest_encoder_plugins

        # in case no encoder name is defined the default result is
        # returns as a plain string of the provided result
        if not encoder_name: "text/plain", str(result)

        # iterates over all the complete set of rest encoder plugins
        # trying to find the encoder for the requested name
        for rest_encoder_plugin in rest_encoder_plugins:
            # verifies if the current rest encoder is the valid one and in
            # case it's not skips the current loop, not found
            is_valid = rest_encoder_plugin.get_encoder_name() == encoder_name
            if not is_valid: continue

            # retries the content type that is going to be returned from
            # the rest encoder plugin and then runs the encoding process
            # returning then a tuple containing both the content type and
            # the result data for the request that is being processed
            content_type = rest_encoder_plugin.get_content_type()
            result_encoded = rest_encoder_plugin.encode_value(result)
            return content_type, result_encoded

        # raises the invalid encoder exception because no valid encoder
        # has been found for the requested name
        raise exceptions.InvalidEncoder("the " + encoder_name + " encoder is invalid")

    def clear_sessions(self):
        """
        Removes all the sessions from the current internal
        structures, this is equivalent to the invalidation
        of all the sessions in the rest manager.
        """

        self.session_c.clear()

    def get_session(self, session_id):
        """
        Retrieves the session with the given session id
        from the underlying registry that stores the various
        session in secondary/main memory.

        @type session_id: String
        @param session_id: The id of the session to retrieve.
        @rtype: RestSession
        @return: The session that has been loaded from memory
        or an invalid value in case no session was found
        """

        return self.session_c.get_s(session_id)

    def _update_matching_regex(self):
        """
        Updates the matching regex.
        """

        # starts the matching regex value buffer
        matching_regex_value_buffer = colony.StringBuffer()

        # clears the matching regex list
        self.matching_regex_list = []

        # clears the matching regex base value map
        self.matching_regex_base_values_map.clear()

        # sets the is first plugin flag
        is_first_plugin = True

        # starts the index value
        index = 0

        # starts the current base value
        current_base_value = 0

        # iterates over all the items in the rest service routes map
        for rest_service_plugin_id, routes_list in self.rest_service_routes_map.items():
            # in case it's the first plugin to be used in
            # the creation of the matching regex unset the flag
            # otherwise adds the "or" character to the buffer
            if is_first_plugin: is_first_plugin = False
            else: matching_regex_value_buffer.write("|")

            # adds the group part of the regex to the matching regex value buffer
            matching_regex_value_buffer.write("(")

            # sets the is first flag
            is_first = True

            # iterates over all the routes in the routes list
            for route in routes_list:
                # in case it's the first route updates the flag otherwise
                # writes the "or" operator to the buffer
                if is_first: is_first = False
                else: matching_regex_value_buffer.write("|")

                # adds the route to the matching regex value buffer
                matching_regex_value_buffer.write(route)

            # closes the matching regex value group
            matching_regex_value_buffer.write(")")

            # sets the rest service plugin id in the regex index
            # plugin id map
            self.regex_index_plugin_id_map[index] = rest_service_plugin_id

            # increments the index
            index += 1

            # in case the current index is in the limit of the python
            # regex compilation
            if index % REGEX_COMILATION_LIMIT == 0:
                # retrieves the matching regex value from the matching
                # regex value buffer
                matching_regex_value = matching_regex_value_buffer.get_value()

                # compiles the matching regex value
                matching_regex = re.compile(matching_regex_value)

                # adds the matching regex to the matching regex list
                self.matching_regex_list.append(matching_regex)

                # sets the base value in matching regex base values map
                self.matching_regex_base_values_map[matching_regex] = current_base_value

                # re-sets the current base value
                current_base_value = index

                # resets the matching regex value buffer
                matching_regex_value_buffer.reset()

                # sets the is first flag
                is_first = True

        # retrieves the matching regex value from the matching
        # regex value buffer, compiles it and adds the (new)
        # matching regex to the matching regex list and map
        matching_regex_value = matching_regex_value_buffer.get_value()
        matching_regex = re.compile(matching_regex_value)
        self.matching_regex_list.append(matching_regex)
        self.matching_regex_base_values_map[matching_regex] = current_base_value

class RestRequest(object):
    """
    The rest request class, responsible for the representation
    of a request coming through the rest layer system.

    This class should also be able to provide method for the
    interaction with the output stream to be returned.
    """

    rest = None
    """ The reference to the owner rest system object
    used to access utility functions """

    request = None
    """ The associated request, may be used for operation
    propagation to the lower layer (encapsulation) """

    flushed = False
    """ If the request has already been flushed to the lower
    layer, meaning that data has already been sent to the
    underlying stream """

    session = None
    """ The associated session object, should allays be access
    indirectly through the proper accessor method """

    resource_name = None
    """ The resource name """

    path_list = None
    """ The path list """

    encoder_name = None
    """ The encoder name, as the name of the encoder that is
    going to be used in the handling of the request """

    content_type = None
    """ The type of the content that is going to be returned
    as part of this request """

    result_translated = None
    """ The translated result as a data string of contents that
    are going to be returned as part of the result for request """

    rest_encoder_plugins = []
    """ The rest encoder plugins that are going to be used
    in the translation process of the request workflow """

    rest_encoder_plugins_map = []
    """ The rest encoder plugins map that contains the various
    "translation" plugins associated with their "names" """

    parameters_map = {}
    """ The parameters map, used to store temporary data """

    _generation_time = None
    """ The original time of generation of the rest request
    measured as seconds since the epoch """

    _generation_clock = None
    """ The original time of generation of the rest request
    measured as seconds since the start of the system process """

    def __init__(self, rest, request):
        """
        Constructor of the class.

        @type rest: MainRestManager
        @param rest: The rest.
        @type request: Request
        @param request: The associated request.
        """

        self.rest = rest
        self.request = request

        self.rest_encoder_plugins = []
        self.rest_encoder_plugins_map = {}
        self.parameters_map = {}

        # updates the generation time value with the current
        # time (useful for generation time) also updates the
        # clock value (useful for benchmarking)
        self._generation_time = time.time()
        self._generation_clock = time.clock()

    def start_session(
        self,
        force = False,
        session_id = None,
        timeout = DEFAULT_TIMEOUT,
        maximum_timeout = DEFAULT_MAXIMUM_TIMEOUT
    ):
        """
        Starts the session for the given session id,
        or generates a new session id.
        In case the session id is not provided a new
        session id is generated in a secure manner.

        @type force: bool
        @param force: If the session should be created if a session
        is already selected.
        @type session_id: String
        @param session_id: The session id to be used.
        @type timeout: float
        @param timeout: The timeout to be used in the session.
        @type maximum_timeout: float
        @param maximum_timeout: The maximum timeout to be used in the session.
        """

        # in case a session exists and force flag is disabled
        # avoids creation (provides duplicate creation blocking)
        # must return immediately
        if self.session and not force: return

        # in case no session id is defined, must generate a new
        # one using a secure algorithm for it (avoid corruption)
        if not session_id:
            # retrieves the random plugin and uses it to generate
            # a new random based session identifier to be used
            random_plugin = self.rest.plugin.random_plugin
            session_id = random_plugin.generate_random_md5_string()

        # creates a new rest session and sets
        # it as the current session (uses the timeout information)
        self.session = self.rest.session_c.new(
            session_id,
            timeout = timeout,
            maximum_timeout = maximum_timeout
        )

        # retrieves the host name value
        domain = self._get_domain()

        # checks if the current request is secure, in case
        # it is the session start must be encrypted and only
        # used in secure channels (the cookie must be set accordingly)
        is_secure = self.request.is_secure()

        # starts the session with the defined domain
        self.session.start(domain, secure = is_secure)

    def stop_session(self):
        """
        Stops the current session, this operation should clear
        the current session and remove it from the current context.
        """

        # in case no session is defined, creates a new empty
        # session that is going to be used for the operation
        if not self.session: self.session = self.session_c()

        # retrieves the domain value and uses it in the stop
        # operation of the currently defined session
        domain = self._get_domain()
        self.session.stop(domain)

    def clear_sessions(self):
        """
        Removes all the sessions from the rest manager internal
        structures, this is equivalent to the invalidation
        of all the sessions in the rest manager.
        """

        # clears the session related structures, removing all
        # the sessions from the rest manager and then invalidate
        # the current session
        self.rest.clear_sessions()
        self.session = None

    def update_session(self):
        """
        Updates the current session.
        This method tries to "load" the session associated
        with the current request.
        The updating of the session will be archived using
        a set of predefined techniques.
        """

        # updates the session using the attribute method
        # this strategy goes through the especially designated
        # session id attribute to load the session
        self._update_session_attribute()

        # updates the session using the cookie method, this
        # strategy loads the cookie from the session id attribute
        # defined in the cookie header
        self._update_session_cookie()

    def touch(self):
        """
        Touches the internal session, updating the expire
        time with the timeout value.
        """

        # in case the session is defined updates the
        # expire time according to the timeout and
        # the current time
        self.session and self.session.update_expire_time()

    def touch_date(self, secure_delta = DEFAULT_TOUCH_SECURE_DELTA):
        """
        Touches the last modified timestamp value, setting it
        to the current date information including a "small"
        security oriented delta value to avoid browser problems.

        @type secure_delta: float
        @param secure_delta: The delta value to be removed from the
        current time value to avoid browser problems
        """

        # updates the last modified timestamp value with the current
        # time value reduced by the secure delta value
        self.request.last_modified_timestamp = time.time() - secure_delta

    def update_timeout(self, timeout, maximum_timeout = None):
        """
        Updates the session timeout (and maximum timeout) values
        so that the session may be extended or shortened.

        This method provides extra security tools for session
        timing control.

        @type timeout: float
        @param timeout: The timeout value to be used as the "new"
        timeout of the session.
        @type maximum_timeout: float
        @param maximum_timeout: The maximum timeout value to be
        used as the "new" maximum timeout of the session.
        """

        # in case no session is defined must return immediately
        # not possible to change timeout in case no session is
        # currently defined
        if not self.session: return

        # sets the maximum timeout value in case is not currently
        # set as the triple value of the timeout
        maximum_timeout = maximum_timeout or timeout * 3

        # updates the session timeout and maximum timeout values
        # and then generates the expire time from the current
        # time and the given timeout and maximum timeout
        self.session.timeout = timeout
        self.session.maximum_timeout = maximum_timeout
        self.session._generate_expire_time(timeout, maximum_timeout)

        # updates the session in the rest request, provides
        # the infra-structure to update expire structures
        self.rest.update_session(self.session)

    def read(self):
        """
        Reads the contents of the request associated with this
        rest request, this operation may take some performance
        impact as the complete data is stored in memory.

        @rtype: String
        @return: The complete data contents of the request associated
        with the current rest request.
        """

        return self.request.read()

    def write(self, data):
        """
        Writes the provided chunk data to the underlying request
        structures. The data is not immediately flushed to the
        client side.

        @type data: String
        @param data: The data to be written to the underlying
        request structures.
        """

        return self.request.write(data)

    def process(self):
        """
        Processes the underlying request object, this should
        start the flushing of the data to the client peer.

        Use this method with care as it may corrupt the request
        life-cycle and create unexpected issues in the server.
        """

        # retrieves the request elements, the service handler and the
        # service connection to be used in the processing then uses
        # them to process the request (send request to client)
        service = self.request.get_service()
        service_connection = self.request.get_service_connection()
        service.process_request(self.request, service_connection)

    def parse_post(self):
        """
        Parses the post message using the default,
        parses and the default encoding.
        """

        # parses the post attributes
        self.request.parse_post_attributes()

    def is_get(self):
        """
        Tests the request to check if it is of type
        get method.

        @rtype: bool
        @return: If the request method is of type get.
        """

        # in case the operation is of type get must return
        # valid otherwise returns false (default validation)
        if self.request.operation_type == "GET": return True
        else: return False

    def is_post(self):
        """
        Tests the request to check if it is of type
        post method.

        @rtype: bool
        @return: If the request method is of type post.
        """

        # in case the operation is of type post must return
        # valid otherwise returns false (default validation)
        if self.request.operation_type == "POST": return True
        else: return False

    def is_debug(self, minimum_level = 6):
        """
        In case the request should be set in debug mode.
        Maximum verbosity, in actions like exception handling.

        @type minimum_level: int
        @param minimum_level: The minimum level to be used for verbosity.
        """

        # retrieves the rest plugin
        rest_plugin = self.rest.plugin

        # retrieves the resources manager plugin
        resources_manager_plugin = rest_plugin.resources_manager_plugin

        # retrieves the debug level
        debug_level = resources_manager_plugin.get_resource("system.debug.level")

        # in case the debug level does meet the required
        # level returns valid otherwise return not valid
        if debug_level and debug_level.data >= minimum_level: return True
        else: return False

    def is_flushed(self):
        """
        Checks if the current rest request has already been flushed
        meaning that the data has already been sent to the output stream.

        In case the data has been already flushed, care should be taken
        to avoid any inconsistent state (double data flush).

        @rtype: bool
        @return: If the current rest request has already been flushed and
        the data sent to the output stream.
        """

        return self.flushed

    def flush(self):
        """
        Flushes the rest request buffer, this operation should
        generate all the required information (partial generation)
        and send it to the underlying request object.

        This is a potentially costy operation so it should be called
        with care (and not very often).
        """

        # in case there is a session available, must try to update the
        # cookie associated information in the response
        if self.session:
            # runs the flush operation in the currently associated session
            # so that the complete data is store in the data source and may
            # be accessed in further/future requests
            self.session.flush()

            # retrieves the session cookie, this is a structure
            # that represents the cookie allowing some manage
            session_cookie = self.session.get_cookie()

            # in case there is a session cookie and the
            # the request is set to allow setting of cookies
            # (provides extra security on single domain access)
            if session_cookie and self.request.allow_cookies:
                # serializes the session cookie into the appropriate
                # representation to be set
                serialized_session_cookie = session_cookie.serialize()

                # sets the session id in the cookie and then invalidates
                # it so that no extra cookies are set
                self.request.append_header("Set-Cookie", serialized_session_cookie)
                self.session.set_cookie(None)

        # sets the content type for the request, this should
        # be able to asset the correct content type in the
        # target request object
        self.request.content_type = self.content_type

        # writes the result translated and flushes the
        # request, sending the output to the client
        self.request.write(self.result_translated)
        self.request.flush()

        # updates the flushed flag so that any consumer object
        # is able to identify if contents have already been flushed
        self.flushed = True

    def redirect(
        self,
        target_path,
        status_code = 302,
        quote = True,
        keep = False,
        attributes_map = None
    ):
        """
        Redirects the request logically, so it becomes readable
        as a new resource. This redirection process uses the
        standard http process for redirection.

        An optional attributes map may be used to use
        url parameters in the redirect.

        @type target_path: String
        @param target_path: The target path of the redirection.
        @type status_code: int
        @param status_code: The status code to be used.
        @type quote: bool
        @param quote: If the target path should be quoted.
        @type keep: bool
        @param keep: If the attributes map from the current request
        should be propagated (as get parameters) to the redirection
        action that is going to be triggered.
        @type attributes_map: Dictionary
        @param attributes_map: Map containing the series of
        attributes to be sent over the target path in the
        redirect url.
        """

        # in case no attributes map is passed uses the current request's
        # attribute map, by default the attributes map is re-used for the
        # redirect operation (no side effects should occur)
        base_map = self.request.attributes_map if keep else {}
        attributes_map = attributes_map or base_map

        # quotes the target path according to the url quoting schema
        # in case the quote flat is set
        target_path_quoted = quote and\
            colony.quote(target_path, "/") or target_path

        # creates the final target path using the attributes
        # map in case they are present (by appending them to
        # the target path) otherwise (in case no attributes map
        # is present) the target path is used
        target_path_quoted = attributes_map and\
            target_path_quoted + "?" +\
            colony.url_encode(attributes_map) or\
            target_path_quoted

        # checks if the current request is "marked" as asynchronous, for
        # such cases a special redirection process is applies to avoid the
        # typical problems with automated redirection using "ajax"
        is_async = True if self.get_attribute("async") else False
        if is_async: status_code = 280

        # sets the status code, that was defined as the argument
        # this status code should represent a redirect
        self.request.status_code = status_code

        # sets the location header (using the quoted target path)
        self.request.set_header("Location", target_path_quoted)

    def execute_background(self, callable, retries = 0, timeout = 0.0, timestamp = None):
        """
        Executes the given callable object in a background
        thread.
        This method is useful for avoid blocking the request
        handling method in non critic tasks.

        @type callable: Callable
        @param callable: The callable to be called in background.
        @type retries: int
        @param retries: The number of times to retry executing the
        callable in case exception is raised.
        @type timeout: float
        @param timeout: The time to be set in between calls of the
        callable, used together with the retry value.
        @type timestamp: float
        @param timestamp: The unix second based timestamp for the
        first execution of the callable.
        """

        self.request.execute_background(
            callable,
            retries = retries,
            timeout = timeout,
            timestamp = timestamp
        )

    def allow_cookies(self):
        """
        Allows the setting of cookies through the typical http
        header technique.

        This technique may prove to be not required for simple
        non interactive user agents.
        """

        self.request.allow_cookies()

    def deny_cookies(self):
        """
        Denies the setting of cookies through the typical http
        header technique.

        This technique may prove to be not required for simple
        non interactive user agents.
        """

        self.request.deny_cookies()

    def get_header(self, header_name):
        """
        Retrieves an header value of the request,
        or none if no header is defined for the given
        header name.

        @type header_name: String
        @param header_name: The name of the header to be retrieved.
        @rtype: Object
        @return: The value of the request header.
        """

        return self.request.get_header(header_name)

    def set_header(self, header_name, header_value):
        """
        Set a response header value on the request.

        @type header_name: String
        @param header_name: The name of the header to be set.
        @type header_value: Object
        @param header_value: The value of the header to be sent
        in the response.
        """

        self.request.set_header(header_name, header_value)

    def set_max_age(self, max_age):
        """
        Sets the max age attribute to be used by the cache
        infra-structure on the client side.

        @type max_age: int
        @param max_age: The maximum age in seconds for the
        returned value to be cached in the client side.
        """

        self.request.set_max_age(max_age)

    def get_attributes_list(self):
        """
        Retrieves the list of available attribute names.

        @rtype: List
        @return: The list of available attribute names.
        """

        return self.request.get_attributes_list()

    def get_attribute(self, attribute_name):
        """
        Retrieves the attribute for the given attribute name.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to retrieve.
        @rtype: Object
        @return: The value of the retrieved attribute.
        """

        return self.request.get_attribute(attribute_name)

    def set_attribute(self, attribute_name, attribute_value):
        """
        Sets the attribute with the given name with the given
        value.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to set.
        @type attribute_value: Object
        @param attribute_value: The value to set the attribute.
        """

        self.request.set_attribute(attribute_name, attribute_value)

    def get_parameter(self, parameter_name):
        """
        Retrieves the parameter for the given parameter name.

        This parameter should be used to compute temporary
        data (not for long term storage).

        @type parameter_name: String
        @param parameter_name: The name of the parameter to retrieve.
        @rtype: Object
        @return: The value of the retrieved parameter.
        """

        return self.parameters_map.get(parameter_name, None)

    def set_parameter(self, parameter_name, parameter_value):
        """
        Sets the parameter with the given name with the given
        value.

        This parameter should be used to compute temporary
        data (not for long term storage).

        @type parameter_name: String
        @param parameter_name: The name of the parameter to set.
        @type parameter_value: Object
        @param parameter_value: The value to set the parameter.
        """

        self.parameters_map[parameter_name] = parameter_value

    def get_session_attributes_map(self):
        """
        Retrieves the session attributes map.
        In case the session is not defined the default (empty)
        attributes map is returned.

        @rtype: Dictionary
        @return: The session attributes map.
        """

        # retrieves the session attributes map in case the session
        # is defined otherwise retrieves the default map
        session_attributes_map = self.session and self.session.attributes_map or {}

        # returns the session attributes map
        return session_attributes_map

    def get_plugin_manager(self):
        """
        Retrieves the plugin manager for the context
        of the rest request.

        @rtype: PluginManager
        @return: The plugin manager for the context
        of the rest request.
        """

        # retrieves the rest plugin and then
        # uses it to retrieve the plugin manager
        rest_plugin = self.rest.plugin
        plugin_manager = rest_plugin.manager

        # retrieves the plugin manager for the current context
        return plugin_manager

    def get_request(self):
        """
        Retrieves the associated request.

        @rtype: Request
        @return: The associated request.
        """

        return self.request

    def set_request(self, request):
        """
        Sets the associated request.

        @type request: Request
        @param request: The associated request.
        """

        self.request = request

    def get_s(self, name, default = None, unset = False):
        """
        Retrieves the value of the session attribute with the
        provided name. The session that is going to be used is
        the one currently associated/loaded to the request.

        An optional parameter may unset the variable afterwards
        if that's required.

        @type name: String
        @param name: The name of the session attribute that is
        going to be retrieved.
        @type default: Object
        @param default: The default value to be returned in case no
        session is found or no value is retrieved from the currently
        set session (fallback value).
        @type unset: bool
        @param unset: If the session attribute should be unset
        or removed from the session after the retrieval.
        @rtype: Object
        @return: The value (as an object) for the requested session
        attribute according to the provided name.
        """

        session = self.get_session()
        if not session: return default
        value = session.get_attribute(name, default = default)
        if unset: session.unset_attribute(name)
        return value

    def set_s(self, name, value):
        """
        Sets a session attribute with the provided name with
        the value that is given.

        This method is provided as a shortcut to quickly access
        the session associated with the request.

        @type name: String
        @param name: The name that is going to be given to the
        session parameter to be set.
        @type value: Object
        @param value: The value to be set in the target session
        attribute to be changed/created.
        """

        session = self.get_session()
        if not session: return None
        session.set_attribute(name, value)

    def unset_s(self, name):
        """
        Unsets the session attribute so that it becomes no longer
        accessible from a session point of view.

        @type name: String
        @param name: The name of the session attribute that is going
        to be unset from session and become unavailable.
        """

        session = self.get_session()
        if not session: return
        session.unset_attribute(name)

    def get_session(self, block = True):
        """
        Retrieves the associated session.

        @type block: bool
        @param block: If the lock should be
        used while accessing the session.
        @rtype: RestSession
        @return: The associated session.
        """

        # in case the session is not set or the
        # block (lock) flag is not set the
        # session may be returned immediately
        if not self.session or not block:
            # returns the session immediately,
            # no need to run through blocking
            return self.session

        # locks the current session to avoid
        # any erroneous modification
        self.session.lock()

        try:
            # saves the current session into
            # a local variable for "safe" return
            session = self.session
        finally:
            # releases the session lock allowing
            # usage by other thread
            self.session.release()

        # returns the "just" retrieved session
        # in a safe manner (run through lock)
        return session

    def set_session(self, session):
        """
        Sets the associated session.

        @type session: RestSession
        @param session: The associated session.
        """

        self.session = session

    def lock_session(self):
        """
        Locks the session so that any subsequent access to
        the underlying logic will block the call.
        """

        # in case no session is defined the control
        # returns immediately to the caller
        if not self.session: return

        # runs the lock operation on the session object
        # blocking any future accesses to the session
        self.session.lock()

    def release_session(self):
        """
        Releases the lock for the access to the session, any
        subsequent access to the session will be "allowed".
        """

        # in case no session is defined the control
        # returns immediately to the caller
        if not self.session: return

        # runs the release operation on the session object
        # allowing any future accesses to the session
        self.session.release()

    def reset_session(self):
        """
        Resets the session present in the current rest request,
        to reset the session is to unset it from the rest request.

        This method is useful for situation where a new session
        context is required or one is meant to be created always.
        """

        # "saves" the session into a temporary
        # attribute so that the session may
        # be removed from the current request
        session = self.session

        # locks the current session to avoid
        # any erroneous modification
        session.lock()

        try:
            # resets the session in the current
            # rest request (removes it from request)
            self.session = None
        finally:
            # releases the session lock allowing
            # usage by other thread
            session.release()

    def get_type(self):
        """
        Retrieves the content type for the current rest request
        using the associated header and processing it.

        @rtype: String
        @return: The content type value (base value) for the
        current request.
        """

        # retrieves the content type header from the current rest request
        # the treats it in case it's a valid content type and returns it
        # to the caller method
        content_type = self.get_header("Content-Type")
        content_type = content_type and content_type.split(";")[0].strip() or None
        return content_type

    def get_resource_name(self):
        """
        Retrieves the resource name.

        @rtype: String
        @return: The resource name.
        """

        return self.resource_name

    def set_resource_name(self, resource_name):
        """
        Sets the resource name.

        @type resource_name: String
        @param resource_name: The resource name.
        """

        self.resource_name = resource_name

    def get_path_list(self):
        """
        Retrieves the path list.

        @rtype: List
        @return: The path list.
        """

        return self.path_list

    def set_path_list(self, path_list):
        """
        Sets the path list.

        @type path_list: String
        @param path_list: The path list.
        """

        self.path_list = path_list

    def get_encoder_name(self):
        """
        Retrieves the encoder name.

        @rtype: String
        @return: The encoder name.
        """

        return self.encoder_name

    def set_encoder_name(self, encoder_name):
        """
        Sets the encoder name.

        @type encoder_name: String
        @param encoder_name: The encoder name.
        """

        self.encoder_name = encoder_name

    def get_content_type(self):
        """
        Retrieves the content type.

        @rtype: String
        @return: The content type.
        """

        return self.content_type

    def set_content_type(self, content_type, flush = False):
        """
        Sets the content type, in case the flush
        flag is set the content type is immediately
        set on the current target request.

        @type content_type: String
        @param content_type: The content type.
        @type flush: bool
        @param flush: If the content type should be
        immediately set on the target request object
        (underlying layer of abstraction).
        """

        self.content_type = content_type
        if flush: self.request.content_type = content_type

    def get_result_translated(self):
        """
        Retrieves the result translated.

        @rtype: String
        @return: The result translated.
        """

        return self.result_translated

    def set_result_translated(self, result_translated):
        """
        Sets the result translated.

        @type result_translated: String
        @param result_translated: The result translated.
        """

        self.result_translated = result_translated

    def get_rest_encoder_plugins(self):
        """
        Retrieves the rest encoder plugins.

        @rtype: List
        @return: The rest encoder plugins.
        """

        return self.rest_encoder_plugins

    def set_rest_encoder_plugins(self, rest_encoder_plugins):
        """
        Sets the rest encoder plugins.

        @type rest_encoder_plugins: List
        @param rest_encoder_plugins: The rest encoder plugins.
        """

        self.rest_encoder_plugins = rest_encoder_plugins

    def get_rest_encoder_plugins_map(self):
        """
        Retrieves the rest encoder plugins map.

        @rtype: Dictionary
        @return: The rest encoder plugins map.
        """

        return self.set_rest_encoder_plugins_map

    def set_rest_encoder_plugins_map(self, set_rest_encoder_plugins_map):
        """
        Sets the rest encoder plugins.

        @type set_rest_encoder_plugins_map: Dictionary
        @param set_rest_encoder_plugins_map: The rest encoder plugins map.
        """

        self.set_rest_encoder_plugins_map = set_rest_encoder_plugins_map

    def get_status_code(self):
        """
        Retrieves the status code.

        @rtype: int
        @return: The status code.
        """

        return self.request.status_code

    def set_status_code(self, status_code):
        """
        Sets the status code.

        @type status_code: int
        @param status_code: The status code.
        """

        self.request.status_code = status_code

    def set_delayed(self, value):
        """
        Sets the request as delayed, this should avoid automatic
        processing of the request (response sending).

        If the delayed mode is set an additional call to the
        process method is required to flush the data to the
        client side.

        @type value: bool
        @param value: The boolean value for the setting of
        the delayed mode flag.
        """

        self.request.delayed = value

    def get_service(self):
        """
        Retrieves the reference to the service responsible for
        the handling of the current request (owner).

        @rtype: Service
        @return: The service responsible for the handling of
        the current request.
        """

        return self.request.get_service()

    def get_service_connection(self):
        """
        Retrieves the reference to the service connection
        associated with the handling of the request.

        @rtype: ServiceConnection
        @return: The reference to the service connection
        associated with the handling of the request.
        """

        return self.request.get_service_connection()

    def get_address(self):
        """
        Retrieves the (ip) address of the service connection
        associated with the rest request.

        @rtype: String
        @return: The (ip) address of the service connection.
        """

        # retrieves the service connection for the request,
        # unpacks the connection address into the address
        service_connection = self.request.service_connection
        address = service_connection.connection_address[0]
        return address

    def get_port(self):
        """
        Retrieves the (tcp) port of the service connection
        associated with the rest request.

        @rtype: String
        @return: The (tcp) port of the service connection.
        """

        # retrieves the service connection for the request,
        # unpacks the connection port into the port
        service_connection = self.request.service_connection
        port = service_connection.connection_address[1]
        return port

    def field(self, name, default = None, cast = None, split = False, token = ","):
        controller = self._get_controller()
        if not controller: return default
        return controller.get_field(
            self,
            name,
            default = default,
            cast_type = cast,
            split = split,
            token = token
        )

    def form(self, name, default = None, cast = None, required = False):
        controller = self._get_controller()
        if not controller: return default
        form_data = controller.process_form_data(self)
        if required and not name in form_data: raise ValueError("%s not found" % name)
        value = form_data.get(name, default)
        if cast and not value in (None, ""): value = cast(value)
        return value

    def _update_session_cookie(self):
        """
        Updates the current session.
        This method retrieves information from the cookie to
        update the session based in the session id.
        """

        # in case there's already a loaded session for
        # the current rest request returns immediately
        if self.session: return

        # retrieves the cookie value from the request
        cookie_value = self.request.get_header("Cookie")

        # in case there is not valid cookie value,
        # must return immediately
        if not cookie_value: return

        # creates a new cookie, using the header value of
        # it and then parses it to populate the attributes
        cookie = Cookie(cookie_value)
        cookie.parse()

        # retrieves the session id
        session_id = cookie.get_attribute("session_id")

        # in case there is no session id defined in the
        # current cookie, must return immediately
        if not session_id: return

        # tries to retrieve the session from the session id
        # this value may be invalid (not set) in case no
        # session could be retrieved from session id
        self.session = self.rest.get_session(session_id)

        # if no session is selected, raises an invalid session
        # exception to indicate the error
        if not self.session: raise exceptions.InvalidSession(
            "no session started or session timed out"
        )

    def _update_session_attribute(self):
        """
        Updates the current session.
        This method retrieves information from the attribute to
        update the session based in the session id.
        """

        # in case there's already a loaded session for
        # the current rest request returns immediately
        if self.session: return

        # retrieves the session id attribute value from the request
        session_id = self.request.get_attribute("session_id")

        # in case there is no valid session id
        # returns immediately
        if not session_id: return

        # retrieves the session from the session id and if
        # no session is selected, raises an invalid session
        # exception to indicate the error
        self.session = self.rest.get_session(session_id)
        if not self.session: raise exceptions.InvalidSession(
            "no session started or session timed out"
        )

    def _get_controller(self):
        """
        Tries to retrieve an underlying controller object
        for the current request.

        The controller value may or may not be defined and
        so a calling to this method is required to avoid
        any exception raising.

        @rtype: Controller
        @return: The controller retrieved from the current
        request instance, or an invalid value in case it was
        not possible to find it.
        """

        if not hasattr(self, "controller"): return None
        return self.controller

    def _get_domain(self):
        """
        Retrieves the domain using the http request header
        host value.

        @rtype: String
        @return: The currently used domain.
        """

        # retrieves the host value from the request headers
        host = self.request.get_header("Host")

        # in case the host is not defined, returns an invalid
        # value immediately, can't parse any value
        if not host: return None

        # retrieves the domain removing the port part
        # of the host value
        domain = host.rsplit(":", 1)[0]

        # returns the domain
        return domain

class RestSession(object):
    """
    The rest session class, defining the abstract interfaces
    that should be used by any of the concrete session
    implementations that are going to be created at runtime.
    """

    session_id = None
    """ The session id used to securely identify each
    session, this value should be secure enough to avoid
    session tampering (could pose a security risk) """

    timeout = None
    """ The timeout value in seconds for the session, this
    value is going to be used as the basis for the calculus
    of the expire time """

    maximum_timeout = None
    """ The maximum timeout value consisting of an hard value
    on until when the session may be extended using the typical
    touch mechanism """

    expire_time = None
    """ The expire time as seconds since epoch from which the
    session is going to be considered expired and removed from
    the associated storage mechanism """

    cookie = None
    """ The cookie structure associated with the session this
    structure is going to be used in serialization """

    attributes_map = {}
    """ The attributes map, that should be accessible much
    like a map using the set and get base interaction """

    _maximum_expire_time = None
    """ The maximum expire time, calculates using the provided
    maximum timeout value and should be an epoch based value """

    _access_lock = None
    """ The lock used to control the access to the session, this
    is required to avoid concurrent access the the session """

    def __init__(
        self,
        session_id = None,
        timeout = DEFAULT_TIMEOUT,
        maximum_timeout = DEFAULT_MAXIMUM_TIMEOUT
    ):
        """
        Constructor of the class.

        @type session_id: String
        @param session_id: The session id.
        @type timeout: float
        @param timeout: The timeout.
        @type maxmimum_timeout: float
        @param maxmimum_timeout: The maximum timeout.
        """

        self.session_id = session_id
        self.timeout = timeout
        self.maximum_timeout = maximum_timeout

        self.attributes_map = {}

        self._access_lock = threading.RLock()

        # generates the expire time from the
        # current time and the given timeout
        # and maximum timeout
        self._generate_expire_time(timeout, maximum_timeout)

    def __getstate__(self):
        return dict(
            session_id = self.session_id,
            timeout = self.timeout,
            maximum_timeout = self.maximum_timeout,
            expire_time = self.expire_time,
            attributes_map = self.attributes_map,
            _maximum_expire_time = self._maximum_expire_time
        )

    def __setstate__(self, state):
        self.session_id = state["session_id"]
        self.timeout = state["timeout"]
        self.maximum_timeout = state["maximum_timeout"]
        self.expire_time = state["expire_time"]
        self.attributes_map = state["attributes_map"]
        self._maximum_expire_time = state["_maximum_expire_time"]
        self._access_lock = threading.RLock()

    @classmethod
    def load(cls):
        cls.STORAGE = {}
        cls.GC_PENDING = True

    @classmethod
    def unload(cls):
        cls.STORAGE = None
        cls.GC_PENDING = False

    @classmethod
    def clear(cls):
        cls.STORAGE.clear()

    @classmethod
    def count(cls):
        return len(cls.STORAGE)

    @classmethod
    def new(cls, *args, **kwargs):
        if not cls.STORAGE: cls.load()
        session = cls(*args, **kwargs)
        cls.STORAGE[session.session_id] = session
        return session

    @classmethod
    def get_s(cls, sid):
        if not cls.STORAGE: cls.load()
        if cls.GC_PENDING: cls.gc()
        session = cls.STORAGE.get(sid, None)
        if not session: return session
        is_expired = session.is_expired()
        if is_expired: cls.expire(sid)
        session = None if is_expired else session
        return session

    @classmethod
    def expire(cls, sid):
        del cls.STORAGE[sid]

    @classmethod
    def gc(cls):
        cls.GC_PENDING = False
        for sid in cls.SHELVE:
            session = cls.SHELVE.get(sid, None)
            is_expired = session.is_expired()
            if is_expired: cls.expire(sid)

    def update(self, domain = None, include_sub_domain = False, secure = False):
        self.start(
            domain = domain,
            include_sub_domain = include_sub_domain,
            secure = secure
        )

    def start(self, domain = None, include_sub_domain = False, secure = False):
        """
        Starts the current session.

        @type domain: String
        @param domain: The domain to be used by the cookie.
        @type include_sub_domain: bool
        @param include_sub_domain: Controls if the sub domain should be included.
        @type secure: bool
        @param secure: Controls if the cookie should be considered secure,
        and only available through secure connections.
        """

        current_timestamp = time.time()
        current_timestamp += DEFAULT_EXPIRATION_DELTA_TIMESTAMP
        current_date_time = datetime.datetime.utcfromtimestamp(current_timestamp)
        current_date_time_formatted = current_date_time.strftime(DATE_FORMAT)

        self.cookie = Cookie()
        self.cookie.set_main_attribute_name("session_id")
        self.cookie.set_attribute("session_id", self.session_id)
        self.cookie.set_attribute("lang", DEFAULT_LANG_VALUE)
        self.cookie.set_attribute("expires", current_date_time_formatted)

        self._set_domain(domain, include_sub_domain)
        self._set_secure(secure)

    def stop(self, domain = None, include_sub_domain = False, secure = False):
        """
        Stops the current session.

        @type domain: String
        @param domain: The domain used by the cookie.
        @type include_sub_domain: bool
        @param include_sub_domain: Controls if the sub domain should be included.
        @type secure: bool
        @param secure: Controls if the cookie should be considered secure,
        and only available through secure connections.
        """

        self.session_id = None

        self.cookie = Cookie()
        self.cookie.set_main_attribute_name("session_id")
        self.cookie.set_attribute("session_id", "")
        self.cookie.set_attribute("lang", DEFAULT_LANG_VALUE)
        self.cookie.set_attribute("expires", DEFAULT_EXPIRATION_DATE)

        self._set_domain(domain, include_sub_domain)
        self._set_secure(secure)

    def update_expire_time(self):
        """
        Updates the expire time value according
        to the currently defined timeout and
        maximum timeout values.
        """

        self._generate_expire_time(self.timeout, self.maximum_timeout)

    def lock(self):
        """
        Locks the session so that any subsequent access to
        the underlying logic will block the call.
        """

        self._access_lock.acquire()

    def release(self):
        """
        Releases the lock for the access to the session, any
        subsequent access to the session will be "allowed".
        """

        self._access_lock.release()

    def flush(self):
        pass

    def is_expired(self):
        return time.time() > self.expire_time

    def get_session_id(self):
        return self.session_id

    def set_session_id(self, session_id):
        self.session_id = session_id

    def get_timeout(self):
        return self.timeout

    def set_timeout(self, timeout):
        self.timeout = timeout

    def get_maximum_timeout(self):
        return self.maximum_timeout

    def set_maximum_timeout(self, maximum_timeout):
        self.maximum_timeout = maximum_timeout

    def get_expire_time(self):
        return self.expire_time

    def set_expire_time(self, expire_time):
        self.expire_time = expire_time

    def get_cookie(self):
        return self.cookie

    def set_cookie(self, cookie):
        self.cookie = cookie

    def get_attribute(self, attribute_name, default = None):
        """
        Retrieves the attribute value for the given
        attribute name. Note that it's possible to provide
        a default value so that such value is returned when
        no value is found in the current session.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to retrieve.
        @type default: Object
        @param default: The fallback value to be returned when no
        value is found for the provided name.
        @rtype: Object
        @return: The retrieved attribute value according to the
        provided name (as defined in specification).
        """

        return self.attributes_map.get(attribute_name, default)

    def set_attribute(self, attribute_name, attribute_value):
        """
        Sets the attribute with the given name with the
        provided value.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to set.
        @type attribute_value: String
        @param attribute_value: The attribute value to set.
        """

        self.attributes_map[attribute_name] = attribute_value

    def unset_attribute(self, attribute_name):
        """
        Unsets the attribute with the given name.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to unset.
        """

        # in case the attribute name exists in
        # the attributes map must unset it from
        # the exiting attributes map
        if attribute_name in self.attributes_map:
            del self.attributes_map[attribute_name]

    def get_attributes_map(self):
        """
        Retrieves the attributes map.

        @rtype: Dictionary
        @return: The attributes map.
        """

        return self.attributes_map

    def set_attributes_map(self, attributes_map):
        """
        Sets the attributes map.

        @type attributes_map: Dictionary
        @param attributes_map: The attributes map.
        """

        self.attributes_map = attributes_map

    def _set_domain(self, domain, include_sub_domain = False):
        """
        Sets the domain "attributes" in the session cookie.

        An optional include sub domains attribute may be used
        to allow the cookie to be propagated to sub domains
        (by default it's disabled).

        @type domain: String
        @param domain: The domain used by the cookie.
        @type include_sub_domain: bool
        @param include_sub_domain: Controls if the sub domain should be included.
        """

        # in case the domain is not defined defined
        # should return immediately
        if not domain: return

        # sets the domain in the cookie
        self.cookie.set_attribute("path", "/")

        # in case the domain is local, returns immediately
        # to avoid problems in the browser
        if domain in LOCALHOST_VALUES: return

        # in case the domain is "valid" and sub domains
        # flag is active, sets the domain in the cookie
        # (including sub domains) otherwise sets only the
        # current domain in the cookie
        if include_sub_domain: self.cookie.set_attribute(DOMAIN_VALUE, "." + domain)
        else: self.cookie.set_attribute(DOMAIN_VALUE, domain)

    def _set_secure(self, secure = False):
        """
        Sets the secure "attributes" in the session cookie.

        An optional include sub domains may be used to allow
        the cookie to be propagated to sub domains (by default
        it's disabled).

        @type secure: bool
        @param secure: Flag that controls if the cookie should
        be considered secure.
        """

        # in case the secure flag is set adds the simple secure
        # attribute to the cookie
        if secure: self.cookie.set_attribute(SECURE_VALUE)

    def _generate_expire_time(self, timeout, maximum_timeout):
        """
        Generates the expire time value from the
        given timeout value using the current
        time.
        The maximum timeout is used to control the generated
        expire time, and for calculation of the maximum expire time.

        @type timeout: float
        @param timeout: The timeout value to be
        used for expire time generation.
        @type maximum_timeout: float
        @param maximum_timeout: The maximum timeout value to be
        used to control the new expire time.
        """

        # retrieves the current time for
        # expire time calculation
        current_time = time.time()

        # calculates the maximum expire time in case it's not defined
        # as the sum of the current time and the maximum timeout
        if not self._maximum_expire_time:
            self._maximum_expire_time = current_time + maximum_timeout

        # calculates the expire time incrementing
        # the timeout to the current time
        expire_time = current_time + timeout

        # sets the expire time as the calculated expire time
        # or as the maximum expire time in case it's smaller
        self.expire_time = expire_time if self._maximum_expire_time > expire_time\
            else self._maximum_expire_time

class ShelveSession(RestSession):
    """
    Shelve based implementation of the rest session, meant
    to provide a minimal and simple persistence layer for
    the sessions to be created.
    """

    @classmethod
    def load(cls, file_path = "session.shelve"):
        super(ShelveSession, cls).load()
        base_path = colony.conf("SESSION_BASE_PATH", "")
        file_path = os.path.join(base_path, file_path)
        cls.SHELVE = shelve.open(
            file_path,
            protocol = 2,
            writeback = True
        )

    @classmethod
    def unload(cls):
        super(ShelveSession, cls).unload()
        cls.SHELVE.close()
        cls.SHELVE = None

    @classmethod
    def clear(cls):
        cls.SHELVE.clear()

    @classmethod
    def count(cls):
        return len(cls.SHELVE)

    @classmethod
    def new(cls, *args, **kwargs):
        if not cls.SHELVE: cls.load()
        session = cls(*args, **kwargs)
        cls.SHELVE[session.session_id] = session
        return session

    @classmethod
    def get_s(cls, sid):
        if not cls.SHELVE: cls.load()
        if cls.GC_PENDING: cls.gc()
        session = cls.SHELVE.get(sid, None)
        if not session: return session
        is_expired = session.is_expired()
        if is_expired: cls.expire(sid)
        session = None if is_expired else session
        return session

    @classmethod
    def expire(cls, sid):
        del cls.SHELVE[sid]

    @classmethod
    def gc(cls):
        cls.GC_PENDING = False
        for sid in cls.SHELVE:
            session = cls.SHELVE.get(sid, None)
            is_expired = session.is_expired()
            if is_expired: cls.expire(sid)

    def flush(self):
        cls = self.__class__
        cls.SHELVE.sync()

class Cookie(object):
    """
    The cookie class representing an http cookie.
    """

    string_value = None
    """ The string value """

    main_attribute_name = None
    """ The main attribute name """

    attributes_map = {}
    """ The attributes map """

    def __init__(self, string_value = None):
        """
        Constructor of the class.

        @type string_value: String
        @param string_value: The cookie string value.
        """

        self.string_value = string_value

        self.attributes_map = {}

    def parse(self):
        """
        Parses the string value creating the attributes
        map, with all the name and values association.
        """

        # in case the string value is invalid, raises an invalid
        # cookie exception to indicate the parsing problem
        if self.string_value == None:
            raise exceptions.InvalidCookie("invalid cookie string value")

        # retrieves the value pairs by splitting the
        # string value
        value_pairs = self.string_value.split(";")

        # iterates over all the value pairs to
        # retrieve the name and value pairs
        for value_pair in value_pairs:
            # strips the value pair to remove
            # extra white spaces
            value_pair_stripped = value_pair.strip()

            # splits the value pair
            value_splitted = value_pair_stripped.split("=")

            # in case the value pairs does respect
            # the key value
            if len(value_splitted) == 2:
                # retrieves the name and the value
                name, value = value_splitted
            else:
                # sets the name as the first element
                # and the value as an invalid value
                name = value_splitted[0]
                value = None

            # sets the value in the attributes map
            self.attributes_map[name] = value

    def serialize(self):
        """
        Serializes the cookie into a string value, using
        the current attributes map.

        @rtype: String
        @return: The linear version of the cookie as default
        serialized value according to http specification.
        """

        # starts the string value
        string_value = str()

        # in case the main attribute name exists and exists in the
        # attributes map
        if self.main_attribute_name and self.main_attribute_name in self.attributes_map:
            # retrieves the main attribute value
            main_attribute_value = self.attributes_map[self.main_attribute_name]

            # serializes the main attribute
            serialized_attribute = self._serialize_attribute(
                self.main_attribute_name,
                main_attribute_value
            )

            # appends the serialized attribute to the string value
            string_value += serialized_attribute

        # iterates over all the attribute name and value in
        # the attributes map
        for attribute_name, attribute_value in self.attributes_map.items():
            # in case the attribute is not the main one
            if not attribute_name == self.main_attribute_name:
                # serializes the attribute
                serialized_attribute = self._serialize_attribute(attribute_name, attribute_value)

                # appends the serialized attribute to the string value
                string_value += serialized_attribute

        # returns the string value, representing the serialized version
        # of the cookie as per http specification
        return string_value

    def get_attribute(self, attribute_name):
        """
        Retrieves an attribute using the attribute name.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to retrieve.
        """

        return self.attributes_map.get(attribute_name, None)

    def set_attribute(self, attribute_name, attribute_value = None):
        """
        Retrieves an attribute using the attribute name.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to set.
        @type attribute_value: Object
        @param attribute_value: The value of the attribute to set.
        """

        self.attributes_map[attribute_name] = attribute_value

    def set_main_attribute_name(self, main_attribute_name):
        """
        Sets the main attribute name.

        @type main_attribute_name: String
        @param main_attribute_name: The main attribute name.
        """

        self.main_attribute_name = main_attribute_name

    def _serialize_attribute(self, attribute_name, attribute_value = None):
        """
        Serializes the given attribute (name and value) into
        a valid cookie string.

        In case no attribute value is provided the attribute
        is considered to be singleton no equal sign.

        @type attribute_name: String
        @param attribute_name: The name of the attribute to be serialized.
        @type attribute_value: Object
        @param attribute_value: The of the attribute to be serialized.
        @rtype: String
        @return: The cookie serialized string.
        """

        # converts the attribute into the correct key value
        # pair defaulting to a single name attribute in case
        # no value is defined
        if attribute_value == None: return attribute_name + ";"
        else: return attribute_name + "=" + str(attribute_value) + ";"
