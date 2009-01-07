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

__author__ = "Jo�o Magalh�es <joamag@hive.pt> & Lu�s Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import search_index_repository_exceptions

class SearchIndexRepository:
    """
    The search index repository class.
    """

    search_index_repository_plugin = None
    """ The search index repository plugin """

    search_index_repository_map = {}
    """ The search index repository map """

    def __init__(self, search_index_repository_plugin):
        """
        Constructor of the class.
        
        @type search_index_repository_plugin: SearchIndexRepositoryPlugin
        @param search_index_repository_plugin: The search index repository plugin.
        """

        self.search_index_repository_plugin = search_index_repository_plugin

        self.search_index_repository_map = {}

    def add_index(self, search_index, search_index_identifier):
        self.search_index_repository_map[search_index_identifier] = search_index

    def remove_index(self, search_index_identifier):
        if not search_index_identifier in self.search_index_repository_map:
            raise search_index_repository_exceptions.InvalidSearchIndexIdentifier(search_index_identifier)

        del self.search_index_repository_map[search_index_identifier]

    def get_index(self, search_index_identifier):
        if not search_index_identifier in self.search_index_repository_map:
            raise search_index_repository_exceptions.InvalidSearchIndexIdentifier(search_index_identifier)

        return self.search_index_repository_map[search_index_identifier]

    def get_index_identifiers(self):
        """
        Returns a list of index identifiers, available in the repository.
        """
        return self.search_index_repository_map.keys()

    def get_indexes(self):
        """
        Returns a list of search indexes, available in the repository.
        """        
        return self.search_index_repository_map.values()
