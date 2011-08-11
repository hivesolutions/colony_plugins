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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import threading

import colony.libs.path_util

import system_updater_parser
import system_updater_exceptions

TEMP_DIRECTORY = "system_updater_tmp"
""" The temporary directory """

RESOURCES_PATH = "system_updater/updater/resources"
""" The resources path """

REPOSITORIES_FILE_NAME = "repositories.xml"
""" The repositories file name """

REPOSITORY_DESCRIPTOR_FILE = "repository_descriptor.xml"
""" The repository descriptor file """

SIMPLE_REPOSITORY_LAYOUT_VALUE = "simple"
""" The simple repository layout value """

EXTENDED_REPOSITORY_LAYOUT_VALUE = "extended"
""" The extended repository layout value """

BUNDLES_VALUE = "bundles"
""" The bundles value """

PLUGINS_VALUE = "plugins"
""" The plugins value """

CONTAINERS_VALUE = "containers"
""" The containers value """

VERSION_VALUE = "version"
""" The version value """

HASH_DIGEST_VALUE = "hash_digest"
""" The hash digest value """

NOT_INSTALLED_STATUS = "not_installed"
""" The not installed status """

NEWER_VERSION_STATUS = "newer_version"
""" The newer version status """

OLDER_VERSION_STATUS = "older_version"
""" The older version status """

SAME_VERSION_STATUS = "same_version"
""" The same version status """

DIFFERENT_DIGEST_STATUS = "different_digest"
""" The different digest status """

