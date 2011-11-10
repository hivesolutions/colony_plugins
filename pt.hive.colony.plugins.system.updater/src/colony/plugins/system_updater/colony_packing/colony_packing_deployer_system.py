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

__revision__ = "$LastChangedRevision: 2349 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:52:01 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony_packing_deployer_exceptions

DEPLOYER_TYPE = "colony_packing_base"
""" The deployer type """

COLONY_VALUE = "colony"
""" The colony value """

TARGET_PATH_VALUE = "target_path"
""" The target path value """

class ColonyPackingDeployer:
    """
    The colony packing deployer class.
    """

    colony_packing_deployer_plugin = None
    """ The colony packing deployer plugin """

    def __init__(self, colony_packing_deployer_plugin):
        """
        Constructor of the class.

        @type colony_packing_deployer_plugin: ColonyPackingDeployerPlugin
        @param colony_packing_deployer_plugin: The colony packing deployer plugin.
        """

        self.colony_packing_deployer_plugin = colony_packing_deployer_plugin

    def load_deployer(self):
        """
        Method called upon load of the deployer.
        """

        self.colony_packing_deployer_plugin.info("Loading colony packing deployer")

    def get_deployer_type(self):
        """
        Retrieves the type of deployer.

        @rtype: String
        @return: The type of deployer.
        """

        return DEPLOYER_TYPE

    def deploy_bundle(self, bundle_id, bundle_version, contents_file, transaction_properties):
        """
        Method called upon deployment of the bundle with
        the given id, version and contents file.

        @type bundle_id: String
        @param bundle_id: The id of the bundle to be deployed.
        @type bundle_version: String
        @param bundle_version: The version of the bundle to be deployed.
        @type contents_file: ContentsFile
        @param contents_file: The contents file of the bundle to
        be deployed.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_deployer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_deployer_plugin.packing_manager_plugin

        # retrieves the main plugin path as the plugin path
        # for deployment
        plugin_path = plugin_manager.get_main_plugin_path()

        # creates the properties map for the file unpacking packing
        properties = {
            TARGET_PATH_VALUE : plugin_path
        }

        # unpacks the files using the colony service
        packing_manager_plugin.unpack_files([contents_file.name], properties, COLONY_VALUE)

    def deploy_plugin(self, plugin_id, plugin_version, contents_file, transaction_properties):
        """
        Method called upon deployment of the plugin with
        the given id, version and contents file.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to be deployed.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to be deployed.
        @type contents_file: ContentsFile
        @param contents_file: The contents file of the plugin to
        be deployed.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_deployer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_deployer_plugin.packing_manager_plugin

        # retrieves the main plugin path as the plugin path
        # for deployment
        plugin_path = plugin_manager.get_main_plugin_path()

        # creates the properties map for the file unpacking packing
        properties = {
            TARGET_PATH_VALUE : plugin_path
        }

        # unpacks the files using the colony service
        packing_manager_plugin.unpack_files([contents_file.name], properties, COLONY_VALUE)

    def deploy_container(self, container_id, container_version, contents_file, transaction_properties):
        """
        Method called upon deployment of the container with
        the given id, version and contents file.

        @type container_id: String
        @param container_id: The id of the container to be deployed.
        @type container_version: String
        @param container_version: The version of the container to be deployed.
        @type contents_file: ContentsFile
        @param contents_file: The contents file of the container to
        be deployed.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # retrieves the container manager
        container_manager = self.colony_packing_deployer_container.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_deployer_container.packing_manager_container

        # retrieves the containers path as the container path
        # for deployment
        containers_path = container_manager.get_containers_path()

        # creates the properties map for the file unpacking packing
        properties = {
            TARGET_PATH_VALUE : containers_path
        }

        # unpacks the files using the colony service
        packing_manager_plugin.unpack_files([contents_file.name], properties, COLONY_VALUE)

    def undeploy_bundle(self, bundle_id, bundle_version, transaction_properties):
        """
        Method called upon undeployment of the bundle with
        the given id and version.

        @type bundle_id: String
        @param bundle_id: The id of the bundle to be undeployed.
        @type bundle_version: String
        @param bundle_version: The version of the bundle to be undeployed.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # raises an operation not implemented exception
        raise colony_packing_deployer_exceptions.OperationNotSupported("not possible to undeploy colony bundles")

    def undeploy_plugin(self, plugin_id, plugin_version, transaction_properties):
        """
        Method called upon undeployment of the plugin with
        the given id and version.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to be undeployed.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to be undeployed.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # raises an operation not implemented exception
        raise colony_packing_deployer_exceptions.OperationNotSupported("not possible to undeploy colony plugins")

    def undeploy_container(self, container_id, container_version, transaction_properties):
        """
        Method called upon undeployment of the container with
        the given id and version.

        @type container_id: String
        @param container_id: The id of the container to be undeployed.
        @type container_version: String
        @param container_version: The version of the container to be undeployed.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # raises an operation not implemented exception
        raise colony_packing_deployer_exceptions.OperationNotSupported("not possible to undeploy colony containers")

    def open_transaction(self, transaction_properties):
        """
        Opens a new transaction and retrieves the transaction
        properties map.

        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the current transaction.
        @rtype: Dictionary
        @return: The map describing the transaction.
        """

        pass

    def commit_transaction(self, transaction_properties):
        """
        Commits the transaction described by the given
        transaction properties.

        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction to be commited.
        """

        pass

    def rollback_transaction(self, transaction_properties):
        """
        "Rollsback" the transaction described by the given
        transaction properties.

        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction to be "rollbacked".
        """

        pass

    def add_commit_callback(self, callback, transaction_properties):
        """
        Adds a commit callback to the current transaction.
        This callback will be called upon the final
        commit is passed.

        @type callback: Function
        @param callback: The callback function to be called
        upon the final commit.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction.
        """

        pass

    def add_rollback_callback(self, callback, transaction_properties):
        """
        Adds a rollback callback to the current transaction.
        This callback will be called upon the final
        rollback is passed.

        @type callback: Function
        @param callback: The callback function to be called
        upon the final rollback.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction.
        """

        pass
