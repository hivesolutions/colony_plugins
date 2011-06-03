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

__author__ = "Tiago Silva <tsilva@hive.pt>"
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

class WebMvcManagerPageItemCodeExecution:
    """
    The web mvc manager page item code execution class.
    """

    web_mvc_manager_page_item_code_execution_plugin = None
    """ The web mvc manager page item code execution plugin """

    def __init__(self, web_mvc_manager_page_item_code_execution_plugin):
        """
        Constructor of the class.

        @type web_mvc_manager_page_item_code_execution_plugin: WebMvcManagerPageItemCodeExecutionPlugin
        @param web_mvc_manager_page_item_code_execution_plugin: The web mvc manager page item code execution plugin.
        """

        self.web_mvc_manager_page_item_code_execution_plugin = web_mvc_manager_page_item_code_execution_plugin

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.web_mvc_manager_page_item_code_execution_plugin.web_mvc_utils_plugin

        # creates the controllers for the web mvc manager page item code execution controller modules
        web_mvc_utils_plugin.create_controllers("web_mvc_manager_page_item.code_execution.web_mvc_manager_page_item_code_execution_controllers", self, self.web_mvc_manager_page_item_code_execution_plugin, "web_mvc_manager_page_item_code_execution")

    def get_resource_patterns(self):
        """
        Retrieves the tuple of regular expressions to be used as resource patterns,
        to the web mvc service. The tuple should relate the route with the base
        file system path to be used.

        @rtype: Tuple
        @return: The tuple of regular expressions to be used as resource patterns,
        to the web mvc service.
        """

        return ()

    def get_page_item_bundle(self, parameters):
        """
        Retrieves a bundle containing all the maps with information
        on all the page items. The maps should contain information
        about the composition of the page item.

        @type parameters: Dictionary
        @param parameters: The parameters to retrieve the page
        item bundle.
        @rtype: List
        @return: A list containing information on all page items.
        """

        return (
            {
                "menu" : "services/Code Execution",
                "base_address" : "code_execution/new",
                "pattern" : (r"^web_mvc_manager/code_execution/new$", self.web_mvc_manager_page_item_code_execution_main_controller.handle_new_ajx, "get", "ajx")
            },
            (r"^web_mvc_manager/code_execution/new$", self.web_mvc_manager_page_item_code_execution_main_controller.handle_new, "get"),
            (r"^web_mvc_manager/code_execution$", self.web_mvc_manager_page_item_code_execution_main_controller.handle_execute, "post", "ajx")
        )