class SystemUpdater:
    """
    The system updater class.
    """

    system_updater_plugin = None
    """ The system updater plugin """

    system_updater_lock = None
    """ The system updater lock """

    repository_list = []
    """ The list of repositories """

    repository_descriptor_list = []
    """ The list of repository descriptors """

    repository_repository_descriptor_map = {}
    """ The map associating the repository with the repository descriptor """

    repository_descriptor_repository_map = {}
    """ The map associating the repository descriptor with the repository """

    deployer_plugins_map = {}
    """ The deployer plugins map """

    def __init__(self, system_updater_plugin):
        """
        Constructor of the class.

        @type system_updater_plugin: SystemUpdaterPlugin
        @param system_updater_plugin: The system updater plugin.
        """

        self.system_updater_plugin = system_updater_plugin

        self.system_updater_lock = threading.RLock()
        self.repository_list = []
        self.repository_descriptor_list = []
        self.repository_repository_descriptor_map = {}
        self.repository_descriptor_repository_map = {}
        self.deployer_plugins_map = {}

    def load_system_updater(self):
        """
        Loads the system updater.
        """

        self.load_repositories_file()

    def load_repositories_file(self):
        """
        Loads the repositories file.
        """

        # retrieves the plugin manager
        plugin_manager = self.system_updater_plugin.manager

        # retrieves the system updater plugin id
        system_updater_plugin_id = self.system_updater_plugin.id

        # retrieves the system updater plugin path
        system_updater_plugin_path = plugin_manager.get_plugin_path_by_id(system_updater_plugin_id)

        # creates the resources path from the system updater plugin path
        resources_path = os.path.join(system_updater_plugin_path, RESOURCES_PATH)

        # creates the repositories file path from the repositories file
        # path relative path
        repositories_file_path = os.path.join(resources_path, REPOSITORIES_FILE_NAME)

        # resolves the configuration file path
        configuration_file_path = plugin_manager.resolve_file_path("%configuration:" + system_updater_plugin_id + "%/" + REPOSITORIES_FILE_NAME, True)

        # ensures that the configuration file path exists and contains the default contents
        colony.libs.path_util.ensure_file_path(configuration_file_path, repositories_file_path)

        # creates the repositories file parser for the
        repositories_file_parser = system_updater_parser.RepositoriesFileParser(configuration_file_path)

        # parses the repositories file using the repositories file parser
        repositories_file_parser.parse()

        # retrieves the repository list from the repositories file parser
        self.repository_list = repositories_file_parser.get_value()

    def load_repositories_information(self):
        """
        Loads the repository information for each of the repositories.
        This method is called to flush the current repository information.
        """

        # in case the repository descriptor list
        # is already populated (a successful run
        # of the load has been completed)
        if self.repository_descriptor_list:
            # returns immediately
            return

        # iterates over all the repositories in the
        # repository list
        for repository in self.repository_list:
            # retrieves the repository information (descriptor)
            repository_descriptor = self.get_repository_information(repository)

            # adds the repository descriptor to the repository descriptor list
            self.repository_descriptor_list.append(repository_descriptor)

    def get_repositories(self):
        """
        Retrieves the list of available repositories.

        @rtype: List
        @return: The list of available repositories.
        """

        return self.repository_list

    def get_repository_by_repository_name(self, repository_name):
        """
        Retrieves the repository structure for the given repository name.

        @type repository_name: String
        @param repository_name: The name of the repository to get the repository structure.
        @rtype: Repository
        @return: The repository structure for the given repository name.
        """

        # iterates over the repository list
        for repository in self.repository_list:
            # in case the repository name does not matches
            if not repository.name == repository_name:
                # continues the loop
                continue

            # returns the repository
            return repository

    def get_repository_information_by_repository_name(self, repository_name):
        """
        Retrieves the repository descriptor for the given repository name.

        @type repository_name: String
        @param repository_name: The name of the repository to get the descriptor
        @rtype: RepositoryDescriptor
        @return: The repository descriptor for the given repository name
        """

        # iterates over the repository list
        for repository in self.repository_list:
            # in case the repository name does not matches
            if not repository.name == repository_name:
                # continues the loop
                continue

            # retrieves the repository information for the repository
            return self.get_repository_information(repository)

    def get_package_information_list_by_repository_name(self, repository_name):
        """
        Retrieves the list of package information for the given repository name.

        @type repository_name: String
        @param repository_name: The name of the repository to get the list of package information.
        @rtype: List
        @return: The list of package information for the given repository name.
        """

        # retrieves the repository information for the repository name
        repository_information = self.get_repository_information_by_repository_name(repository_name)

        # returns the repository packages
        return repository_information.packages

    def get_plugin_information_list_by_repository_name(self, repository_name):
        """
        Retrieves the list of plugin information for the given repository name.

        @type repository_name: String
        @param repository_name: The name of the repository to get the list of plugin information.
        @rtype: List
        @return: The list of plugin information for the given repository name.
        """

        # retrieves the repository information for the repository name
        repository_information = self.get_repository_information_by_repository_name(repository_name)

        # returns the repository plugins
        return repository_information.plugins

    def get_repository_information(self, repository):
        """
        Retrieves the repository descriptor for the given repository.

        @type repository: Repository
        @param repository: The repository to get the descriptor.
        @rtype: RepositoryDescriptor
        @return: The repository descriptor for the given repository.
        """

        # in case the repository exists in the repository descriptor map
        if repository in self.repository_repository_descriptor_map:
            # retrieves the repository descriptor from the repository repository descriptor map
            repository_descriptor = self.repository_repository_descriptor_map[repository]
        # otherwise it must be retrieved (downloaded)
        else:
            # retrieves the repository descriptor file (downloading it)
            repository_descriptor_file = self.get_repository_descriptor_file(repository.addresses)

            # creates the repository descriptor file parser
            repository_descriptor_file_parser = system_updater_parser.RepositoryDescriptorFileParser(repository_descriptor_file)

            # parses the repository descriptor file
            repository_descriptor_file_parser.parse()

            # retrieves the repository descriptor (value) from the repository
            # descriptor file parser
            repository_descriptor = repository_descriptor_file_parser.get_value()

            # sets the repository descriptor in the repository repository descriptor map
            self.repository_repository_descriptor_map[repository] = repository_descriptor

            # sets the repository in the repository descriptor repository map
            self.repository_descriptor_repository_map[repository_descriptor] = repository

            # runs a post-parse processing in the repository descriptor
            self._process_respository_descriptor(repository_descriptor)

        # returns the repository descriptor
        return repository_descriptor

    def get_repository_descriptor_file(self, repository_addresses):
        """
        Retrieves the repository descriptor file for the given repository addresses.

        @type repository_addresses: List
        @param repository_addresses: The repository addresses to search.
        @rtype: Stream
        @return: The stream containing the repository descriptor for the given repository addresses.
        """

        # retrieves the downloader plugin
        downloader_plugin = self.system_updater_plugin.downloader_plugin

        # iterates over all the repositories
        for repository_address in repository_addresses:
            # prints an info message
            self.system_updater_plugin.info("Trying address %s (%s)" % (repository_address.name, repository_address.value))

            # retrieves the repository address value
            repository_address_value = repository_address.value

            # creates the repository file address, using the repository
            # address value
            repository_file_address = repository_address_value + "/" + REPOSITORY_DESCRIPTOR_FILE

            # retrieves the file buffer using the downloader plugin
            file_buffer = downloader_plugin.get_download_package_stream(repository_file_address)

            # in case the download was not successful
            if not file_buffer:
                # continues the loop
                continue

            # returns the file buffer
            return file_buffer

        # raises the file not found exception
        raise system_updater_exceptions.FileNotFoundException("repository descriptor not found")

    def install_package(self, package_id, package_version = None, transaction_properties = None):
        """
        Installs the package with the given id and version
        from a random repository.

        @type package_id: String
        @param package_id: The id of the package to install.
        @type package_version: String
        @param package_version: The version of the package to install.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # acquires the system updater lock
        self.system_updater_lock.acquire()

        try:
            # installs the package (concrete)
            self._install_package(package_id, package_version, transaction_properties)
        finally:
            # releases the system updater lock
            self.system_updater_lock.release()

    def install_bundle(self, bundle_id, bundle_version = None, transaction_properties = None):
        """
        Installs the plugin with the given id and version
        from a random repository.

        @type bundle_id: String
        @param bundle_id: The id of the bundle to install.
        @type bundle_version: String
        @param bundle_version: The version of the bundle to install.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # acquires the system updater lock
        self.system_updater_lock.acquire()

        try:
            # installs the bundle (concrete)
            self._install_bundle(bundle_id, bundle_version, transaction_properties)
        finally:
            # releases the system updater lock
            self.system_updater_lock.release()

    def install_plugin(self, plugin_id, plugin_version = None, transaction_properties = None):
        """
        Installs the plugin with the given id and version from
        a random repository.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to install.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to install.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # acquires the system updater lock
        self.system_updater_lock.acquire()

        try:
            # installs the plugin (concrete)
            self._install_plugin(plugin_id, plugin_version, transaction_properties)
        finally:
            # releases the system updater lock
            self.system_updater_lock.release()

    def install_container(self, container_id, container_version = None, transaction_properties = None):
        """
        Installs the container with the given id and version from
        a random repository.

        @type container_id: String
        @param container_id: The id of the container to install.
        @type container_version: String
        @param container_version: The version of the container to install.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # acquires the system updater lock
        self.system_updater_lock.acquire()

        try:
            # installs the container (concrete)
            self._install_container(container_id, container_version, transaction_properties)
        finally:
            # releases the system updater lock
            self.system_updater_lock.release()

    def uninstall_package(self, package_id, package_version = None, transaction_properties = None):
        """
        Uninstalls the package with the given id and version.

        @type package_id: String
        @param package_id: The id of the package to uninstall.
        @type package_version: String
        @param package_version: The version of the package to uninstall.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # acquires the system updater lock
        self.system_updater_lock.acquire()

        try:
            # uninstalls the package (concrete)
            self._uninstall_package(package_id, package_version, transaction_properties)
        finally:
            # releases the system updater lock
            self.system_updater_lock.release()

    def uninstall_bundle(self, bundle_id, bundle_version = None, transaction_properties = None):
        """
        Uninstalls the plugin with the given id and version
        from a random repository.

        @type bundle_id: String
        @param bundle_id: The id of the bundle to uninstall.
        @type bundle_version: String
        @param bundle_version: The version of the bundle to uninstall.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # acquires the system updater lock
        self.system_updater_lock.acquire()

        try:
            # uninstalls the bundle (concrete)
            self._uninstall_bundle(bundle_id, bundle_version, transaction_properties)
        finally:
            # releases the system updater lock
            self.system_updater_lock.release()

    def uninstall_plugin(self, plugin_id, plugin_version = None, transaction_properties = None):
        """
        Uninstalls the plugin with the given id and version from
        a random repository.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to uninstall.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to uninstall.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # acquires the system updater lock
        self.system_updater_lock.acquire()

        try:
            # uninstalls the plugin (concrete)
            self._uninstall_plugin(plugin_id, plugin_version, transaction_properties)
        finally:
            # releases the system updater lock
            self.system_updater_lock.release()

    def uninstall_container(self, container_id, container_version = None, transaction_properties = None):
        """
        Uninstalls the container with the given id and version from
        a random repository.

        @type container_id: String
        @param container_id: The id of the container to uninstall.
        @type container_version: String
        @param container_version: The version of the container to uninstall.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # acquires the system updater lock
        self.system_updater_lock.acquire()

        try:
            # uninstalls the container (concrete)
            self._uninstall_container(container_id, container_version, transaction_properties)
        finally:
            # releases the system updater lock
            self.system_updater_lock.release()

    def deployer_load(self, deployer_plugin):
        # retrieves the plugin deployer type
        deployer_type = deployer_plugin.get_deployer_type()

        self.deployer_plugins_map[deployer_type] = deployer_plugin

    def deployer_unload(self, deployer_plugin):
        # retrieves the plugin deployer type
        deployer_type = deployer_plugin.get_deployer_type()

        del self.deployer_plugins_map[deployer_type]

    def get_repositories_list(self):
        """
        Retrieves the list of available repositories.

        @rtype: List
        @return: The list of available repositories.
        """

        return self.repository_list

    def get_package_list(self):
        """
        Retrieves the list of available packages.

        @rtype: List
        @return: The list of available packages.
        """

        pass

    def get_plugin_list(self):
        """
        Retrieves the list of available plugins.

        @rtype: List
        @return: The list of available plugins.
        """

        pass

    def get_package_descriptor(self, package_id, package_version = None):
        """
        Retrieves the package descriptor for the given package id and version.

        @type package_id: String
        @param package_id: The id of the package to retrieve the package descriptor.
        @type package_version: String
        @param package_version: The version of the package to retrieve the package descriptor.
        @rtype: PackageDescriptor
        @return: The package descriptor for the package with the given id and version.
        """

        # iterates over all the repository descriptors available
        for repository_descriptor in self.repository_descriptor_list:
            # retrieves the package from the repository descriptor for the given
            # package id and version
            package_descripton = repository_descriptor.get_package(package_id, package_version)

            # in case package descriptor does not exists in current
            # repository descriptor
            if not package_descripton:
                # continues the loop
                continue

            # returns the package description
            return package_descripton

    def get_bundle_descriptor(self, bundle_id, bundle_version = None):
        """
        Retrieves the bundle descriptor for the given bundle id and version.

        @type bundle_id: String
        @param bundle_id: The id of the bundle to retrieve the bundle descriptor.
        @type bundle_version: String
        @param bundle_version: The version of the bundle to retrieve the bundle descriptor.
        @rtype: BundleDescriptor
        @return: The bundle descriptor for the bundle with the given id and version.
        """

        # iterates over all the repository descriptors available
        for repository_descriptor in self.repository_descriptor_list:
            # retrieves the bundle from the repository descriptor for the given
            # bundle id and version
            bundle_descripton = repository_descriptor.get_bundle(bundle_id, bundle_version)

            # in case bundle descriptor does not exists in current
            # repository descriptor
            if not bundle_descripton:
                # continues the loop
                continue

            # returns the bundle descriptor
            return bundle_descripton

    def get_plugin_descriptor(self, plugin_id, plugin_version = None):
        """
        Retrieves the plugin descriptor for the given plugin id and version.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to retrieve the plugin descriptor.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to retrieve the plugin descriptor.
        @rtype: PluginDescriptor
        @return: The plugin descriptor for the plugin with the given id and version.
        """

        # iterates over all the repository descriptors available
        for repository_descriptor in self.repository_descriptor_list:
            # retrieves the plugin from the repository descriptor for the given
            # plugin id and version
            plugin_descripton = repository_descriptor.get_plugin(plugin_id, plugin_version)

            # in case plugin descriptor does not exists in current
            # repository descriptor
            if not plugin_descripton:
                # continues the loop
                continue

            # returns the plugin descriptor
            return plugin_descripton

    def get_container_descriptor(self, container_id, container_version = None):
        """
        Retrieves the container descriptor for the given container id and version.

        @type container_id: String
        @param container_id: The id of the container to retrieve the container descriptor.
        @type container_version: String
        @param container_version: The version of the container to retrieve the container descriptor.
        @rtype: ContainerDescriptor
        @return: The container descriptor for the container with the given id and version.
        """

        # iterates over all the repository descriptors available
        for repository_descriptor in self.repository_descriptor_list:
            # retrieves the container from the repository descriptor for the given
            # container id and version
            container_descripton = repository_descriptor.get_container(container_id, container_version)

            # in case container descriptor does not exists in current
            # repository descriptor
            if not container_descripton:
                # continues the loop
                continue

            # returns the container descriptor
            return container_descripton

    def get_repository_descriptor_bundle_descriptor(self, bundle_descriptor):
        """
        Retrieves the repository descriptor for the given bundle descriptor.

        @type bundle_descriptor: bundleDescriptor
        @param bundle_descriptor: The bundle descriptor to get the repository descriptor.
        @rtype: RepositoryDescriptor
        @return: The repository descriptor for the given bundle descriptor.
        """

        for repository_descriptor in self.repository_descriptor_list:
            if bundle_descriptor in repository_descriptor.bundles:
                return repository_descriptor

    def get_repository_descriptor_plugin_descriptor(self, plugin_descriptor):
        """
        Retrieves the repository descriptor for the given plugin descriptor.

        @type plugin_descriptor: PluginDescriptor
        @param plugin_descriptor: The plugin descriptor to get the repository descriptor.
        @rtype: RepositoryDescriptor
        @return: The repository descriptor for the given plugin descriptor.
        """

        for repository_descriptor in self.repository_descriptor_list:
            if plugin_descriptor in repository_descriptor.plugins:
                return repository_descriptor

    def get_repository_descriptor_container_descriptor(self, container_descriptor):
        """
        Retrieves the repository descriptor for the given container descriptor.

        @type container_descriptor: ContainerDescriptor
        @param container_descriptor: The container descriptor to get the repository descriptor.
        @rtype: RepositoryDescriptor
        @return: The repository descriptor for the given container descriptor.
        """

        for repository_descriptor in self.repository_descriptor_list:
            if container_descriptor in repository_descriptor.containers:
                return repository_descriptor

    def _install_package(self, package_id, package_version = None, transaction_properties = None):
        """
        Installs the package with the given id and version
        from a random repository.

        @type package_id: String
        @param package_id: The id of the package to install.
        @type package_version: String
        @param package_version: The version of the package to install.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # loads the information for the repositories
        self.load_repositories_information()

        # retrieves the descriptor of the package
        package_descriptor = self.get_package_descriptor(package_id, package_version)

        # retrieves the package plugins
        package_plugins = package_descriptor.plugins

        # iterates over all the plugins in the plugin descriptor
        for plugin in package_plugins:
            # retrieves the plugin id and version
            plugin_id = plugin.id
            plugin_version = plugin.version

            # installs the plugin
            self.install_plugin(plugin_id, plugin_version, transaction_properties)

    def _install_bundle(self, bundle_id, bundle_version = None, transaction_properties = None):
        """
        Installs the plugin with the given id and version
        from a random repository.

        @type bundle_id: String
        @param bundle_id: The id of the bundle to install.
        @type bundle_version: String
        @param bundle_version: The version of the bundle to install.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # loads the information for the repositories
        self.load_repositories_information()

        # retrieves the descriptor of the bundle
        bundle_descriptor = self.get_bundle_descriptor(bundle_id, bundle_version)

        # in case the bundle was not found
        if not bundle_descriptor:
            # raises the invalid bundle exception
            raise system_updater_exceptions.InvalidBundleException("bundle %s v%s not found" % (bundle_id, bundle_version))

        # retrieves the bundle type
        bundle_type = bundle_descriptor.bundle_type

        # retrieves a deployer for the given plugin type
        plugin_deployer = self._get_deployer_plugin_by_deployer_type(bundle_type)

        # retrieves the current transaction properties or creates a new transaction
        transaction_properties = plugin_deployer.open_transaction(transaction_properties)

        try:
            # installs the bundle dependencies
            self._install_bundle_dependencies(bundle_descriptor, transaction_properties)

            # retrieves the repository descriptor from the bundle descriptor
            repository_descriptor = self.get_repository_descriptor_bundle_descriptor(bundle_descriptor)

            # retrieves the repository structure for the provided repository descriptor
            repository = self.repository_descriptor_repository_map[repository_descriptor]

            # retrieves the contents file
            contents_file = self._get_contents_file(repository.name, bundle_descriptor.name, bundle_descriptor.version, bundle_descriptor.contents_file, BUNDLES_VALUE)

            try:
                # sends the contents file (bundle) to the bundle type deployer
                # to allow it to be deployed, the transaction properties are
                # also sent for transaction control
                plugin_deployer.deploy_bundle(bundle_descriptor.id, bundle_descriptor.version, contents_file, transaction_properties)
            finally:
                # deletes the contents file
                self._delete_contents_file(contents_file)

            # commits the transaction represented in the
            # transaction properties
            plugin_deployer.commit_transaction(transaction_properties)
        except:
            # "rollsback" the transaction represented in the
            # transaction properties
            plugin_deployer.rollback_transaction(transaction_properties)

            # re-raises the exception
            raise

        # updates the bundle descriptor status
        bundle_descriptor.status = SAME_VERSION_STATUS

    def _install_plugin(self, plugin_id, plugin_version = None, transaction_properties = None):
        """
        Installs the plugin with the given id and version from
        a random repository.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to install.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to install.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # loads the information for the repositories
        self.load_repositories_information()

        # retrieves the descriptor of the plugin
        plugin_descriptor = self.get_plugin_descriptor(plugin_id, plugin_version)

        # in case the plugin was not found
        if not plugin_descriptor:
            # raises the invalid plugin exception
            raise system_updater_exceptions.InvalidPluginException("plugin %s v%s not found" % (plugin_id, plugin_version))

        # retrieves the plugin type
        plugin_type = plugin_descriptor.plugin_type

        # retrieves a deployer for the given plugin type
        plugin_deployer = self._get_deployer_plugin_by_deployer_type(plugin_type)

        # retrieves the current transaction properties or creates a new transaction
        transaction_properties = plugin_deployer.open_transaction(transaction_properties)

        try:
            # installs the plugin dependencies
            self._install_plugin_dependencies(plugin_descriptor, transaction_properties)

            # retrieves the repository descriptor from the plugin descriptor
            repository_descriptor = self.get_repository_descriptor_plugin_descriptor(plugin_descriptor)

            # retrieves the repository structure for the provided repository descriptor
            repository = self.repository_descriptor_repository_map[repository_descriptor]

            # retrieves the contents file
            contents_file = self._get_contents_file(repository.name, plugin_descriptor.name, plugin_descriptor.version, plugin_descriptor.contents_file, PLUGINS_VALUE)

            try:
                # sends the contents file (plugin) to the plugin type deployer
                # to allow it to be deployed, the transaction properties are
                # also sent for transaction control
                plugin_deployer.deploy_plugin(plugin_descriptor.id, plugin_descriptor.version, contents_file, transaction_properties)
            finally:
                # deletes the contents file
                self._delete_contents_file(contents_file)

            # commits the transaction represented in the
            # transaction properties
            plugin_deployer.commit_transaction(transaction_properties)
        except:
            # "rollsback" the transaction represented in the
            # transaction properties
            plugin_deployer.rollback_transaction(transaction_properties)

            # re-raises the exception
            raise

        # updates the plugin descriptor status
        plugin_descriptor.status = SAME_VERSION_STATUS

    def _install_container(self, container_id, container_version = None, transaction_properties = None):
        """
        Installs the container with the given id and version from
        a random repository.

        @type container_id: String
        @param container_id: The id of the container to install.
        @type container_version: String
        @param container_version: The version of the container to install.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # loads the information for the repositories
        self.load_repositories_information()

        # retrieves the descriptor of the container
        container_descriptor = self.get_container_descriptor(container_id, container_version)

        # in case the container was not found
        if not container_descriptor:
            # raises the invalid container exception
            raise system_updater_exceptions.InvalidContainerException("container %s v%s not found" % (container_id, container_version))

        # retrieves the container type
        container_type = container_descriptor.container_type

        # retrieves a deployer for the given container type
        plugin_deployer = self._get_deployer_plugin_by_deployer_type(container_type)

        # retrieves the current transaction properties or creates a new transaction
        transaction_properties = plugin_deployer.open_transaction(transaction_properties)

        try:
            # installs the container dependencies
            self._install_container_dependencies(container_descriptor, transaction_properties)

            # retrieves the repository descriptor from the container descriptor
            repository_descriptor = self.get_repository_descriptor_container_descriptor(container_descriptor)

            # retrieves the repository structure for the provided repository descriptor
            repository = self.repository_descriptor_repository_map[repository_descriptor]

            # retrieves the contents file
            contents_file = self._get_contents_file(repository.name, container_descriptor.name, container_descriptor.version, container_descriptor.contents_file, CONTAINERS_VALUE)

            try:
                # sends the contents file (container) to the plugin type deployer
                # to allow it to be deployed, the transaction properties are
                # also sent for transaction control
                plugin_deployer.deploy_container(container_descriptor.id, container_descriptor.version, contents_file, transaction_properties)
            finally:
                # deletes the contents file
                self._delete_contents_file(contents_file)

            # commits the transaction represented in the
            # transaction properties
            plugin_deployer.commit_transaction(transaction_properties)
        except:
            # "rollsback" the transaction represented in the
            # transaction properties
            plugin_deployer.rollback_transaction(transaction_properties)

            # re-raises the exception
            raise

        # updates the container descriptor status
        container_descriptor.status = SAME_VERSION_STATUS

    def _uninstall_package(self, package_id, package_version = None, transaction_properties = None):
        """
        Uninstalls the package with the given id and version
        from a random repository.

        @type package_id: String
        @param package_id: The id of the package to uninstall.
        @type package_version: String
        @param package_version: The version of the package to uninstall.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # loads the information for the repositories
        self.load_repositories_information()

        # retrieves the descriptor of the package
        package_descriptor = self.get_package_descriptor(package_id, package_version)

        # retrieves the package plugins
        package_plugins = package_descriptor.plugins

        # iterates over all the plugins in the plugin descriptor
        for plugin in package_plugins:
            # retrieves the plugin id and version
            plugin_id = plugin.id
            plugin_version = plugin.version

            # uninstalls the plugin
            self.uninstall_plugin(plugin_id, plugin_version, transaction_properties)

    def _uninstall_bundle(self, bundle_id, bundle_version = None, transaction_properties = None):
        """
        Uninstalls the plugin with the given id and version
        from a random repository.

        @type bundle_id: String
        @param bundle_id: The id of the bundle to uninstall.
        @type bundle_version: String
        @param bundle_version: The version of the bundle to uninstall.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # loads the information for the repositories
        self.load_repositories_information()

        # retrieves the descriptor of the bundle
        bundle_descriptor = self.get_bundle_descriptor(bundle_id, bundle_version)

        # in case the bundle was not found
        if not bundle_descriptor:
            # raises the invalid bundle exception
            raise system_updater_exceptions.InvalidBundleException("bundle %s v%s not found" % (bundle_id, bundle_version))

        # retrieves the bundle type
        bundle_type = bundle_descriptor.bundle_type

        # retrieves a deployer for the given plugin type
        plugin_deployer = self._get_deployer_plugin_by_deployer_type(bundle_type)

        # retrieves the current transaction properties or creates a new transaction
        transaction_properties = plugin_deployer.open_transaction(transaction_properties)

        try:
            # sends the bundle information to the plugin type deployer
            # to allow it to be undeployed, the transaction properties are
            # also sent for transaction control
            plugin_deployer.undeploy_bundle(bundle_descriptor.id, bundle_descriptor.version, transaction_properties)

            # commits the transaction represented in the
            # transaction properties
            plugin_deployer.commit_transaction(transaction_properties)
        except:
            # "rollsback" the transaction represented in the
            # transaction properties
            plugin_deployer.rollback_transaction(transaction_properties)

            # re-raises the exception
            raise

        # updates the bundle descriptor status
        bundle_descriptor.status = NOT_INSTALLED_STATUS

    def _uninstall_plugin(self, plugin_id, plugin_version = None, transaction_properties = None):
        """
        Uninstalls the plugin with the given id and version from
        a random repository.

        @type plugin_id: String
        @param plugin_id: The id of the plugin to uninstall.
        @type plugin_version: String
        @param plugin_version: The version of the plugin to uninstall.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # loads the information for the repositories
        self.load_repositories_information()

        # retrieves the descriptor of the plugin
        plugin_descriptor = self.get_plugin_descriptor(plugin_id, plugin_version)

        # in case the plugin was not found
        if not plugin_descriptor:
            # raises the invalid plugin exception
            raise system_updater_exceptions.InvalidPluginException("plugin %s v%s not found" % (plugin_id, plugin_version))

        # retrieves the plugin type
        plugin_type = plugin_descriptor.plugin_type

        # retrieves a deployer for the given plugin type
        plugin_deployer = self._get_deployer_plugin_by_deployer_type(plugin_type)

        # retrieves the current transaction properties or creates a new transaction
        transaction_properties = plugin_deployer.open_transaction(transaction_properties)

        try:
            # sends the bundle information to the plugin type deployer
            # to allow it to be undeployed, the transaction properties are
            # also sent for transaction control
            plugin_deployer.undeploy_bundle(plugin_descriptor.id, plugin_descriptor.version, transaction_properties)

            # commits the transaction represented in the
            # transaction properties
            plugin_deployer.commit_transaction(transaction_properties)
        except:
            # "rollsback" the transaction represented in the
            # transaction properties
            plugin_deployer.rollback_transaction(transaction_properties)

            # re-raises the exception
            raise

        # updates the plugin descriptor status
        plugin_descriptor.status = NOT_INSTALLED_STATUS

    def _uninstall_container(self, container_id, container_version = None, transaction_properties = None):
        """
        Uninstalls the container with the given id and version from
        a random repository.

        @type container_id: String
        @param container_id: The id of the container to uninstall.
        @type container_version: String
        @param container_version: The version of the container to uninstall.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # loads the information for the repositories
        self.load_repositories_information()

        # retrieves the descriptor of the container
        container_descriptor = self.get_container_descriptor(container_id, container_version)

        # in case the container was not found
        if not container_descriptor:
            # raises the invalid container exception
            raise system_updater_exceptions.InvalidContainerException("container %s v%s not found" % (container_id, container_version))

        # retrieves the container type
        container_type = container_descriptor.container_type

        # retrieves a deployer for the given container type
        plugin_deployer = self._get_deployer_plugin_by_deployer_type(container_type)

        # retrieves the current transaction properties or creates a new transaction
        transaction_properties = plugin_deployer.open_transaction(transaction_properties)

        try:
            # sends the bundle information to the plugin type deployer
            # to allow it to be undeployed, the transaction properties are
            # also sent for transaction control
            plugin_deployer.undeploy_bundle(container_descriptor.id, container_descriptor.version, transaction_properties)

            # commits the transaction represented in the
            # transaction properties
            plugin_deployer.commit_transaction(transaction_properties)
        except:
            # "rollsback" the transaction represented in the
            # transaction properties
            plugin_deployer.rollback_transaction(transaction_properties)

            # re-raises the exception
            raise

        # updates the container descriptor status
        container_descriptor.status = NOT_INSTALLED_STATUS

    def _get_deployer_plugin_by_deployer_type(self, deployer_type):
        """
        Retrieves a deployer plugin for the given deployer type.

        @type deployer_type : String
        @param deployer_type: The type of the deployer to retrieve.
        @rtype: Plugin
        @return: The deployer plugin for the given deployer type.
        """

        # in case the deployer type does not exist in the deployer
        # plugins map
        if not deployer_type in self.deployer_plugins_map:
            # raises the missing deployer exception
            raise system_updater_exceptions.MissingDeployer(deployer_type)

        # retrieves the deployer plugin from the deployer plugins map
        deployer_plugin = self.deployer_plugins_map[deployer_type]

        # returns the deployer plugin
        return deployer_plugin

    def _install_bundle_dependencies(self, bundle_descriptor, transaction_properties):
        """
        Install the bundle dependencies for the given bundle
        descriptor.

        @type bundle_descriptor: BundleDescriptor
        @param bundle_id: The bundle descriptor of the bundle to
        install the dependencies.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # retrieves the system registry plugin
        system_registry_plugin = self.system_updater_plugin.system_registry_plugin

        # retrieves the bundle dependencies
        bundle_dependencies = bundle_descriptor.dependencies

        # iterates over the bundle dependencies
        for bundle_dependency in bundle_dependencies:
            # retrieves the bundle information for the bundle dependency
            bundle_information = system_registry_plugin.get_bundle_information(bundle_dependency.id, bundle_dependency.version)

            # in case the bundle information is valid
            if bundle_information:
                # continues the loop
                continue

            try:
                # installs the bundle dependency
                self.install_bundle(bundle_dependency.id, bundle_dependency.version, transaction_properties)
            except Exception, exception:
                # raises the dependency installation exception
                raise system_updater_exceptions.DependencyInstallationException("problem installing bundle dependency %s v%s: %s" % (bundle_dependency.id, bundle_dependency.version, unicode(exception)))

    def _install_plugin_dependencies(self, plugin_descriptor, transaction_properties):
        """
        Install the plugin dependencies for the given plugin
        descriptor.

        @type plugin_descriptor: PluginDescriptor
        @param plugin_descriptor: The plugin descriptor of the plugin to
        install the dependencies.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # retrieves the system registry plugin
        system_registry_plugin = self.system_updater_plugin.system_registry_plugin

        # retrieves the plugin dependencies
        plugin_dependencies = plugin_descriptor.dependencies

        # iterates over the plugin dependencies
        for plugin_dependency in plugin_dependencies:
            # retrieves the plugin information for the plugin dependency
            plugin_information = system_registry_plugin.get_plugin_information(plugin_dependency.id, plugin_dependency.version)

            # in case the plugin information is valid
            if plugin_information:
                # continues the loop
                continue

            try:
                # installs the plugin dependency
                self.install_plugin(plugin_dependency.id, plugin_dependency.version, transaction_properties)
            except Exception, exception:
                # raises the dependency installation exception
                raise system_updater_exceptions.DependencyInstallationException("problem installing plugin depdency %s v%s: %s" % (plugin_dependency.id, plugin_dependency.version, unicode(exception)))

    def _install_container_dependencies(self, container_descriptor, transaction_properties):
        """
        Install the container dependencies for the given container
        descriptor.

        @type container_descriptor: ContainerDescriptor
        @param container_descriptor: The container descriptor of the container to
        install the dependencies.
        @type transaction_properties: Dictionary
        @param transaction_properties: The properties map for the
        current transaction.
        """

        # retrieves the system registry plugin
        system_registry_plugin = self.system_updater_plugin.system_registry_plugin

        # retrieves the container dependencies
        container_dependencies = container_descriptor.dependencies

        # iterates over the container dependencies
        for container_dependency in container_dependencies:
            # retrieves the container information for the container dependency
            container_information = system_registry_plugin.get_container_information(container_dependency.id, container_dependency.version)

            # in case the container information is valid
            if container_information:
                # continues the loop
                continue

            try:
                # installs the container dependency
                self.install_container(container_dependency.id, container_dependency.version, transaction_properties)
            except Exception, exception:
                # raises the dependency installation exception
                raise system_updater_exceptions.DependencyInstallationException("problem installing container depdency %s v%s: %s" % (container_dependency.id, container_dependency.version, unicode(exception)))

    def _get_contents_file(self, repository_name, content_name, content_version, contents_file, content_type = PLUGINS_VALUE):
        """
        Retrieves the content contents file for the given repository name,
        content name, content version and contents file name.

        @type repository_name: String
        @param repository_name: The name of the repository to use in the content contents file retrieval.
        @type content_name: String
        @param content_name: The name of the content to use in the content contents file retrieval.
        @type content_version: String
        @param content_version: The version of the content to use in the content contents file retrieval.
        @type contents_file: String
        @param contents_file: The name of the content contents file to retrieve.
        @type content_type: String
        @param content_type: The type of content to use in the content contents file retrieval.
        @rtype: Stream
        @return: The retrieved content contents file stream.
        """

        # retrieves the plugin manager
        plugin_manager = self.system_updater_plugin.manager

        # retrieves the repository structure for the given repository name
        repository = self.get_repository_by_repository_name(repository_name)

        # retrieves the repository addresses
        repository_addresses = repository.addresses

        # retrieves the repository layout
        repository_layout = repository.layout

        # retrieves the temporary path
        temporary_path = plugin_manager.get_temporary_path()

        # downloads the contents file
        self._download_contents_file(repository_addresses, content_name, content_version, contents_file, content_type, repository_layout, temporary_path)

        # the created contents file path
        contents_file_path = temporary_path + "/" + contents_file

        # the created contents file
        contents_file = open(contents_file_path, "r")

        # returns the contents file
        return contents_file

    def _download_contents_file(self, repository_addresses, content_name, content_version, contents_file, content_type = PLUGINS_VALUE, repository_layout = SIMPLE_REPOSITORY_LAYOUT_VALUE, target_directory = TEMP_DIRECTORY):
        """
        Downloads the content contents file for the given repository name, content name,
        content version and contents file name.

        @type repository_name: String
        @param repository_name: The name of the repository to use in the content
        contents file download.
        @type content_name: String
        @param content_name: The name of the content to use in the content contents
        file download.
        @type content_version: String
        @param content_version: The version of the content to use in the content
        contents file download.
        @type contents_file: String
        @param contents_file: The name of the content contents file to download.
        @type repository_layout: String
        @param repository_layout: The layout of the repository.
        @type target_directory: String
        @param target_directory: The target directory of the download.
        """

        # retrieves the downloader plugin
        downloader_plugin = self.system_updater_plugin.downloader_plugin

        # iterates over all the repository addresses
        for repository_address in repository_addresses:
            # prints an info message
            self.system_updater_plugin.info("Trying address %s (%s)" % (repository_address.name, repository_address.value))

            # retrieves the repository address value
            repository_address_value = repository_address.value

            # in case the layout of the repository is simple
            # (eg: content_type/content_id_version.ext)
            if SIMPLE_REPOSITORY_LAYOUT_VALUE:
                file_address = repository_address_value + "/" + content_type + "/" + contents_file
            # in case the layout of the repository is extended
            # (eg: content_type/content_name/content_version/content_id_version.ext)
            elif EXTENDED_REPOSITORY_LAYOUT_VALUE:
                file_address = repository_address_value + "/" +  content_type + "/" + content_name + "/" + content_version + "/" + contents_file

            try:
                # downloads the package for the given file address and target directory
                downloader_plugin.download_package(file_address, target_directory)
            except Exception, exception:
                # prints an info message
                self.system_updater_plugin.info("Failed retrieval of address %s (%s): %s" % (repository_address.name, repository_address.value, unicode(exception)))

                # continues the loop
                continue

            # returns immediately
            return

        # raises the file not found exception
        raise system_updater_exceptions.FileNotFoundException("contents file not found for content '%s' v%s" % (content_name, content_version))

    def _delete_contents_file(self, contents_file):
        """
        Deletes the given contents file.

        @type contents_file: File
        @param contents_file: The contents file to be
        deleted.
        """

        # closes the contents file
        contents_file.close()

        # retrieves the contents file path
        contents_file_path = contents_file.name

        # removes the contents file
        os.remove(contents_file_path)

    def _process_respository_descriptor(self, repository_descriptor):
        """
        Processes the given repository descriptor changing it's items
        according to the current system status.
        This method changes the repository descriptor and should be used
        in accordance to such.

        @type repository_descriptor: Repository
        @param repository_descriptor: The repository descritpro to be processed.
        """

        # retrieves the system registry plugin
        system_registry_plugin = self.system_updater_plugin.system_registry_plugin

        # retrieves the repository descriptor bundles, plugins and containers
        repository_descriptor_bundles = repository_descriptor.bundles
        repository_descriptor_plugins = repository_descriptor.plugins
        repository_descriptor_containers = repository_descriptor.containers

        # iterates over all the repository descriptor bundles to process them
        for repository_descriptor_bundle in repository_descriptor_bundles:
            # retrieves the bundle information
            bundle_information = system_registry_plugin.get_bundle_information(repository_descriptor_bundle.id, repository_descriptor_bundle.version)

            # process the repository descriptor bundle using the bundle information
            self._process_repository_item(repository_descriptor_bundle, bundle_information)

        # iterates over all the repository descriptor plugins to process them
        for repository_descriptor_plugin in repository_descriptor_plugins:
            # retrieves the plugin information
            plugin_information = system_registry_plugin.get_plugin_information(repository_descriptor_plugin.id, repository_descriptor_plugin.version)

            # process the repository descriptor plugin using the plugin information
            self._process_repository_item(repository_descriptor_plugin, plugin_information)

        # iterates over all the repository descriptor containers to process them
        for repository_descriptor_container in repository_descriptor_containers:
            # retrieves the container information
            container_information = system_registry_plugin.get_container_information(repository_descriptor_container.id, repository_descriptor_container.version)

            # process the repository descriptor container using the container information
            self._process_repository_item(repository_descriptor_container, container_information)

    def _process_repository_item(self, repository_descriptor_item, item_information):
        """
        Processes the repository descriptor item using the given item
        information map as data source.

        @type repository_descriptor_item: Repository
        @param repository_descriptor_item: The repository descriptor
        item to be processed.
        @type item_information: Dictionary
        @param item_information: The item information map to be used in the
        repository descriptor item processing.
        """

        # in case the item information is defined the
        # item is considered to be installed
        if item_information:
            # retrieves the item information values
            item_version = item_information.get(VERSION_VALUE, "0.0.0")
            item_hash_digest = item_information.get(HASH_DIGEST_VALUE, {})

            # in case the item version is superior to the currently
            # installed version
            if item_version > repository_descriptor_item.version:
                # sets the repository descriptor item status as newer version
                repository_descriptor_item.status = NEWER_VERSION_STATUS
            # in case the item version is the same as the currently
            # installed version
            elif item_version == repository_descriptor_item.version:
                # verifies the hash digest values from the repository descriptor
                # trying to find any mismatch
                valid_hash_digest_values = self._verify_hash_digest_values(repository_descriptor_item.hash_digest_items, item_hash_digest)

                # in case the hash digestr values are valid
                if valid_hash_digest_values:
                    # sets the repository descriptor item status as same version
                    repository_descriptor_item.status = SAME_VERSION_STATUS
                # otherwise it's a different version (based on digest only)
                else:
                    # sets the repository descriptor item status as different digest
                    repository_descriptor_item.status = DIFFERENT_DIGEST_STATUS
            # otherwise it's an inferior (older) version
            else:
                # sets the repository descriptor item status as older version
                repository_descriptor_item.status = OLDER_VERSION_STATUS
        # otherwise the defined itemis not installed
        else:
            # sets the repository descriptor item status as not installed
            repository_descriptor_item.status = NOT_INSTALLED_STATUS

    def _verify_hash_digest_values(self, hash_digest_items, item_hash_digest):
        """
        Verifies the given list of hash digest items against a map
        containing a set of hash digest values.

        @type hash_digest_items: List
        @param hash_digest_items: The list of hash digest items
        to be verified against the item hash digest.
        @type item_hash_digest: Dictionary
        @param item_hash_digest: The dictionary containing all the hash digest
        elements to be verified.
        @rtype: bool
        @return: The result of the hash digest verification.
        """

        # iterates over all the hash digest items
        # to check for any mismatch
        for hash_digest_item in hash_digest_items:
            # retrieves the hash digest item key and value
            hash_digest_item_key = hash_digest_item.key
            hash_digest_item_value = hash_digest_item.value

            # retrieves item hash digest value from the item hash digest
            item_hash_digest_value = item_hash_digest.get(hash_digest_item_key, None)

            # in the item hash digest value is not valid
            if not item_hash_digest_value:
                # continues the loop
                continue

            # in case the hash digest does not match
            if not item_hash_digest_value == hash_digest_item_value:
                # return false (invalid)
                return False

        # returns true (valid)
        return True
