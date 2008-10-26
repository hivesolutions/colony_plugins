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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import xml.dom.minidom

class Parser:
    """
    The abstract parser class
    """

    def __init__(self):
        """
        Constructor of the class
        """

        pass

    def parse(self):
        """
        Parses the defined file
        """

        pass

    def get_value(self):
        """
        Retrieves the result of the parse
        
        @rtype: Object
        @return: The result of the parse
        """

        pass

class BuildAutomationFileParser(Parser):
    """
    The build automation file parser class.
    """

    file = None
    """ The file path """

    build_automation = None
    """ The build automation """

    def __init__(self, file = None):
        Parser.__init__(self)
        self.file = file

    def parse(self):
        self.load_build_automation_file(self.file)

    def get_value(self):
        return self.build_automation

    def get_build_automation(self):
        return self.build_automation

    def load_build_automation_file(self, file):
        # creates the xml doument DOM object
        xml_document = xml.dom.minidom.parse(file)
        child_nodes = xml_document.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.build_automation = self.parse_build_automation(child_node)

    def parse_build_automation(self, build_automation):
        build_automation_structure = BuildAutomation()
        child_nodes = build_automation.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_build_automation_element(child_node, build_automation_structure)

        return build_automation_structure

    def parse_build_automation_element(self, build_automation_element, build_automation):
        node_name = build_automation_element.nodeName

        if node_name == "artifact":
            build_automation.artifact = self.parse_build_automation_artifact(build_automation_element)
        #elif node_name == "build":
        #    build_automation.build = self.parse_build_automation_build(build_automation_element)
        #elif node_name == "profiles":
        #    build_automation.profiles = self.parse_build_automation_profiles(build_automation_element)

    def parse_build_automation_artifact(self, build_automation_artifact):
        artifact = Artifact()
        child_nodes = build_automation_artifact.childNodes

        for child_node in child_nodes:
            if valid_node(child_node):
                self.parse_build_automation_artifact_element(child_node, artifact)

        return artifact

    def parse_build_automation_artifact_element(self, build_automation_artifact_element, artifact):
        node_name = build_automation_artifact_element.nodeName

        if node_name == "id":
            artifact.id = self.parse_build_automation_artifact_id(build_automation_artifact_element)
        elif node_name == "version":
            artifact.version = self.parse_build_automation_artifact_version(build_automation_artifact_element)
        elif node_name == "type":
            artifact.type = self.parse_build_automation_artifact_type(build_automation_artifact_element)
        elif node_name == "name":
            artifact.name = self.parse_build_automation_artifact_name(build_automation_artifact_element)
        elif node_name == "description":
            artifact.description = self.parse_build_automation_artifact_description(build_automation_artifact_element)

    def parse_build_automation_artifact_id(self, artifact_id):
        build_automation_artifact_id = artifact_id.firstChild.data.strip()
        return build_automation_artifact_id

    def parse_build_automation_artifact_version(self, artifact_version):
        build_automation_artifact_version = artifact_version.firstChild.data.strip()
        return build_automation_artifact_version

    def parse_build_automation_artifact_type(self, artifact_type):
        build_automation_artifact_type = artifact_type.firstChild.data.strip()
        return build_automation_artifact_type

    def parse_build_automation_artifact_name(self, artifact_name):
        build_automation_artifact_name = artifact_name.firstChild.data.strip()
        return build_automation_artifact_name

    def parse_build_automation_artifact_description(self, artifact_description):
        build_automation_artifact_description = artifact_description.firstChild.data.strip()
        return build_automation_artifact_description

class BuildAutomation:
    """
    The build automation class.
    """

    artifact = None
    build = None
    profiles = []

    def __init__(self, artifact = None, build = None):
        self.artifact = artifact
        self.build = build
        self.profiles = []

class Artifact:
    """
    The artifact class.
    """

    id = "none"
    version = "none"
    type = "none"
    name = "none"
    description = "none"

    def __init__(self, id = "none", version = "none", type = "none", name = "none", description = "none"):
        self.id = id
        self.version = version
        self.type = type
        self.name = name
        self.description = description

class Build:
    """
    The build class.
    """

    pass

class Plugin:
    """
    The plugin class.
    """

    pass

class Profile:
    """
    The profile class.
    """

    pass

def valid_node(node):
    """
    Gets if a node is valid or not for parsing.
    
    @type node: Node
    @param node: The Xml node to be validated.
    @rtype: bool
    @return: The valid or not valid value.
    """

    if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
        return True
    else:
        return False
