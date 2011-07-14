#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__author__ = "Tiago Silva <tsilva@hive.pt> & João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 12939 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-02-01 17:54:16 +0000 (Tue, 01 Feb 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import re

SCAFFOLDER_TYPE_SEPARATOR = ","
""" The scaffolder type separator """

DEFAULT_VERSION = "1.0.0"
""" The default version """

CONSOLE_EXTENSION_NAME = "main_scaffolding"
""" The console extension name """

class ConsoleMainScaffolding:
    """
    The console main scaffolding class.
    """

    main_scaffolding_plugin = None
    """ The main scaffolding plugin """

    commands_map = {}
    """ The map containing the commands information """

    def __init__(self, main_scaffolding_plugin):
        """
        Constructor of the class.

        @type main_scaffolding_plugin: MainScaffoldingPlugin
        @param main_scaffolding_plugin: The main scaffolding plugin.
        """

        self.main_scaffolding_plugin = main_scaffolding_plugin

        # initializes the commands map
        self.commands_map = self.__generate_commands_map()

    def get_console_extension_name(self):
        return CONSOLE_EXTENSION_NAME

    def get_commands_map(self):
        return self.commands_map

    def process_generate_scaffold(self, arguments, arguments_map, output_method, console_context):
        """
        Processes the run automation command, with the given
        arguments and output method.

        @type arguments: List
        @param arguments: The arguments for the processing.
        @type arguments_map: Dictionary
        @param arguments_map: The map of arguments for the processing.
        @type output_method: Method
        @param output_method: The output method to be used in the processing.
        @type console_context: ConsoleContext
        @param console_context: The console context for the processing.
        """

        # retrieves the main scaffolding instance
        main_scaffolding = self.main_scaffolding_plugin.main_scaffolding

        # retrieves the mandatory arguments
        scaffolder_types_string = arguments_map["scaffolder_types"]
        plugin_id = arguments_map["plugin_id"]

        # retrieves the scaffold path for the plugin id
        scaffold_path = main_scaffolding._get_scaffold_path(plugin_id)

        # retrieves the optional arguments
        plugin_version = arguments_map.get("plugin_version", DEFAULT_VERSION)
        scaffold_path = arguments_map.get("scaffold_path", scaffold_path)
        specification_file_path = arguments_map.get("specification_file_path", None)

        # retrieves the scaffolder types
        scaffolder_types = scaffolder_types_string.split(SCAFFOLDER_TYPE_SEPARATOR)

        # prints a message
        output_method("started generating %s scaffold files..." % scaffolder_types_string)

        # generates the scaffold
        main_scaffolding.generate_scaffolds(scaffolder_types, plugin_id, plugin_version, scaffold_path, specification_file_path)

        # prints a message
        output_method("finished generating scaffold files into: %s" % scaffold_path)

    def get_scaffolder_types(self, argument, console_context):
        # retrieves the main scaffolding instance
        main_scaffolding = self.main_scaffolding_plugin.main_scaffolding

        # splits the argument
        argument_tokens = argument.rsplit(SCAFFOLDER_TYPE_SEPARATOR, 1)

        # retrieves the number of argument tokens
        number_argument_tokens = len(argument_tokens)

        # retrieves the scaffolder type prefix
        scaffolder_type_prefix = number_argument_tokens > 1 and argument_tokens[0] or ""

        # retrieves the last argument token
        last_argument_token = argument_tokens[-1]

        # retrieves the scaffolder types
        scaffolder_types = main_scaffolding.get_scaffolder_types()

        # retrieves the scaffolder types that start with the last argument
        scaffolder_types = [scaffolder_type_prefix + SCAFFOLDER_TYPE_SEPARATOR + scaffolder_type for scaffolder_type in scaffolder_types if scaffolder_type.startswith(last_argument_token)]

        # returns the scaffolder types
        return scaffolder_types

    def get_path_names_list(self, argument, console_context):
        # retrieves the directory name from the argument
        directory_name = os.path.dirname(argument)

        # retrieves the "full" path
        path = console_context.get_full_path(directory_name)

        # retrieves the path exists value
        path_exists = os.path.exists(path)

        # in case the path does
        # not exists
        if not path_exists:
            # returns empty list
            return []

        # retrieves the path names
        path_names = os.listdir(path)

        # in case the directory name is set
        if directory_name:
            # re-creates the path name joining the directory name
            path_names = [os.path.join(directory_name, value) for value in path_names]

        # returns the path names list
        return path_names

    def __generate_commands_map(self):
        # creates the commands map
        commands_map = {
            "generate_scaffold" : {
                "handler" : self.process_generate_scaffold,
                "description" : "generates the scaffold",
                "arguments" : [
                    {
                        "name" : "scaffolder_types",
                        "description" : "the scaffolds to generate separated by comma",
                        "values" : self.get_scaffolder_types,
                        "mandatory" : True
                    },
                    {
                        "name" : "plugin_id",
                        "description" : "the id of the plugin",
                        "values" : str,
                        "mandatory" : True
                    },
                    {
                        "name" : "plugin_version",
                        "description" : "the version of the plugin",
                        "values" : str,
                        "mandatory" : False
                    },
                    {
                        "name" : "scaffold_path",
                        "description" : "the path where to generate the plugin scaffold",
                        "values" : self.get_path_names_list,
                        "mandatory" : False
                    },
                    {
                        "name" : "specification_file_path",
                        "description" : "the file path to the specification file",
                        "values" : self.get_path_names_list,
                        "mandatory" : False
                    }
                ]
            }
        }

        # returns the commands map
        return commands_map
