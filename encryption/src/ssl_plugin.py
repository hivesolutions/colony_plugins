#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2016 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

class SslPlugin(colony.Plugin):
    """
    The main class for the Ssl plugin.
    """

    id = "pt.hive.colony.plugins.encryption.ssl"
    name = "Ssl"
    description = "The plugin that offers the ssl support"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT,
        colony.JYTHON_ENVIRONMENT
    ]
    capabilities = [
        "test",
        "encryption.ssl"
    ]
    dependencies = [
        colony.PluginDependency("pt.hive.colony.plugins.encryption.rsa"),
        colony.PluginDependency("pt.hive.colony.plugins.encryption.pkcs1")
    ]
    main_modules = [
        "ssl_c"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import ssl_c
        self.system = ssl_c.Ssl(self)
        self.test = ssl_c.SslTest(self)

    def create_structure(self, parameters):
        return self.system.create_structure(parameters)
