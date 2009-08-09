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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import socket
import select
import threading
import cStringIO

import main_service_telnet_exceptions

HOST_VALUE = ""
""" The host value """

CLIENT_CONNECTION_TIMEOUT = 1
""" The client connection timeout """

REQUEST_TIMEOUT = 60
""" The request timeout """

CHUNK_SIZE = 4096
""" The chunk size """

NUMBER_THREADS = 15
""" The number of threads """

MAX_NUMBER_THREADS = 30
""" The maximum number of threads """

SCHEDULING_ALGORITHM = 2
""" The scheduling algorithm """

DEFAULT_PORT = 23
""" The default port """

class MainServiceTelnet:
    """
    The main service telnet class.
    """

    main_service_telnet_plugin = None
    """ The main service telnet plugin """

    telnet_socket = None
    """ The telnet socket """

    telnet_connection_active = False
    """ The telnet connection active flag """

    telnet_client_thread_pool = None
    """ The telnet client thread pool """

    telnet_connection_close_event = None
    """ The telnet connection close event """

    telnet_connection_close_end_event = None
    """ The telnet connection close end event """

    def __init__(self, main_service_telnet_plugin):
        """
        Constructor of the class.

        @type main_service_telnet_plugin: MainServiceTelnetPlugin
        @param main_service_telnet_plugin: The main service telnet plugin.
        """

        self.main_service_telnet_plugin = main_service_telnet_plugin

        self.telnet_connection_close_event = threading.Event()
        self.telnet_connection_close_end_event = threading.Event()

    def start_service(self, parameters):
        """
        Starts the service with the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        # retrieves the socket provider value
        socket_provider = parameters.get("socket_provider", None)

        # retrieves the port value
        port = parameters.get("port", DEFAULT_PORT)

        # retrieves the service configuration
        #service_configuration = self.main_service_telnet_plugin.get_configuration_property("server_configuration").get_data()

        service_configuration = {}

        # retrieves the socket provider configuration value
        #socket_provider = service_configuration.get("default_socket_provider", socket_provider)

        # retrieves the port configuration value
        #port = service_configuration.get("default_port", port)

        # start the server for the given socket provider, port and encoding
        self.start_server(socket_provider, port, service_configuration)

        # clears the telnet connection close event
        self.telnet_connection_close_event.clear()

        # sets the telnet connection close end event
        self.telnet_connection_close_end_event.set()

    def stop_service(self, parameters):
        """
        Stops the service.

        @type parameters: Dictionary
        @param parameters: The parameters to start the service.
        """

        pass

    def start_server(self, socket_provider, port, service_configuration):
        """
        Starts the server in the given port.

        @type socket_provider: String
        @param socket_provider: The name of the socket provider to be used.
        @type port: int
        @param port: The port to start the server.
        @type service_configuration: Map
        @param service_configuration: The service configuration map.
        """

        # retrieves the thread pool manager plugin
        thread_pool_manager_plugin = self.main_service_telnet_plugin.thread_pool_manager_plugin

        # retrieves the task descriptor class
        task_descriptor_class = thread_pool_manager_plugin.get_thread_task_descriptor_class()

        # creates the telnet client thread pool
        self.telnet_client_thread_pool = thread_pool_manager_plugin.create_new_thread_pool("telnet pool",
                                                                                           "pool to support telnet client connections",
                                                                                           NUMBER_THREADS, SCHEDULING_ALGORITHM, MAX_NUMBER_THREADS)

        # starts the telnet client thread pool
        self.telnet_client_thread_pool.start_pool()

        # sets the telnet connection active flag as true
        self.telnet_connection_active = True

        # in case the socket provider is defined
        if socket_provider:
            # retrieves the socket provider plugins
            socket_provider_plugins = self.main_service_telnet_plugin.socket_provider_plugins

            # iterates over all the socket provider plugins
            for socket_provider_plugin in socket_provider_plugins:
                # retrieves the provider name from the socket provider plugin
                socket_provider_plugin_provider_name = socket_provider_plugin.get_provider_name()

                # in case the names are the same
                if socket_provider_plugin_provider_name == socket_provider:
                    # creates a new telnet socket with the socket provider plugin
                    self.telnet_socket = socket_provider_plugin.provide_socket()

            # in case the socket was not created, no socket provider found
            if not self.telnet_socket:
                raise main_service_telnet_exceptions.SocketProviderNotFound("socket provider %s not found" % socket_provider)
        else:
            # creates the telnet socket
            self.telnet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # sets the socket to be able to reuse the socket
        self.telnet_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # binds the telnet socket
        self.telnet_socket.bind((HOST_VALUE, port))

        # start listening in the telnet socket
        self.telnet_socket.listen(5)

        # loops while the telnet connection is active
        while not self.telnet_connection_close_event.isSet():
            try:
                # sets the socket to non blocking mode
                self.telnet_socket.setblocking(0)

                # starts the select values
                selected_values = ([], [], [])

                # iterates while there is no selected values
                while selected_values == ([], [], []):
                    # in case the connection is closed
                    if self.telnet_connection_close_event.isSet():
                        # closes the telnet socket
                        self.telnet_socket.close()

                        return

                    # selects the values
                    selected_values = select.select([self.telnet_socket], [], [], CLIENT_CONNECTION_TIMEOUT)

                # sets the socket to blocking mode
                self.telnet_socket.setblocking(1)
            except:
                # prints debug message about connection
                self.main_service_telnet_plugin.info("The socket is not valid for selection of the pool")

                return

            # in case the connection is closed
            if self.telnet_connection_close_event.isSet():
                # closes the telnet socket
                self.telnet_socket.close()

                return

            try:
                # accepts the connection retrieving the telnet connection object and the address
                telnet_connection, telnet_address = self.telnet_socket.accept()

                # creates a new telnet client service task, with the given telnet connection, address, encoding and encoding handler
                telnet_client_service_task = TelnetClientServiceTask(self.main_service_telnet_plugin, telnet_connection, telnet_address, service_configuration)

                # creates a new task descriptor
                task_descriptor = task_descriptor_class(start_method = telnet_client_service_task.start,
                                                        stop_method = telnet_client_service_task.stop,
                                                        pause_method = telnet_client_service_task.pause,
                                                        resume_method = telnet_client_service_task.resume)

                # inserts the new task descriptor into the telnet client thread pool
                self.telnet_client_thread_pool.insert_task(task_descriptor)

                self.main_service_telnet_plugin.debug("Number of threads in pool: %d" % self.telnet_client_thread_pool.current_number_threads)
            except Exception, ex:
                print ex
                self.main_service_telnet_plugin.error("Error accepting connection")

        # closes the telnet socket
        self.telnet_socket.close()

class TelnetClientServiceTask:
    """
    The telnet client service task class.
    """

    main_service_telnet_plugin = None
    """ The main service telnet plugin """

    telnet_connection = None
    """ The telnet connection """

    telnet_address = None
    """ The telnet address """

    service_configuration = None
    """ The service configuration """

    encoding_handler = None
    """ The encoding handler """

    def __init__(self, main_service_telnet_plugin, telnet_connection, telnet_address, service_configuration):
        self.main_service_telnet_plugin = main_service_telnet_plugin
        self.telnet_connection = telnet_connection
        self.telnet_address = telnet_address
        self.service_configuration = service_configuration

    def start(self):
        # retrieves the telnet service handler plugins map
        #telnet_service_handler_plugins_map = self.main_service_telnet_plugin.main_service_telnet.telnet_service_handler_plugins_map

        # prints debug message about connection
        self.main_service_telnet_plugin.debug("Connected to: %s" % str(self.telnet_address))

        # sets the request timeout
        request_timeout = REQUEST_TIMEOUT

        while True:
            try:
                # retrieves the request
                request = self.retrieve_request(request_timeout)
            except main_service_telnet_exceptions.MainServiceTelnetException:
                self.main_service_telnet_plugin.debug("Connection: %s closed" % str(self.telnet_address))
                return

            try:
                # prints debug message about request
                self.main_service_telnet_plugin.debug("Handling request: %s" % str(request))

                # handles the request by the request handler
                self.main_service_telnet_plugin.telnet_service_handler_plugins[0].handle_request(request)

                # sends the request to the client (response)
                self.send_request(request)
#
#                # retrieves the service configuration contexts
#                service_configuration_contexts = self.service_configuration["contexts"]
#
#                # starts the request handled
#                request_handled = False
#
#                # iterates over the service configuration context names
#                for service_configuration_context_name, service_configuration_context in service_configuration_contexts.items():
#                    if request.path.find(service_configuration_context_name) == 0:
#                        # sets the request properties
#                        request.properties = service_configuration_context.get("request_properties", {})
#
#                        # sets the handler path
#                        request.handler_path = service_configuration_context_name
#
#                        # retrieves the handler name
#                        handler_name = service_configuration_context["handler"]
#
#                        # sets the request handled flag
#                        request_handled = True
#
#                        # breaks the loop
#                        break
#
#                # in case the request was not already handled
#                if not request_handled:
#                    # retrieves the default handler name
#                    handler_name = self.service_configuration["default_handler"]
#
#                    # sets the handler path
#                    request.handler_path = None
#
#                # handles the request by the request handler
#                telnet_service_handler_plugins_map[handler_name].handle_request(request)
#
#                # sends the request to the client (response)
#                self.send_request(request)
#
#                # in case the connection is meant to be kept alive
#                if self.keep_alive(request):
#                    self.main_service_telnet_plugin.debug("Connection: %s kept alive for %ss" % (str(self.telnet_address), str(request_timeout)))
#                # in case the connection is not meant to be kept alive
#                else:
#                    self.main_service_telnet_plugin.debug("Connection: %s closed" % str(self.telnet_address))
#                    break

            except Exception, exception:
                self.send_exception(request, exception)

        # closes the telnet connection
        self.telnet_connection.close()

    def stop(self):
        # closes the telnet connection
        self.telnet_connection.close()

    def pause(self):
        pass

    def resume(self):
        pass

    def retrieve_request(self, request_timeout = REQUEST_TIMEOUT):
        """
        Retrieves the request from the received message.

        @type request_timeout: int
        @param request_timeout: The timeout for the request retrieval.
        @rtype: TelnetRequest
        @return: The request from the received message.
        """

        # creates the string io for the message
        message = cStringIO.StringIO()

        # creates a request object
        request = TelnetRequest()

        # creates the message size value
        message_size = 0

        # continuous loop
        while True:
            # retrieves the data
            data = self.retrieve_data(request_timeout)

            # in case no valid data was received
            if data == "":
                raise main_service_telnet_exceptions.TelnetInvalidDataException("empty data received")

            # writes the data to the string io
            message.write(data)

            # retrieves the message value from the string io
            message_value = message.getvalue()

            # finds the first new line value
            new_line_index = message_value.find("\r\n")

            # in case there is a new line value found
            if not new_line_index == -1:
                # retrieves the telnet message
                telnet_message = message_value[:new_line_index]

                # sets the telnet message in the request
                request.set_message(telnet_message)

                # returns the request
                return request

    def decode_request(self, request):
        """
        Decodes the request message for the encoding
        specified in the request.

        @type request: TelnetRequest
        @param request: The request to be decoded.
        """

        # start the valid charset flag
        valid_charset = False

        # in case the content type is not defined
        if "Content-Type" in request.headers_map:
            # retrieves the content type
            content_type = request.headers_map["Content-Type"]

            # splits the content type
            content_type_splited = content_type.split(";")

            # iterates over all the items in the content type splited
            for content_type_item in content_type_splited:
                # strips the content type item
                content_type_item_stripped = content_type_item.strip()

                # in case the content is of type multipart form data
                if content_type_item_stripped.startswith(MULTIPART_FORM_DATA_VALUE):
                    return

                # in case the item is the charset definition
                if content_type_item_stripped.startswith("charset"):
                    # splits the content type item stripped
                    content_type_item_stripped_splited = content_type_item_stripped.split("=")

                    # retrieves the content type charset
                    content_type_charset = content_type_item_stripped_splited[1].lower()

                    # sets the valid charset flag
                    valid_charset = True

                    # breaks the cycle
                    break

        # in case there is no valid charset defined
        if not valid_charset:
            # sets the default content type charset
            content_type_charset = DEFAULT_CHARSET

        # retrieves the received message value
        received_message_value = request.received_message

        # re-encodes the message value in the current default encoding
        request.received_message = received_message_value.decode(content_type_charset).encode()

    def retrieve_data(self, request_timeout = REQUEST_TIMEOUT, chunk_size = CHUNK_SIZE):
        try:
            # sets the connection to non blocking mode
            self.telnet_connection.setblocking(0)

            # runs the select in the telnet connection, with timeout
            selected_values = select.select([self.telnet_connection], [], [], request_timeout)

            # sets the connection to blocking mode
            self.telnet_connection.setblocking(1)
        except:
            raise main_service_telnet_exceptions.RequestClosed("invalid socket")

        if selected_values == ([], [], []):
             self.telnet_connection.close()
             raise main_service_telnet_exceptions.ServerRequestTimeout("%is timeout" % request_timeout)
        try:
            # receives the data in chunks
            data = self.telnet_connection.recv(chunk_size)
        except:
            raise main_service_telnet_exceptions.ClientRequestTimeout("timeout")

        return data

    def send_exception(self, request, exception):
        """
        Sends the exception to the given request for the given exception.

        @type request: TelnetRequest
        @param request: The request to send the exception.
        @type exception: Exception
        @param exception: The exception to be sent.
        """

        # sets the request content type
        request.content_type = "text/plain"

        # checks if the exception contains a status code
        if hasattr(exception, "status_code"):
            # sets the status code in the request
            request.status_code = exception.status_code
        # in case there is no status code defined in the exception
        else:
            # sets the internal server error status code
            request.status_code = 500

        # retrieves the value for the status code
        status_code_value = STATUS_CODE_VALUES[request.status_code]

        # writes the header message in the message
        request.write("colony web server - " + str(request.status_code) + " " + status_code_value + "\n")

        # writes the exception message
        request.write("error: '" + str(exception) + "'\n")

        # writes the traceback message in the request
        request.write("traceback:\n")

        # writes the traceback in the request
        formated_traceback = traceback.format_tb(sys.exc_traceback)

        # iterates over the traceback lines
        for formated_traceback_line in formated_traceback:
            request.write(formated_traceback_line)

        # sends the request to the client (response)
        self.send_request(request)

    def send_request(self, request):
        self.send_request_simple(request)

    def send_request_simple(self, request):
        # retrieves the result value
        result_value = request.get_result()

        try:
            # sends the result value to the client
            self.telnet_connection.send(result_value)
        except:
            # error in the client side
            return

    def keep_alive(self, request):
        """
        Retrieves the value of the keep alive for the given request.

        @type request: TelnetRequest
        @param request: The request to retrieve the keep alive value.
        @rtype: bool
        @return: The value of the keep alive for the given request.
        """

        if "Connection" in request.headers_map:
            connection_type = request.headers_map["Connection"]

            if connection_type.lower() == "keep-alive":
                return True
            else:
                return False
        else:
            return False

class TelnetRequest:
    """
    The telnet request class.
    """

    message = "none"
    """ The received message """

    operation_type = "none"
    """ The operation type """

    message_stream = cStringIO.StringIO()
    """ The message stream """

    properties = {}
    """ The properties """

    def __init__(self):
        self.message_stream = cStringIO.StringIO()
        self.properties = {}

    def __repr__(self):
        return "(%s, %s)" % (self.operation_type, self.message)

    def read(self):
        return self.message

    def write(self, message):
        self.message_stream.write(message)

    def get_result(self):
        # retrieves the result string value
        message = self.message_stream.getvalue()

        # creates the return message
        return_message = message + "\r"

        # returns the return message
        return return_message

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message
