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

import os
import time
import datetime
import threading

import colony.libs.file_util
import colony.libs.path_util
import colony.libs.crypt_util

import colony_packing_installer_exceptions

INSTALLER_TYPE = "colony_packing"
""" The installer type """

JSON_FILE_EXTENSION = "json"
""" The json file extension """

COLONY_VALUE = "colony"
""" The colony value """

FILE_CONTEXT_VALUE = "file_context"
""" The file context value """

TRANSACTION_PROPERTIES_VALUE = "transaction_properties"
""" The transaction properties value """

SUB_TYPE_VALUE = "sub_type"
""" The sub type value """

ID_VALUE = "id"
""" The id value """

VERSION_VALUE = "version"
""" The version value """

TIMESTAMP_VALUE = "timestamp"
""" The timestamp value """

HASH_DIGEST_VALUE = "hash_digest"
""" The hash digest value """

TYPE_VALUE = "type"
""" The type value """

RESOURCES_VALUE = "resources"
""" The resources value """

KEEP_RESOURCES_VALUE = "keep_resources"
""" The keep resources value """

EXTRA_RESOURCES_VALUE = "extra_resources"
""" The extra resources value """

BUNDLE_VALUE = "bundle"
""" The bundle value """

PLUGIN_VALUE = "plugin"
""" The plugin value """

CONTAINER_VALUE = "container"
""" The container value """

BUNDLES_VALUE = "bundles"
""" The bundles value """

PLUGINS_VALUE = "plugins"
""" The plugins value """

PLUGIN_SYSTEM_VALUE = "plugin_system"
""" The plugin system value """

LIBRARY_VALUE = "library"
""" The library value """

CONFIGURATION_VALUE = "configuration"
""" The configuration value """

UPGRADE_VALUE = "upgrade"
""" The upgrade value """

TARGET_PATH_VALUE = "target_path"
""" The target path value """

INSTALLED_PACKAGES_VALUE = "installed_packages"
""" The installed packages value """

INSTALLED_BUNDLES_VALUE = "installed_bundles"
""" The installed bundles value """

INSTALLED_PLUGINS_VALUE = "installed_plugins"
""" The installed plugins value """

INSTALLED_CONTAINERS_VALUE = "installed_containers"
""" The installed containers value """

DUPLICATE_FILES_VALUE = "duplicate_files"
""" The duplicate files values """

LAST_MODIFIED_TIMESTAMP_VALUE = "last_modified_timestamp"
""" The last modified timestamp value """

LAST_MODIFIED_DATE_VALUE = "last_modified_date"
""" The last modified date value """

RELATIVE_BUNDLES_PATH = "bundles"
""" The path relative to the manager path for the bundles """

RELATIVE_PLUGINS_PATH = "plugins"
""" The path relative to the manager path for the plugins """

RELATIVE_CONTAINERS_PATH = "containers"
""" The path relative to the manager path for the containers """

RELATIVE_REGISTRY_PATH = "registry"
""" The path relative to the variable path for the registry """

PACKAGES_FILE_NAME = "packages.json"
""" The packages file name """

BUNDLES_FILE_NAME = "bundles.json"
""" The bundles file name """

PLUGINS_FILE_NAME = "plugins.json"
""" The plugins file name """

CONTAINERS_FILE_NAME = "containers.json"
""" The containers file name """

DUPLICATES_FILE_NAME = "duplicates.json"
""" The duplicates file name """

COLONY_BUNDLE_FILE_EXTENSION = ".cbx"
""" The colony bundle file extension """

COLONY_PLUGIN_FILE_EXTENSION = ".cpx"
""" The colony plugin file extension """

COLONY_CONTAINER_FILE_EXTENSION = ".ccx"
""" The colony container file extension """

