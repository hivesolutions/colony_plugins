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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import web_mvc_manager_controllers

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

WEB_MVC_MANAGER_RESOURCES_PATH = "web_mvc_manager/manager/resources"
""" The web mvc manager resources path """

TEMPLATES_PATH = WEB_MVC_MANAGER_RESOURCES_PATH + "/templates"
""" The templates path """

EXTRAS_PATH = WEB_MVC_MANAGER_RESOURCES_PATH + "/extras"
""" The extras path """

class WebMvcManager:
    """
    The web mvc manager class.
    """

    web_mvc_manager_plugin = None
    """ The web mvc manager plugin """

    web_mvc_manager_main_controller = None
    """ The web mvc manager main controller """

    web_mvc_manager_side_panel_controller = None
    """ The web mvc manager side panel controller """

    web_mvc_manager_plugin_controller = None
    """ The web mvc manager plugin controller """

    web_mvc_manager_capability_controller = None
    """ The web mvc manager capability controller """

    def __init__(self, web_mvc_manager_plugin):
        """
        Constructor of the class.

        @type web_mvc_manager_plugin: WebMvcManagerPlugin
        @param web_mvc_manager_plugin: The web mvc manager plugin.
        """

        self.web_mvc_manager_plugin = web_mvc_manager_plugin

    def load_components(self):
        """
        Loads the main components controller, etc.
        This load should occur only after the dependencies are loaded.
        """

        # retrieves the web mvc utils plugin
        web_mvc_utils_plugin = self.web_mvc_manager_plugin.web_mvc_utils_plugin

        # creates the web mvc manager main controller
        self.web_mvc_manager_main_controller = web_mvc_utils_plugin.create_controller(WebMvcManagerMainController, [self.web_mvc_manager_plugin, self], {})

        # creates the web mvc manager side panel controller
        self.web_mvc_manager_side_panel_controller = web_mvc_utils_plugin.create_controller(web_mvc_manager_controllers.SidePanelController, [self.web_mvc_manager_plugin, self], {})

        # creates the web mvc manager plugin controller
        self.web_mvc_manager_plugin_controller = web_mvc_utils_plugin.create_controller(web_mvc_manager_controllers.PluginController, [self.web_mvc_manager_plugin, self], {})

        # creates the web mvc manager capability controller
        self.web_mvc_manager_capability_controller = web_mvc_utils_plugin.create_controller(web_mvc_manager_controllers.CapabilityController, [self.web_mvc_manager_plugin, self], {})

    def get_patterns(self):
        """
        Retrieves the map of regular expressions to be used as patters,
        to the web mvc service. The map should relate the route with the handler
        method/function.

        @rtype: Dictionary
        @return: The map of regular expressions to be used as patterns,
        to the web mvc service.
        """

        return {r"^web_mvc_manager/?$" : self.web_mvc_manager_main_controller.handle_web_mvc_manager_index,
                r"^web_mvc_manager/index$" : self.web_mvc_manager_main_controller.handle_web_mvc_manager_index,
                r"^web_mvc_manager/side_panel/configuration$" : self.web_mvc_manager_side_panel_controller.handle_configuration,
                r"^web_mvc_manager/plugins$" : self.web_mvc_manager_plugin_controller.handle_list,
                #r"^web_mvc_manager/plugins/[a-zA-Z0-9\._]+$" : self.web_mvc_manager_plugin_controller.handle_show,
                r"^web_mvc_manager/plugins/partial$" : self.web_mvc_manager_plugin_controller.handle_partial_list,
                r"^web_mvc_manager/plugins/new$" : self.web_mvc_manager_plugin_controller.handle_new,
                r"^web_mvc_manager/plugins/change_status$" : self.web_mvc_manager_plugin_controller.handle_change_status,
                r"^web_mvc_manager/capabilities$" : self.web_mvc_manager_capability_controller.handle_list,
                r"^web_mvc_manager/capabilities/[a-zA-Z0-9\._]+$" : self.web_mvc_manager_capability_controller.handle_show}

    def get_resource_patterns(self):
        # estes sao os patterns para serem enviados para
        # o file handleers

        # rinha de sacar aki o plugin path
        # e tinha de perceber para onde e ke os tinha de enviar

        # tenho de mandar um evento sempre que alguma destas coisas muda

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the web mvc resources base plugin
        web_mvc_resources_base_plugin = self.web_mvc_manager_plugin.web_mvc_resources_base_plugin

        # retrieves the web mvc resources ui plugin
        web_mvc_resources_ui_plugin = self.web_mvc_manager_plugin.web_mvc_resources_ui_plugin

        # retrieves the web mvc manager plugin path
        web_mvc_manager_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_manager_plugin.id)

        # retrieves the web mvc resources base plugin resources path
        web_mvc_resources_base_plugin_resources_path = web_mvc_resources_base_plugin.get_resources_path()

        # retrieves the web mvc resources ui plugin resources path
        web_mvc_resources_ui_plugin_resources_path = web_mvc_resources_ui_plugin.get_resources_path()

        return {r"^web_mvc_manager/resources/.+$" : (web_mvc_manager_plugin_path + "/" + EXTRAS_PATH, "web_mvc_manager/resources"),
                r"^web_mvc_manager/resources_base/.+$" : (web_mvc_resources_base_plugin_resources_path, "web_mvc_manager/resources_base"),
                r"^web_mvc_manager/resources_ui/.+$" : (web_mvc_resources_ui_plugin_resources_path, "web_mvc_manager/resources_ui")}

    def require_permissions(self, controller, rest_request, permissions_list = [], base_path = None):
        """
        Requires the permissions in the given permissions list to be set.
        In case the requirements are not met the request is redirected or an
        error message is sent.

        @type controller: Controller
        @param controller: The controller being validated.
        @type rest_request: RestRequest
        @param rest_request: The rest request to be updated.
        @type permissions_list: List
        @param permissions_list: The list of permission to be validated.
        @type base_path: String
        @param base_path: The base path to be used as prefix in the url.
        """

