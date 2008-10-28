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

class IzpackBuildAutomationExtension:
    """
    The izpack build automation extension class.
    """

    izpack_build_automation_extension_plugin = None
    """ The izpack build automation extension plugin """

    def __init__(self, izpack_build_automation_extension_plugin):
        """
        Constructor of the class.
        
        @type izpack_build_automation_extension_plugin: IzpackBuildAutomationExtensionPlugin
        @param izpack_build_automation_extension_plugin: The izpack build automation extension plugin.
        """

        self.izpack_build_automation_extension_plugin = izpack_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters):
        # retrieves the resource manager plugin
        resource_manager_plugin = self.izpack_build_automation_extension_plugin.resource_manager_plugin

        # retrieves the execution environment plugin
        execution_environment_plugin = self.izpack_build_automation_extension_plugin.execution_environment_plugin

        # retrieves the command execution plugin
        command_execution_plugin = self.izpack_build_automation_extension_plugin.command_execution_plugin

        # retrieves the izpack home path resource
        izpack_home_path_resource = resource_manager_plugin.get_resource("system.path.izpack_home")

        # in case the izpach_home resource is not defined
        if not izpack_home_path_resource:
            return

        # retrieves the izpack home path value
        izpack_home_path = izpack_home_path_resource.data

        # retrieves the current operative system
        current_operative_system = execution_environment_plugin.get_operative_system()

        # in case the current environment is windows
        if current_operative_system == "windows":
            # creates the execution command
            izpack_execution_command = izpack_home_path + "/compile.bat"

        # executes the compilation command
        command_execution_plugin.execute_command(izpack_execution_command, ["C:/Users/Administrator/Desktop/hive_installer_test/hive_installer_test/install.xml"])
