#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import copy
import time

import colony

import base

SIZE_LIMIT = 20000
""" The limit in size of an array of the sub set of
requests that will be used in search for filter string """

mvc_utils = colony.__import__("mvc_utils")

class DiagnosticsController(base.BaseController):

    def requests(self, request):
        # generates and processes the template with the provided values
        # changing the current request accordingly, note that there's
        # a defined partial page and a base template value defined
        self._template(
            request = request,
            template = "diagnostics/requests.html.tpl",
            title = "Requests",
            area = "diagnostics",
            until = time.time()
        )

    def requests_list(self, request):
        # retrieves the json plugin for the encoding of the
        # response value (serialized value)
        json_plugin = self.plugin.json_plugin

        # retrieves the json plugin to be used for the retrieval
        # of the diagnostics information to be shown
        diagnostics_plugin = self.plugin.diagnostics_plugin

        # retrieves the various fields that are going to be used to
        # perform the query over the plugins
        until = request.field("until", None, cast = float)
        filter = request.field("filter_string", "")
        start_record = request.field("start_record", 0, cast = int)
        number_records = request.field("number_records", 9, cast = int)

        # converts the filter into a lower cased representation to be able to
        # perform a case insensitive comparison
        _filter = filter.lower()

        data = diagnostics_plugin.get_data()
        requests = data.get("requests_l", [])
        requests = requests[SIZE_LIMIT * -1:]

        # creates the list that will hold the final set of requests to be
        # presented, these request should be a result of a filtering
        _requests = []

        for _request in requests:
            path = _request["path"]
            initial = _request["initial"]
            path = path.lower()

            if not _filter in path: continue
            if until and initial > until: continue
            if not "time" in _request: continue

            _request = copy.copy(_request)
            time = _request["time"]

            if time >= 1000: time_color = "text-red"
            elif time >= 200: time_color = "text-orange"
            else: time_color = "text-normal"

            _request["time_color"] = time_color
            _requests.append(_request)

        _requests.reverse()
        _requests = _requests[start_record:start_record + number_records]
        self.serialize(request, _requests, serializer = json_plugin)

    def requests_show(self, request, request_id = None):
        pass