#        # retrieves the login session attribute
#        login = controller.get_session_attribute(rest_request, "login")
#
#        # in case the login is not set
#        if not login:
#            # in case the encoder name is ajax
#            if rest_request.encoder_name == AJAX_ENCODER_NAME:
#                # sets the contents
#                controller.set_contents(rest_request, "not enough permissions - access denied")
#            else:
#                # in case the base path is not defined
#                if not base_path:
#                    # retrieves the base path from the rest request
#                    base_path = controller.get_base_path(rest_request)
#
#                # redirects the request
#                rest_request.redirect(base_path + "signin")
#
#                # sets the contents (null)
#                controller.set_contents(rest_request)
#
#            # returns false
#            return False

        # returns true
        return True

class WebMvcManagerMainController:
    """
    The web mvc manager main controller.
    """

    web_mvc_manager_plugin = None
    """ The web mvc manager main plugin """

    web_mvc_manager = None
    """ The web mvc manager """

    def __init__(self, web_mvc_manager_plugin, web_mvc_manager):
        """
        Constructor of the class.

        @type web_mvc_manager_plugin: WebMvcManagerPlugin
        @param web_mvc_manager_plugin: The web mvc manager plugin.
        @type web_mvc_manager: WebMvcManager
        @param web_mvc_manager: The web mvc manager.
        """

        self.web_mvc_manager_plugin = web_mvc_manager_plugin
        self.web_mvc_manager = web_mvc_manager

    def start(self):
        """
        Method called upon structure initialization.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the web mvc manager plugin path
        web_mvc_manager_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_manager_plugin.id)

        # creates the templates path
        templates_path = web_mvc_manager_plugin_path + "/" + TEMPLATES_PATH

        # sets the templates path
        self.set_templates_path(templates_path)

    def handle_web_mvc_manager_index(self, rest_request, parameters = {}):
        """
        Handles the given web mvc manager index rest request.

        @type rest_request: RestRequest
        @param rest_request: The web mvc manager index rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the template file
        template_file = self.retrieve_template_file("general.html.tpl")

        # sets the page to be included

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True
