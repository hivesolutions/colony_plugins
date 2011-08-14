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

__revision__ = "$LastChangedRevision: 2341 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:42:37 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

configuration = {
    "instances" : {
        "colony" : {
            "name" : "colony",
            "wiki_name" : "Colony Docs",
            "template" : "simply",
            "main_page" : "documentation_index",
            "repository_type" : "svn",
            "repository_path" : "%manager_path%/../../../../pt.hive.colony.documentation/trunk/pt.hive.colony.documentation.technical",
            "logo_path" : "colony_logo.png",
            "icon_path" : "colony_icon.ico",
            "repository_arguments" : {
                "save_username_password" : False
            },
            "configuration_map" : {
                "auto_numbered_sections" : True,
                "generate_footer" : False,
                "simple_parse" : True
            }
        },
        "bargania" : {
            "name" : "bargania",
            "wiki_name" : "Bargania Developers",
            "template" : "simply",
            "main_page" : "index",
            "repository_type" : "svn",
            "repository_path" : "%plugin_path:com.bargania.documentation.plugins.main%/bargania_documentation_main/main/resources/container",
            "logo_path" : "bargania_logo.png",
            "icon_path" : "bargania_icon.ico",
            "footer_enabled" : False,
            "options_enabled" : False,
            "print_enabled" : False,
            "header_links" : [],
            "repository_arguments" : {
                "save_username_password" : False
            },
            "configuration_map" : {
                "auto_numbered_sections" : True,
                "generate_footer" : False,
                "simple_parse" : True
            },
            "configuration_index" : [
                {
                    "name" : "Global",
                    "items" : [
                        {
                            "name" : "Index",
                            "link" : "index"
                        }
                    ]
                },
                {
                    "name" : "Learn",
                    "items" : [
                        {
                            "name" : "What you get",
                            "link" : "what_you_get"
                        },
                        {
                            "name" : "Bargania RSS Specification",
                            "link" : "rss_specification"
                        },
                        {
                            "name" : "Bargania RSS Examples",
                            "link" : "rss_examples"
                        },
                    ]
                },
                {
                    "name" : "Cities and Categories",
                    "items" : [
                        {
                            "name" : "Locations",
                            "link" : "locations"
                        },
                        {
                            "name" : "Categories",
                            "link" : "categories"
                        }
                    ]
                },
                {
                    "name" : "Get Help",
                    "items" : [
                        {
                            "name" : "FAQ",
                            "link" : "faq"
                        },
                        {
                            "name" : "Support",
                            "link" : "support"
                        }
                    ]
                }
            ]
        }
    }
}
