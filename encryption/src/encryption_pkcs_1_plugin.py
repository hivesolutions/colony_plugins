#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system
import colony.base.decorators

class EncryptionPkcs1Plugin(colony.base.system.Plugin):
    """
    The main class for the Pkcs 1 Encryption plugin.
    """

    id = "pt.hive.colony.plugins.encryption.pkcs_1"
    name = "Pksc 1 Encryption Plugin"
    short_name = "Pkcs 1 Encryption"
    description = "The plugin that offers the pkcs 1 encryption support"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    loading_type = colony.base.system.EAGER_LOADING_TYPE
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT,
        colony.base.system.JYTHON_ENVIRONMENT
    ]
    attributes = {
        "build_automation_file_path" : "$base{plugin_directory}/encryption/pkcs_1/resources/baf.xml"
    }
    capabilities = [
        "encryption.pkcs_1",
        "build_automation_item"
    ]
    dependencies = [
        colony.base.system.PluginDependency("pt.hive.colony.plugins.format.ber", "1.x.x")
    ]
    main_modules = [
        "encryption.pkcs_1.encryption_pkcs_1_exceptions",
        "encryption.pkcs_1.encryption_pkcs_1_system"
    ]

    encryption_pkcs_1 = None
    """ The encryption pkcs 1 """

    format_ber_plugin = None
    """ The format ber plugin """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import encryption.pkcs_1.encryption_pkcs_1_system
        self.encryption_pkcs_1 = encryption.pkcs_1.encryption_pkcs_1_system.EncryptionPkcs1(self)

    def end_load_plugin(self):
        colony.base.system.Plugin.end_load_plugin(self)

    def unload_plugin(self):
        colony.base.system.Plugin.unload_plugin(self)

    def end_unload_plugin(self):
        colony.base.system.Plugin.end_unload_plugin(self)

    def load_allowed(self, plugin, capability):
        colony.base.system.Plugin.load_allowed(self, plugin, capability)

    def unload_allowed(self, plugin, capability):
        colony.base.system.Plugin.unload_allowed(self, plugin, capability)

    @colony.base.decorators.inject_dependencies
    def dependency_injected(self, plugin):
        colony.base.system.Plugin.dependency_injected(self, plugin)

    def create_structure(self, parameters):
        return self.encryption_pkcs_1.create_structure(parameters)

    def get_format_ber_plugin(self):
        return self.format_ber_plugin

    @colony.base.decorators.plugin_inject("pt.hive.colony.plugins.format.ber")
    def set_format_ber_plugin(self, format_ber_plugin):
        self.format_ber_plugin = format_ber_plugin
