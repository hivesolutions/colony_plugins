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

class UrlParserPlugin(colony.Plugin):
    """
    The main class for the Url Parser plugin.
    """

    id = "pt.hive.colony.plugins.misc.url_parser"
    name = "Url Parser"
    description = "A plugin to parse url for agile interpretation"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "url_parse"
    ]
    main_modules = [
        "url_parser_c"
    ]

    def load_plugin(self):
        colony.Plugin.load_plugin(self)
        import url_parser_c
        self.system = url_parser_c.UrlParser(self)

    def parse_url(self, url):
        """
        Parses the given url retrieving the url object.

        @type url: String
        @param url:  The url to be parsed.
        @rtype: Url
        @return: The url object representing the url
        """

        return self.system.parse_url(url)
