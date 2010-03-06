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

import stat
import hashlib
import datetime

import os.path

HANDLER_FILENAME = "none"
""" The handler filename """

FILE_MIME_TYPE_MAPPING = {"html" : "text/html", "txt" : "text/plain", "css" : "text/css",
                          "jpg" : "image/jpg", "png" : "image/png"}
""" The map that relates the file extension and the associated mime type """

EXPIRATION_DELTA_TIMESTAMP = 31536000
""" The expiration delta timestamp """

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"
""" The date format """

SERVER_VALUE = "Server"
""" The server value """

IF_MODIFIED_SINCE_VALUE = "If-Modified-Since"
""" The if modified since value """

IF_NONE_MATCH_VALUE = "If-None-Match"
""" The if none match value """

DEFAULT_MIME_TYPE = "text/plain"
""" The default mime type """

DEFAULT_CHARSET = "Cp1252"
""" The default charset """

LONG_PATH_PREFIX = u"\\\\?\\"
""" The windows long path prefix """

class JavascriptFileHandler:
    """
    The javascript file handler class.
    """

    javascript_file_handler_plugin = None
    """ The javascript file handler plugin """

    def __init__(self, javascript_file_handler_plugin):
        """
        Constructor of the class.

        @type javascript_file_handler_plugin: JavascriptFileHandlerPlugin
        @param javascript_file_handler_plugin: The javascript file handler plugin.
        """

        self.javascript_file_handler_plugin = javascript_file_handler_plugin

    def get_handler_filename(self):
        return HANDLER_FILENAME

    def is_request_handler(self, request):
        # retrieves the simple filename from the complete path filename
        simple_filename = request.uri.split("/")[-1]

        if simple_filename == HANDLER_FILENAME:
            return True
        else:
            return False

    def handle_request(self, request):
        # retrieves the javascript handler plugins
        javascript_handler_plugins = self.javascript_file_handler_plugin.javascript_handler_plugins

        # retrieves the javascript manager plugin
        javascript_manager_plugin = self.javascript_file_handler_plugin.javascript_manager_plugin

        # splits the uri using the "/" character
        uri_splited = request.uri.split("/")

        # retrieves the list o components for the relative path
        relative_path_list = uri_splited[3:]

        # start the relative path string
        relative_path = str()

        # iterates over the list of relative path
        for relative_path_item in relative_path_list:
            relative_path += relative_path_item + "/"

        # retrieves the full path for the file
        full_path = javascript_manager_plugin.get_file_full_path(relative_path)

        # retrieves the current os name
        os_name = os.name

        # in case the current operative system is windows based
        if os_name == "nt" or os_name == "dos":
            # normalizes the full path
            full_path = os.path.normpath(full_path);

            # creates the full path in the windows mode
            full_path = LONG_PATH_PREFIX + full_path

        # retrieves the file extension
        file_extension = full_path.split(".")[-1]

        # retrieves the mime type for the given file
        mime_type = FILE_MIME_TYPE_MAPPING.get(file_extension, DEFAULT_MIME_TYPE)

        # retrieves the file stat
        file_stat = os.stat(full_path)

        # retrieves the modified timestamp
        modified_timestamp = file_stat[stat.ST_MTIME]

        # computes the etag value base in the file stat and
        # modified timestamp
        etag_value = self._compute_etag(file_stat, modified_timestamp)

        # retrieves the if modified header value
        if_modified_header = request.get_header(IF_MODIFIED_SINCE_VALUE)

        # in case the if modified header is defined
        if if_modified_header:
            # converts the if modified header value to date time
            if_modified_header_data_time = datetime.datetime.strptime(if_modified_header, DATE_FORMAT)

            # converts the modified timestamp to date time
            modified_date_time = datetime.datetime.fromtimestamp(modified_timestamp)

            # in case the modified date time is less or the same
            # as the if modified header date time (no modification)
            if modified_date_time <= if_modified_header_data_time:
                # sets the request mime type
                request.content_type = mime_type + ";charset=" + DEFAULT_CHARSET

                # sets the request status code
                request.status_code = 304

                # returns immediately
                return

        # retrieves the if none match value
        if_none_match_header = request.get_header(IF_NONE_MATCH_VALUE)

        # in case the if none header is defined
        if if_none_match_header:
            # in case the value of the if modified heade is the same
            # as the etag value of the file (no modification)
            if if_modified_header == etag_value:
                # sets the request mime type
                request.content_type = mime_type + ";charset=" + DEFAULT_CHARSET

                # sets the request status code
                request.status_code = 304

                # returns immediately
                return

        # calculates the expiration timestamp from the modified timestamp
        # incrementing the delta timestamp for expiration
        expiration_timestamp = modified_timestamp + EXPIRATION_DELTA_TIMESTAMP

        # sets the request status code
        request.status_code = 200

        # sets the last modified timestamp
        request.set_last_modified_timestamp(modified_timestamp)

        # sets the expiration timestamp in the request
        request.set_expiration_timestamp(expiration_timestamp)

        # sets the etag in the request
        request.set_etag(etag_value)

        # opens the file for reading
        file = open(full_path, "rb")

        # reads the file contents
        file_contents = file.read()

        # closes the file
        file.close()

        # sets the content type for the request
        request.content_type = mime_type + ";charset=" + DEFAULT_CHARSET

        # iterates over all the javascript handler plugins
        for javascript_handler_plugin in javascript_handler_plugins:
            # handles the contents to the javascript handler plugin
            file_contents = javascript_handler_plugin.handle_contents(file_contents)

        # writes the file contents to the request
        request.write(file_contents)

        # in case the file is of type js
        if file_extension == "js":
            # writes the file footer
            request.write("loaded(\"plugins/" + relative_path.strip("/") + "\");")

        # flushes the request, sending the output to the client
        request.flush()

        # returns true
        return True

    def _compute_etag(self, file_stat, modified_timestamp):
        """
        Computes the etag for the given file stat and
        modified timestamp.

        @type file_stat: Dictionary
        @param file_stat: The file stat values dictionary.
        @type modified_timestamp: int
        @param modified_timestamp: The last modified timestamp.
        @rtype: String
        @return: The etag value.
        """

        # retrieves the md5 builder
        md5 = hashlib.md5()

        # retrieves the size
        size = file_stat[stat.ST_SIZE]

        # creates the modification plus size string
        modification_size_string = str(modified_timestamp + size)

        # updates the md5 hash with the modification
        # plus size string
        md5.update(modification_size_string)

        # retrieves the md5 hex digest as the etag value
        etag_value = md5.hexdigest()

        # returns the etag value
        return etag_value