class ColonyPackingInstaller:
    """
    The colony packing installer class.
    """

    colony_packing_installer_plugin = None
    """ The colony packing installer plugin """

    colony_packing_installer_lock = None
    """ The lock to controll the access to installation """

    def __init__(self, colony_packing_installer_plugin):
        """
        Constructor of the class.

        @type colony_packing_installer_plugin: ColonyPackingInstallerPlugin
        @param colony_packing_installer_plugin: The colony packing installer plugin.
        """

        self.colony_packing_installer_plugin = colony_packing_installer_plugin

        self.colony_packing_installer_lock = threading.RLock()

    def load_installer(self):
        """
        Method called upon load of the installer.
        """

        self.colony_packing_installer_plugin.info("Loading colony packing installer")

    def get_installer_type(self):
        """
        Retrieves the type of installer.

        @rtype: String
        @return: The type of installer.
        """

        return INSTALLER_TYPE

    def exists_package(self, package_id, file_context):
        """
        Tests if the package with the given id exists in the
        current appropriate target.

        @type package_id: String
        @param package_id: The id of the package to be tested
        for existence.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        @rtype: bool
        @return: The result of the existence package test.
        """

        # retrieves the packages structure
        packages = self._get_packages(file_context)

        # retrieves the installed packages
        installed_packages = packages.get(INSTALLED_PACKAGES_VALUE, {})

        # checks if the package exists in the installed packages
        exists_package = package_id in installed_packages

        # returns the exists package (flag)
        return exists_package

    def install_package(self, file_path, properties, file_context = None):
        """
        Method called upon installation of the package with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the package file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # acquires the colony packing installer lock
        self.colony_packing_installer_lock.acquire()

        try:
            # installs the package (concrete method)
            self._install_package(file_path, properties, file_context)
        finally:
            # releases the colony packing installer lock
            self.colony_packing_installer_lock.release()

    def install_bundle(self, file_path, properties, file_context = None):
        """
        Method called upon installation of the bundle with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the bundle file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # acquires the colony packing installer lock
        self.colony_packing_installer_lock.acquire()

        try:
            # installs the bundle (concrete method)
            self._install_bundle(file_path, properties, file_context)
        finally:
            # releases the colony packing installer lock
            self.colony_packing_installer_lock.release()

    def install_plugin(self, file_path, properties, file_context = None):
        """
        Method called upon installation of the plugin with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the plugin file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # acquires the colony packing installer lock
        self.colony_packing_installer_lock.acquire()

        try:
            # installs the plugin (concrete method)
            self._install_plugin(file_path, properties, file_context)
        finally:
            # releases the colony packing installer lock
            self.colony_packing_installer_lock.release()

    def install_container(self, file_path, properties, file_context = None):
        """
        Method called upon installation of the container with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the container file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # acquires the colony packing installer lock
        self.colony_packing_installer_lock.acquire()

        try:
            # installs the container (concrete method)
            self._install_container(file_path, properties, file_context)
        finally:
            # releases the colony packing installer lock
            self.colony_packing_installer_lock.release()

    def uninstall_package(self, package_id, package_version, properties, file_context = None):
        """
        Method called upon removal of the package with
        the given id, version and properties.

        @type package_id: String
        @param package_id: The id of the package to be removed.
        @type package_version: String
        @param package_version: The version of the package to be removed.
        @type properties: Dictionary
        @param properties: The map of properties for removal.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # acquires the colony packing installer lock
        self.colony_packing_installer_lock.acquire()

        try:
            # installs the package (concrete method)
            self._uninstall_package(package_id, package_version, properties, file_context)
        finally:
            # releases the colony packing installer lock
            self.colony_packing_installer_lock.release()

    def uninstall_bundle(self, bundle_id, bundle_version, properties, file_context = None):
        """
        Method called upon removal of the bundle with
        the given id, version and properties.

        @type bundle_id: String
        @param bundle_id: The id of the bundle to be removed.
        @type bundle_version: String
        @param bundle_version: The version of the bundle to be removed.
        @type properties: Dictionary
        @param properties: The map of properties for removal.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # acquires the colony packing installer lock
        self.colony_packing_installer_lock.acquire()

        try:
            # installs the bundle (concrete method)
            self._uninstall_bundle(bundle_id, bundle_version, properties, file_context)
        finally:
            # releases the colony packing installer lock
            self.colony_packing_installer_lock.release()

    def uninstall_plugin(self, plugin_id, plugin_version, properties, file_context = None):
        """
        Method called upon removal of the plugin with
        the given id, version and properties.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to be removed.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to be removed.
        @type properties: Dictionary
        @param properties: The map of properties for removal.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # acquires the colony packing installer lock
        self.colony_packing_installer_lock.acquire()

        try:
            # installs the plugin (concrete method)
            self._uninstall_plugin(plugin_id, plugin_version, properties, file_context)
        finally:
            # releases the colony packing installer lock
            self.colony_packing_installer_lock.release()

    def uninstall_container(self, container_id, container_version, properties, file_context = None):
        """
        Method called upon removal of the container with
        the given id, version and properties.

        @type container_id: String
        @param container_id: The id of the container to be removed.
        @type container_version: String
        @param container_version: The version of the container to be removed.
        @type properties: Dictionary
        @param properties: The map of properties for removal.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # acquires the colony packing installer lock
        self.colony_packing_installer_lock.acquire()

        try:
            # installs the container (concrete method)
            self._uninstall_container(container_id, container_version, properties, file_context)
        finally:
            # releases the colony packing installer lock
            self.colony_packing_installer_lock.release()

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

        # retrieves the transaction properties
        transaction_properties = transaction_properties or {}

        # creates a new file transaction context
        file_context = transaction_properties.get(FILE_CONTEXT_VALUE) or colony.libs.file_util.FileTransactionContext()

        # opens the file context
        file_context.open()

        # sets the file context in the transaction properties
        transaction_properties[FILE_CONTEXT_VALUE] = file_context

        # returns the transaction properties
        return transaction_properties

    def commit_transaction(self, transaction_properties):
        """
        Commits the transaction described by the given
        transaction properties.

        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction to be commited.
        """

        # retrieves the file context
        file_context = transaction_properties.get(FILE_CONTEXT_VALUE)

        # commits the file context
        file_context.commit()

    def rollback_transaction(self, transaction_properties):
        """
        "Rollsback" the transaction described by the given
        transaction properties.

        @type transaction_properties: Dictionary
        @param transaction_properties: The properties of
        the transaction to be "rollbacked".
        """

        # retrieves the file context
        file_context = transaction_properties.get(FILE_CONTEXT_VALUE)

        # "rollsback" the file context
        file_context.rollback()

    def _install_package(self, file_path, properties, file_context = None):
        """
        Method called upon installation of the package with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the package file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # prints an info message
        self.colony_packing_installer_plugin.info("Installing package '%s'" % (file_path))

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # retrieves the transaction properties
        transaction_properties = properties.get(TRANSACTION_PROPERTIES_VALUE, {})

        # creates a new file transaction context
        file_context = file_context or transaction_properties.get(FILE_CONTEXT_VALUE, None) or colony.libs.file_util.FileTransactionContext()

        # opens a new transaction in the file context
        file_context.open()

        try:
            # resolves the file path retrieving the real file path
            real_file_path = file_context.resolve_file_path(file_path)

            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(real_file_path, {}, COLONY_VALUE)

            # retrieves the type
            type = packing_information.get_property(TYPE_VALUE)

            # retrieves the package id
            package_id = packing_information.get_property(ID_VALUE)

            # retrieves the package version
            package_version = packing_information.get_property(VERSION_VALUE)

            # processes the upgrade part of the installation
            self._process_upgrade(package_id, package_version, properties, file_context)

            # in case the type is bundle
            if type == BUNDLE_VALUE:
                # installs the bundle
                self.install_bundle(file_path, properties, file_context)
            # in case the type is plugin
            elif type == PLUGIN_VALUE:
                # installs the plugin
                self.install_plugin(file_path, properties, file_context)
            # in case the type is container
            elif type == CONTAINER_VALUE:
                # installs the container
                self.install_container(file_path, properties, file_context)
            # otherwise it's not a valid type
            else:
                # raises a plugin installation error
                raise colony_packing_installer_exceptions.PluginInstallationError("invalid packaging type: %s" % type)

            # retrieves the package item key
            package_item_key = package_id

            # generates the hash digest map for the package file
            hash_digest_map = colony.libs.crypt_util.generate_hash_digest_map(real_file_path)

            # creates the package item value
            package_item_value = {
                TYPE_VALUE : type,
                VERSION_VALUE : package_version,
                HASH_DIGEST_VALUE : hash_digest_map
            }

            # adds the package item
            self._add_package_item(package_item_key, package_item_value, file_context)

            # commits the transaction
            file_context.commit()
        except:
            # rollsback the transaction
            file_context.rollback()

            # re-raises the exception
            raise

        # prints an info message
        self.colony_packing_installer_plugin.info("Finished installing package '%s'" % (file_path))

    def _install_bundle(self, file_path, properties, file_context = None):
        """
        Method called upon installation of the bundle with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the bundle file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # creates the bundles directory path
        bundles_directory_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH + "/" + RELATIVE_BUNDLES_PATH)

        # retrieves the transaction properties
        transaction_properties = properties.get(TRANSACTION_PROPERTIES_VALUE, {})

        # creates a new file transaction context
        file_context = file_context or transaction_properties.get(FILE_CONTEXT_VALUE, None) or colony.libs.file_util.FileTransactionContext()

        # opens a new transaction in the file context
        file_context.open()

        try:
            # resolves the file path retrieving the real file path
            real_file_path = file_context.resolve_file_path(file_path)

            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(real_file_path, {}, COLONY_VALUE)

            # retrieves the bundle id
            bundle_id = packing_information.get_property(ID_VALUE)

            # retrieves the bundle version
            bundle_version = packing_information.get_property(VERSION_VALUE)

            # retrieves the bundle keep resources
            bundle_keep_resources = packing_information.get_property(KEEP_RESOURCES_VALUE)

            # retrieves the plugins
            plugins = packing_information.get_property(PLUGINS_VALUE)

            # reads the bundle file contents
            bundle_file_contents = file_context.read_file(file_path)

            # creates the bundle descriptor file path
            bundle_file_path = os.path.join(bundles_directory_path, bundle_id + "_" + bundle_version + COLONY_BUNDLE_FILE_EXTENSION)

            # writes the bundle file contents to the bundle file path
            file_context.write_file(bundle_file_path, bundle_file_contents)

            # retrieves the temporary path
            temporary_path = plugin_manager.get_temporary_path()

            # creates the temporary bundles path
            temporary_bundles_path = os.path.join(temporary_path, BUNDLES_VALUE)

            # retrieves the "virtual" main bundle path from the file context
            # this is necessary to ensure a transaction mode (no duplicate files are replaced)
            main_bundle_virtual_path = file_context.get_file_path(temporary_bundles_path, False)

            # deploys the package using the main bundle "virtual" path
            self._deploy_package(real_file_path, main_bundle_virtual_path)

            # iterates over all the bundle keep resources to remove
            # them from the temporary directory (avoids file overlap)
            for bundle_keep_resource in bundle_keep_resources:
                # creates the bundle keep resource path and removes
                # it from the file system (avoids file overlap)
                bundle_keep_resource_path = os.path.join(main_bundle_virtual_path, bundle_keep_resource)
                os.remove(bundle_keep_resource_path)

            # iterates over all the plugins
            for plugin in plugins:
                # retrieves the plugin id
                plugin_id = plugin[ID_VALUE]

                # retrieves the plugin version
                plugin_version = plugin[VERSION_VALUE]

                # creates the plugin file path
                plugin_file_path = os.path.join(temporary_bundles_path, PLUGINS_VALUE + "/" + plugin_id + "_" + plugin_version + COLONY_PLUGIN_FILE_EXTENSION)

                # installs the plugin for the given plugin file path
                # properties and file context
                self.install_plugin(plugin_file_path, properties, file_context)

                # retrieves the package item key
                package_item_key = plugin_id

                # resolves the plugin file path retrieving the real file path
                real_plugin_file_path = file_context.resolve_file_path(file_path)

                # generates the hash digest map for the package file
                hash_digest_map = colony.libs.crypt_util.generate_hash_digest_map(real_plugin_file_path)

                # creates the package item value
                package_item_value = {
                    TYPE_VALUE : PLUGIN_VALUE,
                    VERSION_VALUE : plugin_version,
                    HASH_DIGEST_VALUE : hash_digest_map
                }

                # adds the package item
                self._add_package_item(package_item_key, package_item_value, file_context)

            # retrieves the bundle item key
            bundle_item_key = bundle_id

            # generates the hash digest map for the bundle file
            hash_digest_map = colony.libs.crypt_util.generate_hash_digest_map(real_file_path)

            # creates the bundle item value
            bundle_item_value = {
                VERSION_VALUE : bundle_version,
                HASH_DIGEST_VALUE : hash_digest_map
            }

            # adds the bundle item
            self._add_bundle_item(bundle_item_key, bundle_item_value, file_context)

            # removes the temporary bundles path (directory)
            file_context.remove_directory_immediate(temporary_bundles_path)

            # commits the transaction
            file_context.commit()
        except:
            # rollsback the transaction
            file_context.rollback()

            # re-raises the exception
            raise

    def _install_plugin(self, file_path, properties, file_context = None):
        """
        Method called upon installation of the plugin with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the plugin file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # creates the plugins directory path
        plugins_directory_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH + "/" + RELATIVE_PLUGINS_PATH)

        # retrieves the transaction properties
        transaction_properties = properties.get(TRANSACTION_PROPERTIES_VALUE, {})

        # creates a new file transaction context
        file_context = file_context or transaction_properties.get(FILE_CONTEXT_VALUE, None) or colony.libs.file_util.FileTransactionContext()

        # opens a new transaction in the file context
        file_context.open()

        try:
            # resolves the file path retrieving the real file path
            real_file_path = file_context.resolve_file_path(file_path)

            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(real_file_path, {}, COLONY_VALUE)

            # retrieves the plugin id
            plugin_id = packing_information.get_property(ID_VALUE)

            # retrieves the plugin version
            plugin_version = packing_information.get_property(VERSION_VALUE)

            # retrieves the resources
            plugin_resources = packing_information.get_property(RESOURCES_VALUE)

            # retrieves the keep resources
            plugin_keep_resources = packing_information.get_property(KEEP_RESOURCES_VALUE, [])

            # retrieves the manager path
            manager_path = plugin_manager.get_manager_path()

            # retrieves the plugins path
            plugins_path = plugin_manager.get_main_plugin_path()

            # reads the plugin file contents
            plugin_file_contents = file_context.read_file(file_path)

            # creates the plugin descriptor file path
            plugin_file_path = os.path.join(plugins_directory_path, plugin_id + "_" + plugin_version + COLONY_PLUGIN_FILE_EXTENSION)

            # writes the plugin file contents to the plugin file path
            file_context.write_file(plugin_file_path, plugin_file_contents)

            # retrieves the "virtual" plugins path from the file context
            # this is necessary to ensure a transaction mode (no duplicate files are replaced)
            plugins_virtual_path = file_context.get_file_path(plugins_path, False)

            # retrieves the duplicates structure (from file)
            duplicates_structure = self._get_duplicates_structure(file_context)

            # retrieves the duplicate files structure
            duplicate_files_structure = duplicates_structure.get(DUPLICATE_FILES_VALUE, {})

            # iterates over all the plugin resources to check for
            # duplicate files
            for plugin_resource in plugin_resources:
                # in case the plugin resource is of type keep
                # (it should not be counted as duplicate)
                if plugin_resource in plugin_keep_resources:
                    # continues the loop
                    continue

                # creates the (complete) resource file path
                resource_file_path = os.path.join(plugins_path, plugin_resource)

                # in case the resource file path does not already exists
                if not file_context.exists_file_path(resource_file_path):
                    # continues the loop no need to update
                    # the duplicate files structure
                    continue

                # "calculates" the relative path between the resource file
                # path and the manager path
                resource_relative_path = colony.libs.path_util.relative_path(resource_file_path, manager_path)

                # aligns the path normalizing it into a system independent path
                resource_relative_path = colony.libs.path_util.align_path(resource_relative_path)

                # retrieves the number of times the file is "duplicated"
                duplicate_file_count = duplicate_files_structure.get(resource_relative_path, 0)

                # increments the duplicate count by one
                duplicate_file_count += 1

                # sets the duplicate file count in the duplicate files structure
                duplicate_files_structure[resource_relative_path] = duplicate_file_count

            # persists the duplicates structure
            self._persist_duplicates_structure(duplicates_structure, file_context)

            # deploys the package using the plugins "virtual" path
            self._deploy_package(real_file_path, plugins_virtual_path)

            # iterates over all the plugin keep resources to remove
            # them from the temporary directory (avoids file overlap)
            for plugin_keep_resource in plugin_keep_resources:
                # creates the plugin keep resource path and removes
                # it from the file system (avoids file overlap)
                plugin_keep_resource_path = os.path.join(plugins_virtual_path, plugin_keep_resource)
                os.remove(plugin_keep_resource_path)

            # retrieves the plugin item key
            plugin_item_key = plugin_id

            # generates the hash digest map for the plugin file
            hash_digest_map = colony.libs.crypt_util.generate_hash_digest_map(real_file_path)

            # creates the plugin item value
            plugin_item_value = {
                VERSION_VALUE : plugin_version,
                HASH_DIGEST_VALUE : hash_digest_map
            }

            # adds the plugin item
            self._add_plugin_item(plugin_item_key, plugin_item_value, file_context)

            # commits the transaction
            file_context.commit()
        except:
            # rollsback the transaction
            file_context.rollback()

            # re-raises the exception
            raise

    def _install_container(self, file_path, properties, file_context = None):
        """
        Method called upon installation of the container with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the container file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # creates the containers directory path
        containers_directory_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH + "/" + RELATIVE_CONTAINERS_PATH)

        # retrieves the transaction properties
        transaction_properties = properties.get(TRANSACTION_PROPERTIES_VALUE, {})

        # creates a new file transaction context
        file_context = file_context or transaction_properties.get(FILE_CONTEXT_VALUE, None) or colony.libs.file_util.FileTransactionContext()

        # opens a new transaction in the file context
        file_context.open()

        try:
            # resolves the file path retrieving the real file path
            real_file_path = file_context.resolve_file_path(file_path)

            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(real_file_path, {}, COLONY_VALUE)

            # retrieves the container sub type
            container_sub_type = packing_information.get_property(SUB_TYPE_VALUE)

            # retrieves the container id
            container_id = packing_information.get_property(ID_VALUE)

            # retrieves the container version
            container_version = packing_information.get_property(VERSION_VALUE)

            # retrieves the resources
            container_resources = packing_information.get_property(RESOURCES_VALUE)

            # retrieves the keep resources
            container_keep_resources = packing_information.get_property(KEEP_RESOURCES_VALUE, [])

            # retrieves the manager path
            manager_path = plugin_manager.get_manager_path()

            # retrieves the containers path in order to be used
            # to determine the containers exclusive (unique usage) path
            containers_path = plugin_manager.get_containers_path()
            containers_exclusive_path = os.path.join(containers_path, container_id)

            # reads the container file contents
            container_file_contents = file_context.read_file(file_path)

            # creates the container descriptor file path
            container_file_path = os.path.join(containers_directory_path, container_id + "_" + container_version + COLONY_CONTAINER_FILE_EXTENSION)

            # writes the container file contents to the container file path
            file_context.write_file(container_file_path, container_file_contents)

            # retrieves the "virtual" containers path from the file context
            # this is necessary to ensure a transaction mode (no duplicate files are replaced)
            containers_virtual_path = file_context.get_file_path(containers_exclusive_path, False)

            # retrieves the duplicates structure (from file)
            duplicates_structure = self._get_duplicates_structure(file_context)

            # retrieves the duplicate files structure
            duplicate_files_structure = duplicates_structure.get(DUPLICATE_FILES_VALUE, {})

            # iterates over all the container resources to check for
            # duplicate files
            for container_resource in container_resources:
                # in case the container resource is of type keep
                # (it should not be counted as duplicate)
                if container_resource in container_keep_resources:
                    # continues the loop
                    continue

                # creates the (complete) resource file path
                resource_file_path = os.path.join(containers_exclusive_path, container_resource)

                # in case the resource file path does not already exists
                if not file_context.exists_file_path(resource_file_path):
                    # continues the loop no need to update
                    # the duplicate files structure
                    continue

                # "calculates" the relative path between the resource file
                # path and the manager path
                resource_relative_path = colony.libs.path_util.relative_path(resource_file_path, manager_path)

                # aligns the path normalizing it into a system independent path
                resource_relative_path = colony.libs.path_util.align_path(resource_relative_path)

                # retrieves the number of times the file is "duplicated"
                duplicate_file_count = duplicate_files_structure.get(resource_relative_path, 0)

                # increments the duplicate count by one
                duplicate_file_count += 1

                # sets the duplicate file count in the duplicate files structure
                duplicate_files_structure[resource_relative_path] = duplicate_file_count

            # in case the container sub type is plugin system
            if container_sub_type == PLUGIN_SYSTEM_VALUE:
                # installs the plugin system
                self._install_plugin_system(file_path, properties, file_context)
            # in case the container sub type is library
            elif container_sub_type == LIBRARY_VALUE:
                # installs the library
                self._install_library(file_path, properties, file_context)
            # in case the container sub type is configuration
            elif container_sub_type == CONFIGURATION_VALUE:
                # installs the configuration
                self._install_configuration(file_path, properties, file_context)

            # persists the duplicates structure
            self._persist_duplicates_structure(duplicates_structure, file_context)

            # deploys the package using the containers "virtual" path
            self._deploy_package(real_file_path, containers_virtual_path)

            # iterates over all the container keep resources to remove
            # them from the temporary directory (avoids file overlap)
            for container_keep_resource in container_keep_resources:
                # creates the container keep resource path and removes
                # it from the file system (avoids file overlap)
                container_keep_resource_path = os.path.join(containers_virtual_path, container_keep_resource)
                os.remove(container_keep_resource_path)

            # retrieves the container item key
            container_item_key = container_id

            # generates the hash digest map for the container file
            hash_digest_map = colony.libs.crypt_util.generate_hash_digest_map(real_file_path)

            # creates the container item value
            container_item_value = {
                VERSION_VALUE : container_version,
                HASH_DIGEST_VALUE : hash_digest_map
            }

            # adds the container item
            self._add_container_item(container_item_key, container_item_value, file_context)

            # commits the transaction
            file_context.commit()
        except:
            # rollsback the transaction
            file_context.rollback()

            # re-raises the exception
            raise

    def _install_plugin_system(self, file_path, properties, file_context = None):
        """
        Method called upon installation of the plugin system with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the plugin system file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # creates the containers directory path
        containers_directory_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH + "/" + RELATIVE_CONTAINERS_PATH)

        # retrieves the transaction properties
        transaction_properties = properties.get(TRANSACTION_PROPERTIES_VALUE, {})

        # creates a new file transaction context
        file_context = file_context or transaction_properties.get(FILE_CONTEXT_VALUE, None) or colony.libs.file_util.FileTransactionContext()

        # opens a new transaction in the file context
        file_context.open()

        try:
            # resolves the file path retrieving the real file path
            real_file_path = file_context.resolve_file_path(file_path)

            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(real_file_path, {}, COLONY_VALUE)

            # retrieves the plugin system id
            plugin_system_id = packing_information.get_property(ID_VALUE)

            # retrieves the plugin system version
            plugin_system_version = packing_information.get_property(VERSION_VALUE)

            # retrieves the plugin system keep resources
            plugin_system_keep_resources = packing_information.get_property(KEEP_RESOURCES_VALUE)

            # retrieves the manager path
            manager_path = plugin_manager.get_manager_path()

            # reads the plugin system file contents
            plugin_system_file_contents = file_context.read_file(file_path)

            # creates the plugin system descriptor file path
            plugin_system_file_path = os.path.join(containers_directory_path, plugin_system_id + "_" + plugin_system_version + COLONY_CONTAINER_FILE_EXTENSION)

            # writes the plugin system file contents to the plugin system file path
            file_context.write_file(plugin_system_file_path, plugin_system_file_contents)

            # retrieves the "virtual" manager path from the file context
            # this is necessary to ensure a transaction mode (no duplicate files are replaced)
            manager_virtual_path = file_context.get_file_path(manager_path, False)

            # deploys the package using the manager "virtual" path
            self._deploy_package(real_file_path, manager_virtual_path)

            # iterates over all the plugin system keep resources to remove
            # them from the temporary directory (avoids file overlap)
            for plugin_system_keep_resource in plugin_system_keep_resources:
                # creates the plugin system keep resource path and removes
                # it from the file system (avoids file overlap)
                plugin_system_keep_resource_path = os.path.join(manager_virtual_path, plugin_system_keep_resource)
                os.remove(plugin_system_keep_resource_path)

            # commits the transaction
            file_context.commit()
        except:
            # rollsback the transaction
            file_context.rollback()

            # re-raises the exception
            raise

    def _install_library(self, file_path, properties, file_context = None):
        """
        Method called upon installation of the library with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the library file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # creates the containers directory path
        containers_directory_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH + "/" + RELATIVE_CONTAINERS_PATH)

        # retrieves the transaction properties
        transaction_properties = properties.get(TRANSACTION_PROPERTIES_VALUE, {})

        # creates a new file transaction context
        file_context = file_context or transaction_properties.get(FILE_CONTEXT_VALUE, None) or colony.libs.file_util.FileTransactionContext()

        # opens a new transaction in the file context
        file_context.open()

        try:
            # resolves the file path retrieving the real file path
            real_file_path = file_context.resolve_file_path(file_path)

            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(real_file_path, {}, COLONY_VALUE)

            # retrieves the library id
            library_id = packing_information.get_property(ID_VALUE)

            # retrieves the library version
            library_version = packing_information.get_property(VERSION_VALUE)

            # retrieves the library keep resources
            library_keep_resources = packing_information.get_property(KEEP_RESOURCES_VALUE)

            # retrieves the libraries path
            libraries_path = plugin_manager.get_libraries_path()

            # reads the library file contents
            library_file_contents = file_context.read_file(file_path)

            # creates the library descriptor file path
            library_file_path = os.path.join(containers_directory_path, library_id + "_" + library_version + COLONY_CONTAINER_FILE_EXTENSION)

            # writes the library file contents to the library file path
            file_context.write_file(library_file_path, library_file_contents)

            # retrieves the "virtual" libraries path from the file context
            # this is necessary to ensure a transaction mode (no duplicate files are replaced)
            libraries_virtual_path = file_context.get_file_path(libraries_path, False)

            # deploys the package using the libraries "virtual" path
            self._deploy_package(real_file_path, libraries_virtual_path)

            # iterates over all the library keep resources to remove
            # them from the temporary directory (avoids file overlap)
            for library_keep_resource in library_keep_resources:
                # creates the library keep resource path and removes
                # it from the file system (avoids file overlap)
                library_keep_resource_path = os.path.join(libraries_virtual_path, library_keep_resource)
                os.remove(library_keep_resource_path)

            # commits the transaction
            file_context.commit()
        except:
            # rollsback the transaction
            file_context.rollback()

            # re-raises the exception
            raise

    def _install_configuration(self, file_path, properties, file_context = None):
        """
        Method called upon installation of the configuration with
        the given file path and properties.

        @type file_path: String
        @param file_path: The path to the configuration file to be installed.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        pass

    def _uninstall_package(self, package_id, package_version, properties, file_context = None):
        """
        Method called upon removal of the package with
        the given id, version and properties.

        @type package_id: String
        @param package_id: The id of the package to be removed.
        @type package_version: String
        @param package_version: The version of the package to be removed.
        @type properties: Dictionary
        @param properties: The map of properties for removal.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # prints an info message
        self.colony_packing_installer_plugin.info("Uninstalling package '%s'" % (package_id))

        # retrieves the transaction properties
        transaction_properties = properties.get(TRANSACTION_PROPERTIES_VALUE, {})

        # creates a new file transaction context
        file_context = file_context or transaction_properties.get(FILE_CONTEXT_VALUE, None) or colony.libs.file_util.FileTransactionContext()

        # opens a new transaction in the file context
        file_context.open()

        try:
            # retrieves the packages structure
            packages = self._get_packages(file_context)

            # retrieves the installed packages
            installed_packages = packages.get(INSTALLED_PACKAGES_VALUE, {})

            # in case the package id is not found in the installed packages
            if not package_id in installed_packages:
                # raises the plugin installation error
                raise colony_packing_installer_exceptions.PluginInstallationError("package '%s' v'%s' is not installed" % (package_id, package_version))

            # retrieves the package (information) from the
            # installed packages
            package = installed_packages[package_id]

            # retrieves the package version as the package version
            # or from the package structure
            package_version = package_version or package[VERSION_VALUE]

            # retrieves the package type
            package_type = package[TYPE_VALUE]

            # in case the type is bundle
            if package_type == BUNDLE_VALUE:
                # removes the bundle
                self.uninstall_bundle(package_id, package_version, properties, file_context)
            # in case the type is plugin
            elif package_type == PLUGIN_VALUE:
                # removes the plugin
                self.uninstall_plugin(package_id, package_version, properties, file_context)
            # in case the type is container
            elif package_type == CONTAINER_VALUE:
                # removes the container
                self.uninstall_container(package_id, package_version, properties, file_context)
            # otherwise it's not a valid type
            else:
                # raises a plugin installation error
                raise colony_packing_installer_exceptions.PluginInstallationError("invalid packaging type: %s" % package_type)

            # removes the package item
            self._remove_package_item(package_id, file_context)

            # commits the transaction
            file_context.commit()
        except:
            # rollsback the transaction
            file_context.rollback()

            # re-raises the exception
            raise

        # prints an info message
        self.colony_packing_installer_plugin.info("Finished uninstalling package '%s'" % (package_id))

    def _uninstall_bundle(self, bundle_id, bundle_version, properties, file_context = None):
        """
        Method called upon removal of the bundle with
        the given id, version and properties.

        @type bundle_id: String
        @param bundle_id: The id of the bundle to be removed.
        @type bundle_version: String
        @param bundle_version: The version of the bundle to be removed.
        @type properties: Dictionary
        @param properties: The map of properties for removal.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # retrieves the registry path
        registry_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH)

        # retrieves the transaction properties
        transaction_properties = properties.get(TRANSACTION_PROPERTIES_VALUE, {})

        # creates a new file transaction context
        file_context = file_context or transaction_properties.get(FILE_CONTEXT_VALUE, None) or colony.libs.file_util.FileTransactionContext()

        # opens a new transaction in the file context
        file_context.open()

        try:
            # retrieves the bundles structure
            bundles = self._get_bundles(file_context)

            # retrieves the installed bundles
            installed_bundles = bundles.get(INSTALLED_BUNDLES_VALUE, {})

            # in case the bundle id is not found in the installed bundles
            if not bundle_id in installed_bundles:
                # raises the plugin installation error
                raise colony_packing_installer_exceptions.PluginInstallationError("bundle '%s' v'%s' is not installed" % (bundle_id, bundle_version))

            # retrieves the bundle (information) from the
            # installed bundles
            bundle = installed_bundles[bundle_id]

            # retrieves the bundle version as the bundle version
            # or from the bundle structure
            bundle_version = bundle_version or bundle[VERSION_VALUE]

            # creates the bundle file name from the bundle
            # id and version
            bundle_file_name = bundle_id + "_" + bundle_version + COLONY_BUNDLE_FILE_EXTENSION

            # creates the bundle file path from the
            bundle_path = os.path.join(registry_path, RELATIVE_BUNDLES_PATH + "/" + bundle_file_name)

            # resolves the bundle path
            real_bundle_path = file_context.resolve_file_path(bundle_path)

            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(real_bundle_path, {}, COLONY_VALUE)

            # retrieves the bundle plugins
            bundle_plugins = packing_information.get_property(PLUGINS_VALUE)

            # iterates over all the plugins to remove them
            for bundle_plugin in bundle_plugins:
                # retrieves the plugin id
                plugin_id = bundle_plugin[ID_VALUE]

                # retrieves the plugin version
                plugin_version = bundle_plugin[VERSION_VALUE]

                # removes the plugin
                self.uninstall_plugin(plugin_id, plugin_version, properties, file_context)

                # removes the package item
                self._remove_package_item(plugin_id, file_context)

            # removes the bundle file
            file_context.remove_file(real_bundle_path)

            # removes the bundle item
            self._remove_bundle_item(bundle_id, file_context)

            # commits the transaction
            file_context.commit()
        except:
            # rollsback the transaction
            file_context.rollback()

            # re-raises the exception
            raise

    def _uninstall_plugin(self, plugin_id, plugin_version, properties, file_context = None):
        """
        Method called upon removal of the plugin with
        the given id, version and properties.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to be removed.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to be removed.
        @type properties: Dictionary
        @param properties: The map of properties for removal.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # retrieves the manager path
        manager_path = plugin_manager.get_manager_path()

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # retrieves the registry path
        registry_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH)

        # retrieves the plugins path
        plugins_path = plugin_manager.get_main_plugin_path()

        # retrieves the transaction properties
        transaction_properties = properties.get(TRANSACTION_PROPERTIES_VALUE, {})

        # creates a new file transaction context
        file_context = file_context or transaction_properties.get(FILE_CONTEXT_VALUE, None) or colony.libs.file_util.FileTransactionContext()

        # opens a new transaction in the file context
        file_context.open()

        try:
            # retrieves the plugins structure
            plugins = self._get_plugins(file_context)

            # retrieves the installed plugins
            installed_plugins = plugins.get(INSTALLED_PLUGINS_VALUE, {})

            # in case the plugin id is not found in the installed plugins
            if not plugin_id in installed_plugins:
                # raises the plugin installation error
                raise colony_packing_installer_exceptions.PluginInstallationError("plugin '%s' v'%s' is not installed" % (plugin_id, plugin_version))

            # retrieves the plugin (information) from the
            # installed plugins
            plugin = installed_plugins[plugin_id]

            # retrieves the plugin version as the plugin version
            # or from the plugin structure
            plugin_version = plugin_version or plugin[VERSION_VALUE]

            # creates the plugin file name from the plugin
            # id and version
            plugin_file_name = plugin_id + "_" + plugin_version + COLONY_PLUGIN_FILE_EXTENSION

            # creates the plugin file path from the
            plugin_path = os.path.join(registry_path, RELATIVE_PLUGINS_PATH + "/" + plugin_file_name)

            # resolves the plugin path
            real_plugin_path = file_context.resolve_file_path(plugin_path)

            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(real_plugin_path, {}, COLONY_VALUE)

            # retrieves the plugin resources
            plugin_resources = packing_information.get_property(RESOURCES_VALUE)

            # retrieves the plugin keep resources
            plugin_keep_resources = packing_information.get_property(KEEP_RESOURCES_VALUE, [])

            # retrieves the plugin extra resources
            plugin_extra_resources = packing_information.get_property(EXTRA_RESOURCES_VALUE, [])

            # filters the plugin resources that are meant to be kept in
            # the system and then extends the plugin resources list with
            # the plugin extra resources
            plugin_resources = [value for value in plugin_resources if not value in plugin_keep_resources]
            plugin_resources.extend(plugin_extra_resources)

            # creates the list of directory paths for (possible)
            # later removal
            directory_path_list = []

            # retrieves the duplicates structure (from file)
            duplicates_structure = self._get_duplicates_structure(file_context)

            # retrieves the duplicate files structure
            duplicate_files_structure = duplicates_structure.get(DUPLICATE_FILES_VALUE, {})

            # iterates over all the resources to remove them
            for plugin_resource in plugin_resources:
                # creates the (complete) resource file path
                resource_file_path = os.path.join(plugins_path, plugin_resource)

                # "calculates" the relative path between the resource file
                # path and the manager path
                resource_relative_path = colony.libs.path_util.relative_path(resource_file_path, manager_path)

                # aligns the path normalizing it into a system independent path
                resource_relative_path = colony.libs.path_util.align_path(resource_relative_path)

                # retrieves the number of times the file is "duplicated"
                duplicate_file_count = duplicate_files_structure.get(resource_relative_path, 0)

                # checks if the file should be removed
                remove_file = duplicate_file_count == 0

                # decrements the duplicate count by one
                duplicate_file_count -= 1

                # in case the duplicate file count is superior to zero
                if duplicate_file_count > 0:
                    # sets the duplicate file count in the duplicate files structure
                    duplicate_files_structure[resource_relative_path] = duplicate_file_count
                # otherwise in case the resource relative path reference
                # exists in the duplicate files structure
                elif resource_relative_path in duplicate_files_structure:
                    # removes the resource relative path from the duplicate
                    # files structure
                    del duplicate_files_structure[resource_relative_path]

                # in case the remove file is not set
                if not remove_file:
                    # continues the loop no need to remove a file that
                    # is duplicated
                    continue

                # in case the resource file path exists
                if not file_context.exists_file_path(resource_file_path):
                    # continues the loop
                    continue

                # removes the resource file in the resource file path
                file_context.remove_file(resource_file_path)

                # retrieves the resource file directory path
                resource_file_directory_path = os.path.dirname(resource_file_path)

                # in case the resource file directory path is not yet
                # present in the directory path list
                if not resource_file_directory_path in directory_path_list:
                    # adds the file directory path to the
                    # directory path list
                    directory_path_list.append(resource_file_directory_path)

            # persists the duplicates structure
            self._persist_duplicates_structure(duplicates_structure, file_context)

            # iterates over all the directory paths
            for directory_path in directory_path_list:
                # in case the directory path does not refers
                # a directory
                if not file_context.is_directory_path(directory_path):
                    # continues the loop
                    continue

                # removes the directories in the directory path
                file_context.remove_directory(directory_path, True)

            # removes the plugin file
            file_context.remove_file(real_plugin_path)

            # removes the plugin item
            self._remove_plugin_item(plugin_id, file_context)

            # commits the transaction
            file_context.commit()
        except:
            # rollsback the transaction
            file_context.rollback()

            # re-raises the exception
            raise

    def _uninstall_container(self, container_id, container_version, properties, file_context = None):
        """
        Method called upon removal of the container with
        the given id, version and properties.

        @type container_id: String
        @param container_id: The id of the container to be removed.
        @type container_version: String
        @param container_version: The version of the container to be removed.
        @type properties: Dictionary
        @param properties: The map of properties for removal.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # retrieves the manager path
        manager_path = plugin_manager.get_manager_path()

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # retrieves the registry path
        registry_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH)

        # retrieves the containers path in order to be used
        # to determine the containers exclusive (unique usage) path
        containers_path = plugin_manager.get_containers_path()
        containers_exclusive_path = os.path.join(containers_path, container_id)

        # retrieves the transaction properties
        transaction_properties = properties.get(TRANSACTION_PROPERTIES_VALUE, {})

        # creates a new file transaction context
        file_context = file_context or transaction_properties.get(FILE_CONTEXT_VALUE, None) or colony.libs.file_util.FileTransactionContext()

        # opens a new transaction in the file context
        file_context.open()

        try:
            # retrieves the containers structure
            containers = self._get_containers(file_context)

            # retrieves the installed containers
            installed_containers = containers.get(INSTALLED_CONTAINERS_VALUE, {})

            # in case the container id is not found in the installed containers
            if not container_id in installed_containers:
                # raises the container installation error
                raise colony_packing_installer_exceptions.ContainerInstallationError("container '%s' v'%s' is not installed" % (container_id, container_version))

            # retrieves the container (information) from the
            # installed containers
            container = installed_containers[container_id]

            # retrieves the container version as the container version
            # or from the container structure
            container_version = container_version or container[VERSION_VALUE]

            # creates the container file name from the container
            # id and version
            container_file_name = container_id + "_" + container_version + COLONY_CONTAINER_FILE_EXTENSION

            # creates the container file path from the
            container_path = os.path.join(registry_path, RELATIVE_CONTAINERS_PATH + "/" + container_file_name)

            # resolves the container path
            real_container_path = file_context.resolve_file_path(container_path)

            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(real_container_path, {}, COLONY_VALUE)

            # retrieves the container sub type
            container_sub_type = packing_information.get_property(SUB_TYPE_VALUE)

            # retrieves the container resources
            container_resources = packing_information.get_property(RESOURCES_VALUE)

            # retrieves the container keep resources
            container_keep_resources = packing_information.get_property(KEEP_RESOURCES_VALUE, [])

            # retrieves the container extra resources
            container_extra_resources = packing_information.get_property(EXTRA_RESOURCES_VALUE, [])

            # filters the container resources that are meant to be kept in
            # the system and then extends the container resources list with
            # the container extra resources
            container_resources = [value for value in container_resources if not value in container_keep_resources]
            container_resources.extend(container_extra_resources)

            # creates the list of directory paths for (possible)
            # later removal
            directory_path_list = []

            # retrieves the duplicates structure (from file)
            duplicates_structure = self._get_duplicates_structure(file_context)

            # retrieves the duplicate files structure
            duplicate_files_structure = duplicates_structure.get(DUPLICATE_FILES_VALUE, {})

            # iterates over all the resources to remove them
            for container_resource in container_resources:
                # creates the (complete) resource file path
                resource_file_path = os.path.join(containers_exclusive_path, container_resource)

                # "calculates" the relative path between the resource file
                # path and the manager path
                resource_relative_path = colony.libs.path_util.relative_path(resource_file_path, manager_path)

                # aligns the path normalizing it into a system independent path
                resource_relative_path = colony.libs.path_util.align_path(resource_relative_path)

                # retrieves the number of times the file is "duplicated"
                duplicate_file_count = duplicate_files_structure.get(resource_relative_path, 0)

                # checks if the file should be removed
                remove_file = duplicate_file_count == 0

                # decrements the duplicate count by one
                duplicate_file_count -= 1

                # in case the duplicate file count is superior to zero
                if duplicate_file_count > 0:
                    # sets the duplicate file count in the duplicate files structure
                    duplicate_files_structure[resource_relative_path] = duplicate_file_count
                # otherwise in case the resource relative path reference
                # exists in the duplicate files structure
                elif resource_relative_path in duplicate_files_structure:
                    # removes the resource relative path from the duplicate
                    # files structure
                    del duplicate_files_structure[resource_relative_path]

                # in case the remove file is not set
                if not remove_file:
                    # continues the loop no need to remove a file that
                    # is duplicated
                    continue

                # in case the resource file path exists
                if not file_context.exists_file_path(resource_file_path):
                    # continues the loop
                    continue

                # removes the resource file in the resource file path
                file_context.remove_file(resource_file_path)

                # retrieves the resource file directory path
                resource_file_directory_path = os.path.dirname(resource_file_path)

                # in case the resource file directory path is not yet
                # present in the directory path list
                if not resource_file_directory_path in directory_path_list:
                    # adds the file directory path to the
                    # directory path list
                    directory_path_list.append(resource_file_directory_path)

            # in case the container sub type is plugin system
            if container_sub_type == PLUGIN_SYSTEM_VALUE:
                # uninstalls the plugin system
                self._uninstall_plugin_system(container_id, container_version, container, properties, file_context)
            # in case the container sub type is library
            elif container_sub_type == LIBRARY_VALUE:
                # uninstalls the library
                self._uninstall_library(container_id, container_version, container, properties, file_context)
            # in case the container sub type is configuration
            elif container_sub_type == CONFIGURATION_VALUE:
                # uninstalls the configuration
                self._uninstall_configuration(container_id, container_version, container, properties, file_context)

            # persists the duplicates structure
            self._persist_duplicates_structure(duplicates_structure, file_context)

            # iterates over all the directory paths
            for directory_path in directory_path_list:
                # in case the directory path does not refers
                # a directory
                if not file_context.is_directory_path(directory_path):
                    # continues the loop
                    continue

                # removes the directories in the directory path
                file_context.remove_directory(directory_path, True)

            # removes the container file
            file_context.remove_file(real_container_path)

            # removes the container item
            self._remove_container_item(container_id, file_context)

            # commits the transaction
            file_context.commit()
        except:
            # rollsback the transaction
            file_context.rollback()

            # re-raises the exception
            raise

    def _uninstall_plugin_system(self, plugin_system_id, plugin_system_version, plugin_system, properties, file_context = None):
        """
        Method called upon removal of the plugin system with
        the given id, version and properties.

        @type plugin_system_id: String
        @param plugin_system_id: The id of the plugin system to be removed.
        @type plugin_system_version: String
        @param plugin_system_version: The version of the plugin system to be removed.
        @type plugin_system: Dictionary
        @param plugin_system: The map containing the plugin system description.
        @type properties: Dictionary
        @param properties: The map of properties for removal.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # retrieves the manager path
        manager_path = plugin_manager.get_manager_path()

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # retrieves the registry path
        registry_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH)

        # retrieves the transaction properties
        transaction_properties = properties.get(TRANSACTION_PROPERTIES_VALUE, {})

        # creates a new file transaction context
        file_context = file_context or transaction_properties.get(FILE_CONTEXT_VALUE, None) or colony.libs.file_util.FileTransactionContext()

        # opens a new transaction in the file context
        file_context.open()

        try:
            # retrieves the plugin system version as the plugin system version
            # or from the plugin system structure
            plugin_system_version = plugin_system_version or plugin_system[VERSION_VALUE]

            # creates the library file name from the library
            # id and version
            plugin_system_file_name = plugin_system_id + "_" + plugin_system_version + COLONY_CONTAINER_FILE_EXTENSION

            # creates the plugin system file path from the
            plugin_system_path = os.path.join(registry_path, RELATIVE_CONTAINERS_PATH + "/" + plugin_system_file_name)

            # resolves the plugin system path
            real_plugin_system_path = file_context.resolve_file_path(plugin_system_path)

            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(real_plugin_system_path, {}, COLONY_VALUE)

            # retrieves the plugin system resources
            plugin_system_resources = packing_information.get_property(RESOURCES_VALUE)

            # retrieves the plugin system keep resources
            plugin_system_keep_resources = packing_information.get_property(KEEP_RESOURCES_VALUE, [])

            # retrieves the plugin system extra resources
            plugin_system_extra_resources = packing_information.get_property(EXTRA_RESOURCES_VALUE, [])

            # filters the plugin system resources that are meant to be kept in
            # the system and then extends the plugin system resources list with
            # the plugin system extra resources
            plugin_system_resources = [value for value in plugin_system_resources if not value in plugin_system_keep_resources]
            plugin_system_resources.extend(plugin_system_extra_resources)

            # creates the list of directory paths for (possible)
            # later removal
            directory_path_list = []

            # iterates over all the resources to remove them
            for plugin_system_resource in plugin_system_resources:
                # creates the (complete) resource file path
                resource_file_path = os.path.join(manager_path, plugin_system_resource)

                # "calculates" the relative path between the resource file
                # path and the manager path
                resource_relative_path = colony.libs.path_util.relative_path(resource_file_path, manager_path)

                # aligns the path normalizing it into a system independent path
                resource_relative_path = colony.libs.path_util.align_path(resource_relative_path)

                # in case the resource file path exists
                if not file_context.exists_file_path(resource_file_path):
                    # continues the loop
                    continue

                # removes the resource file in the resource file path
                file_context.remove_file(resource_file_path)

                # retrieves the resource file directory path
                resource_file_directory_path = os.path.dirname(resource_file_path)

                # in case the resource file directory path is not yet
                # present in the directory path list
                if not resource_file_directory_path in directory_path_list:
                    # adds the file directory path to the
                    # directory path list
                    directory_path_list.append(resource_file_directory_path)

            # iterates over all the directory paths
            for directory_path in directory_path_list:
                # in case the directory path does not refers
                # a directory
                if not file_context.is_directory_path(directory_path):
                    # continues the loop
                    continue

                # removes the directories in the directory path
                file_context.remove_directory(directory_path, True)

            # commits the transaction
            file_context.commit()
        except:
            # rollsback the transaction
            file_context.rollback()

            # re-raises the exception
            raise

    def _uninstall_library(self, library_id, library_version, library, properties, file_context = None):
        """
        Method called upon removal of the library with
        the given id, version and properties.

        @type library_id: String
        @param library_id: The id of the library to be removed.
        @type library_version: String
        @param library_version: The version of the library to be removed.
        @type library: Dictionary
        @param library: The map containing the library description.
        @type properties: Dictionary
        @param properties: The map of properties for removal.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # retrieves the manager path
        manager_path = plugin_manager.get_manager_path()

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # retrieves the registry path
        registry_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH)

        # retrieves the libraries path
        libraries_path = plugin_manager.get_libraries_path()

        # retrieves the transaction properties
        transaction_properties = properties.get(TRANSACTION_PROPERTIES_VALUE, {})

        # creates a new file transaction context
        file_context = file_context or transaction_properties.get(FILE_CONTEXT_VALUE, None) or colony.libs.file_util.FileTransactionContext()

        # opens a new transaction in the file context
        file_context.open()

        try:
            # retrieves the library version as the library version
            # or from the library structure
            library_version = library_version or library[VERSION_VALUE]

            # creates the library file name from the library
            # id and version
            library_file_name = library_id + "_" + library_version + COLONY_CONTAINER_FILE_EXTENSION

            # creates the library file path from the
            library_path = os.path.join(registry_path, RELATIVE_CONTAINERS_PATH + "/" + library_file_name)

            # resolves the library path
            real_library_path = file_context.resolve_file_path(library_path)

            # retrieves the packing information
            packing_information = packing_manager_plugin.get_packing_information(real_library_path, {}, COLONY_VALUE)

            # retrieves the library resources
            library_resources = packing_information.get_property(RESOURCES_VALUE)

            # retrieves the library keep resources
            library_keep_resources = packing_information.get_property(KEEP_RESOURCES_VALUE, [])

            # retrieves the library extra resources
            library_extra_resources = packing_information.get_property(EXTRA_RESOURCES_VALUE, [])

            # filters the library resources that are meant to be kept in
            # the system and then extends the library resources list with
            # the library extra resources
            library_resources = [value for value in library_resources if not value in library_keep_resources]
            library_resources.extend(library_extra_resources)

            # creates the list of directory paths for (possible)
            # later removal
            directory_path_list = []

            # iterates over all the resources to remove them
            for library_resource in library_resources:
                # creates the (complete) resource file path
                resource_file_path = os.path.join(libraries_path, library_resource)

                # "calculates" the relative path between the resource file
                # path and the manager path
                resource_relative_path = colony.libs.path_util.relative_path(resource_file_path, manager_path)

                # aligns the path normalizing it into a system independent path
                resource_relative_path = colony.libs.path_util.align_path(resource_relative_path)

                # in case the resource file path exists
                if not file_context.exists_file_path(resource_file_path):
                    # continues the loop
                    continue

                # removes the resource file in the resource file path
                file_context.remove_file(resource_file_path)

                # retrieves the resource file directory path
                resource_file_directory_path = os.path.dirname(resource_file_path)

                # in case the resource file directory path is not yet
                # present in the directory path list
                if not resource_file_directory_path in directory_path_list:
                    # adds the file directory path to the
                    # directory path list
                    directory_path_list.append(resource_file_directory_path)

            # iterates over all the directory paths
            for directory_path in directory_path_list:
                # in case the directory path does not refers
                # a directory
                if not file_context.is_directory_path(directory_path):
                    # continues the loop
                    continue

                # removes the directories in the directory path
                file_context.remove_directory(directory_path, True)

            # commits the transaction
            file_context.commit()
        except:
            # rollsback the transaction
            file_context.rollback()

            # re-raises the exception
            raise

    def _uninstall_configuration(self, configuration_id, configuration_version, configuration, properties, file_context = None):
        """
        Method called upon removal of the configuration with
        the given id, version and properties.

        @type configuration_id: String
        @param configuration_id: The id of the configuration to be removed.
        @type configuration_version: String
        @param configuration_version: The version of the configuration to be removed.
        @type configuration: Dictionary
        @param configuration: The map containing the configuration description.
        @type properties: Dictionary
        @param properties: The map of properties for removal.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        pass

    def _deploy_package(self, package_path, target_path = None):
        """
        Deploys the package in the given path.
        In case the target path is not defined the main plugin path
        is used for deploying.

        @type package_path: String
        @param package_path: The path to the package to be deployed.
        @type target_path: String
        @param target_path: The path to the target of the deployment.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the packing manager plugin
        packing_manager_plugin = self.colony_packing_installer_plugin.packing_manager_plugin

        # retrieves the main plugin path
        main_plugin_path = plugin_manager.get_main_plugin_path()

        # sets the target path
        target_path = target_path or main_plugin_path

        # creates the properties map for the file unpacking packing
        properties = {
            TARGET_PATH_VALUE : target_path
        }

        # unpacks the files using the colony service
        packing_manager_plugin.unpack_files([package_path], properties, COLONY_VALUE)

    def _process_upgrade(self, package_id, package_version, properties, file_context):
        """
        Processes the upgrade part of the installation.

        @type package_id: String
        @param package_id: The id of the package to te upgraded.
        @type package_version: String
        @param package_version: The version of the package to te upgraded.
        @type properties: Dictionary
        @param properties: The map of properties for installation.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # checks if the package is already installed
        # (in case it "exists")
        exists_package = self.exists_package(package_id, file_context)

        # retrieves the upgrade property
        upgrade = properties.get(UPGRADE_VALUE, True)

        # in case the package does not already exists
        if not exists_package:
            # returns immediately
            return

        # in case the upgrade flag is set
        if upgrade:
            # removes the package in order to provide upgrade
            self.uninstall_package(package_id, package_version, properties, file_context)
        # otherwise
        else:
            # raises a plugin installation error
            raise colony_packing_installer_exceptions.PluginInstallationError("package with the same id already exists")

    def _touch_structure(self, structure):
        """
        Touches the structure, updating the timestamp
        references present in it.

        @type structure: Dictionary
        @param structure: The structure to be update with with
        new timestamps.
        """

        # retrieves the current time
        current_time = time.time()

        # retrieves the current date time
        current_date_time = datetime.datetime.utcnow()

        # formats the current date time
        current_date_time_formated = current_date_time.strftime("%d-%m-%Y %H:%M:%S")

        # updates the structure map with the current time
        # and date time values
        structure[LAST_MODIFIED_TIMESTAMP_VALUE] = current_time
        structure[LAST_MODIFIED_DATE_VALUE] = current_date_time_formated

    def _get_packages(self, file_context):
        """
        Retrieves the packages structure.

        @type file_context: FileContext
        @param file_context: The file context to be used.
        @rtype: Dictionary
        @return: The retrieved bundles structure.
        """

        return self.__get_structure(file_context, PACKAGES_FILE_NAME)

    def _get_bundles(self, file_context):
        """
        Retrieves the bundles structure.

        @type file_context: FileContext
        @param file_context: The file context to be used.
        @rtype: Dictionary
        @return: The retrieved bundles structure.
        """

        return self.__get_structure(file_context, BUNDLES_FILE_NAME)

    def _get_plugins(self, file_context):
        """
        Retrieves the plugins structure.

        @type file_context: FileContext
        @param file_context: The file context to be used.
        @rtype: Dictionary
        @return: The retrieved plugins structure.
        """

        return self.__get_structure(file_context, PLUGINS_FILE_NAME)

    def _get_containers(self, file_context):
        """
        Retrieves the containers structure.

        @type file_context: FileContext
        @param file_context: The file context to be used.
        @rtype: Dictionary
        @return: The retrieved plugins structure.
        """

        return self.__get_structure(file_context, CONTAINERS_FILE_NAME)

    def _add_package_item(self, item_key, item_value, file_context, update_time = True):
        """
        Adds a package item to the packages file structure.

        @type item_key: String
        @param item_key: The key to the item to be added.
        @type item_value: Dictionary
        @param item_value: The map containing the item value to be added.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        @type update_time: bool
        @param update_time: If the timetamp value should be updated.
        """

        self.__add_structure_item(item_key, item_value, file_context, update_time, PACKAGES_FILE_NAME, INSTALLED_PACKAGES_VALUE)

    def _add_bundle_item(self, item_key, item_value, file_context, update_time = True):
        """
        Adds a bundle item to the bundles file structure.

        @type item_key: String
        @param item_key: The key to the item to be added.
        @type item_value: Dictionary
        @param item_value: The map containing the item value to be added.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        @type update_time: bool
        @param update_time: If the timetamp value should be updated.
        """

        self.__add_structure_item(item_key, item_value, file_context, update_time, BUNDLES_FILE_NAME, INSTALLED_BUNDLES_VALUE)

    def _add_plugin_item(self, item_key, item_value, file_context, update_time = True):
        """
        Adds a plugin item to the plugins file structure.

        @type item_key: String
        @param item_key: The key to the item to be added.
        @type item_value: Dictionary
        @param item_value: The map containing the item value to be added.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        @type update_time: bool
        @param update_time: If the timetamp value should be updated.
        """

        self.__add_structure_item(item_key, item_value, file_context, update_time, PLUGINS_FILE_NAME, INSTALLED_PLUGINS_VALUE)

    def _add_container_item(self, item_key, item_value, file_context, update_time = True):
        """
        Adds a container item to the containers file structure.

        @type item_key: String
        @param item_key: The key to the item to be added.
        @type item_value: Dictionary
        @param item_value: The map containing the item value to be added.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        @type update_time: bool
        @param update_time: If the timetamp value should be updated.
        """

        self.__add_structure_item(item_key, item_value, file_context, update_time, CONTAINERS_FILE_NAME, INSTALLED_CONTAINERS_VALUE)

    def _remove_package_item(self, item_key, file_context):
        """
        Removes a package item from the packages file structure.

        @type item_key: String
        @param item_key: The key to the item to be removed.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        self.__remove_structure_item(item_key, file_context, PACKAGES_FILE_NAME, INSTALLED_PACKAGES_VALUE)

    def _remove_bundle_item(self, item_key, file_context):
        """
        Removes a bundle item from the bundles file structure.

        @type item_key: String
        @param item_key: The key to the item to be removed.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        self.__remove_structure_item(item_key, file_context, BUNDLES_FILE_NAME, INSTALLED_BUNDLES_VALUE)

    def _remove_plugin_item(self, item_key, file_context):
        """
        Removes a plugin item from the bundles file structure.

        @type item_key: String
        @param item_key: The key to the item to be removed.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        self.__remove_structure_item(item_key, file_context, PLUGINS_FILE_NAME, INSTALLED_PLUGINS_VALUE)

    def _remove_container_item(self, item_key, file_context):
        """
        Removes a container item from the bundles file structure.

        @type item_key: String
        @param item_key: The key to the item to be removed.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        self.__remove_structure_item(item_key, file_context, CONTAINERS_FILE_NAME, INSTALLED_CONTAINERS_VALUE)

    def _get_duplicates_structure(self, file_context):
        """
        Retrieves the duplicates structure from the file system.

        @rtype: Dictionary
        @return: The duplicates structure retrieved from the
        file system.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the json plugin
        json_plugin = self.colony_packing_installer_plugin.json_plugin

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # retrieves the registry path
        registry_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH)

        # creates the structure file path
        structure_file_path = os.path.join(registry_path, DUPLICATES_FILE_NAME)

        # reads the structure file contents
        structure_file_contents = file_context.read_file(structure_file_path)

        # loads the structure file contents from json
        structure = json_plugin.loads(structure_file_contents)

        # returns the structure
        return structure

    def _persist_duplicates_structure(self, duplicates_structure, file_context):
        """
        Persists the given duplicates structure into
        the file system.

        @type duplicates_structure: Dictionary
        @param duplicates_structure: The duplicates structure to be
        persisted into the file system.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the json plugin
        json_plugin = self.colony_packing_installer_plugin.json_plugin

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # retrieves the registry path
        registry_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH)

        # creates the structure file path
        structure_file_path = os.path.join(registry_path, DUPLICATES_FILE_NAME)

        # touches the duplicates structure (internal structure)
        # updating the dates in it
        self._touch_structure(duplicates_structure)

        # serializes the structure
        structure_serialized = json_plugin.dumps_pretty(duplicates_structure)

        # writes the structure file contents
        file_context.write_file(structure_file_path, structure_serialized)

    def __get_structure(self, file_context, structure_file_name):
        """
        Retrieves the structure from the structure file.

        @type file_context: FileContext
        @param file_context: The file context to be used.
        @type structure_file_name: String
        @param structure_file_name: The name of the structure file to be used.
        @rtype: Dictionary
        @return: The structure retrieved from the structure file.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the json plugin
        json_plugin = self.colony_packing_installer_plugin.json_plugin

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # retrieves the registry path
        registry_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH)

        # creates the structure file path
        structure_file_path = os.path.join(registry_path, structure_file_name)

        # reads the structure file contents
        structure_file_contents = file_context.read_file(structure_file_path)

        # loads the structure file contents from json
        structure = json_plugin.loads(structure_file_contents)

        # returns the structure
        return structure

    def __add_structure_item(self, item_key, item_value, file_context, update_time, structure_file_name, structure_key_name):
        """
        Adds a new structure item to an existing structures file.

        @type item_key: String
        @param item_key: The key to the item to be added.
        @type item_value: Dictionary
        @param item_value: The map containing the item value to be added.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        @type update_time: bool
        @param update_time: If the timetamp value should be updated.
        @type structure_file_name: String
        @param structure_file_name: The name of the structure file to be used.
        @type structure_key_name: String
        @param structure_key_name: The key to the structure base item.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the json plugin
        json_plugin = self.colony_packing_installer_plugin.json_plugin

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # retrieves the registry path
        registry_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH)

        # creates the structure file path
        structure_file_path = os.path.join(registry_path, structure_file_name)

        # reads the structure file contents
        structure_file_contents = file_context.read_file(structure_file_path)

        # loads the structure file contents from json
        structure = json_plugin.loads(structure_file_contents)

        # retrieves the installed structure
        installed_structure = structure.get(structure_key_name, {})

        # in case the update time flag is set
        if update_time:
            # retrieves the current time
            current_time = time.time()

            # sets the item value
            item_value[TIMESTAMP_VALUE] = current_time

        # sets the installed structure map
        installed_structure[item_key] = item_value

        # touches the structure (internal structure)
        # updating the dates in it
        self._touch_structure(structure)

        # serializes the structure
        structure_serialized = json_plugin.dumps_pretty(structure)

        # writes the structure file contents
        file_context.write_file(structure_file_path, structure_serialized)

    def __remove_structure_item(self, item_key, file_context, structure_file_name, structure_key_name):
        """
        Removes a structure item from an existing structures file.

        @type item_key: String
        @param item_key: The key to the item to be removed.
        @type file_context: FileContext
        @param file_context: The file context to be used.
        @type structure_file_name: String
        @param structure_file_name: The name of the structure file to be used.
        @type structure_key_name: String
        @param structure_key_name: The key to the structure base item.
        """

        # retrieves the plugin manager
        plugin_manager = self.colony_packing_installer_plugin.manager

        # retrieves the json plugin
        json_plugin = self.colony_packing_installer_plugin.json_plugin

        # retrieves the variable path
        variable_path = plugin_manager.get_variable_path()

        # retrieves the registry path
        registry_path = os.path.join(variable_path, RELATIVE_REGISTRY_PATH)

        # creates the structure file path
        structure_file_path = os.path.join(registry_path, structure_file_name)

        # reads the structure file contents
        structure_file_contents = file_context.read_file(structure_file_path)

        # loads the structure file contents from json
        structure = json_plugin.loads(structure_file_contents)

        # retrieves the installed structure
        installed_structure = structure.get(structure_key_name, {})

        # in case the item key is not present in the
        # installed structure
        if not item_key in installed_structure:
            # raises a plugin installation error
            raise colony_packing_installer_exceptions.PluginInstallationError("item key '%s' does not exist" % item_key)

        # removes the item from the installed structure
        del installed_structure[item_key]

        # touches the structure (internal structure)
        # updating the dates in it
        self._touch_structure(structure)

        # serializes the structure
        structure_serialized = json_plugin.dumps_pretty(structure)

        # writes the structure file contents
        file_context.write_file(structure_file_path, structure_serialized)
