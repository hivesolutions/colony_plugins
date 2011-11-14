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

__author__ = "João Magalhães <joamag@hive.pt>"
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

import os

import colony.libs.path_util

SOURCE_VALUE = "source"
""" The source value """

TARGET_VALUE = "target"
""" The target value """

class CopyBuildAutomationExtension:
    """
    The copy build automation extension class.
    """

    copy_build_automation_extension_plugin = None
    """ The copy build automation extension plugin """

    def __init__(self, copy_build_automation_extension_plugin):
        """
        Constructor of the class.

        @type copy_build_automation_extension_plugin: CopyBuildAutomationExtensionPlugin
        @param copy_build_automation_extension_plugin: The copy build automation extension plugin.
        """

        self.copy_build_automation_extension_plugin = copy_build_automation_extension_plugin

    def run_automation(self, plugin, stage, parameters, build_automation_structure, logger):
        # prints an info message
        logger.info("Running copy build automation plugin")

        # retrieves the copies
        copies = parameters.get("copies", {})

        # retrieves the various copy elements (copies)
        _copies = colony.libs.map_util.map_get_values(copies, "copy")

        # iterates over all the copies to be performed
        for copy in _copies:
            # retrieves the source and target (file paths)
            # from the copy information map
            source_path = copy[SOURCE_VALUE]
            target_path = copy[TARGET_VALUE]

            # retrieves the value for the copy hidden flag
            copy_hidden = copy.get("copy_hidden", "true") == "true" and True or False

            # in case the source path "refers" a directory, recursive
            # file copy must be performed
            if os.path.isdir(source_path):
                # copes the directory from the source path to the target
                # path replacing any existing duplicate files
                colony.libs.path_util.copy_directory(source_path, target_path, copy_hidden = copy_hidden)
            # otherwise it must be a regular file
            else:
                # copies the file from the source path to the target
                # path, in case a duplicate file already exists replaces it
                colony.libs.path_util.copy_file(source_path, target_path)

        # returns valid (success)
        return True
