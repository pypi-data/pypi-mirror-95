"""
Base classes and utilities for all Xena Manager (Xena) objects.

:author: yoram@ignissoft.com
"""

import logging

from xenavalkyrie.api.xena_socket import XenaSocket

logger = logging.getLogger(__name__)


class XenaCliWrapper(object):

    def __init__(self, logger):
        """ Init Xena REST API.

        :param looger: application logger.
        """

        self.logger = logger
        self.sockets_list = {}

    def connect(self, owner):
        self.owner = owner

    def disconnect(self):
        for chassis in self.sockets_list.values():
            chassis.disconnect()
        self.sockets_list = {}

    def add_chassis(self, chassis):
        """
        :param chassis: chassis object
        """

        socket = XenaSocket(self.logger, chassis.ip, chassis.port)
        socket.connect()
        self.sockets_list[chassis] = socket
        self.send_command(chassis, 'c_logon', '"{}"'.format(chassis.password))
        self.send_command(chassis, 'c_owner', '"{}"'.format(chassis.owner))

    def create(self, obj):
        self.send_command(obj, obj.create_command)

    def send_command(self, obj, command, *arguments):
        """ Send command and do not parse output (except for communication errors).

        :param obj: requested object.
        :param command: command to send.
        :param arguments: list of command arguments.
        """
        index_command = obj._build_index_command(command, *arguments)
        self.sockets_list[obj.chassis].sendQueryVerify(index_command)

    def send_command_return(self, obj, command, *arguments):
        """ Send command and wait for single line output. """
        index_command = obj._build_index_command(command, *arguments)
        return obj._extract_return(command, self.sockets_list[obj.chassis].sendQuery(index_command))

    def send_command_return_multilines(self, obj, command, *arguments):
        """ Send command and wait for multiple lines output. """
        index_command = obj._build_index_command(command, *arguments)
        return self.sockets_list[obj.chassis].sendQuery(index_command, True)

    def get_attribute(self, obj, attribute):
        """ Returns single object attribute.

        :param obj: requested object.
        :param attribute: requested attribute to query.
        :returns: returned value.
        :rtype: str
        """
        raw_return = self.send_command_return(obj, attribute, '?')
        if len(raw_return) > 2 and raw_return[0] == '"' and raw_return[-1] == '"':
            return raw_return[1:-1]
        return raw_return

    def get_attributes(self, obj):
        """ Get all object's attributes.

        Sends multi-parameter info/config queries and returns the result as dictionary.

        :param obj: requested object.
        :returns: dictionary of <name, value> of all attributes returned by the query.
        :rtype: dict of (str, str)
        """

        attributes = {}
        for info_config_command in obj._info_config_commands:
            index_commands_values = self.send_command_return_multilines(obj, info_config_command, '?')
            # poor implementation...
            li = obj._get_index_len()
            ci = obj._get_command_len()
            for index_command_value in index_commands_values:
                command = index_command_value.split()[ci].lower()
                if len(index_command_value.split()) > li + 1:
                    value = ' '.join(index_command_value.split()[li+1:]).replace('"', '')
                else:
                    value = ''
                attributes[command] = value
        return attributes

    def set_attributes(self, obj, **attributes):
        """ Set attributes.

        :param obj: requested object.
        :param attributes: dictionary of {attribute: value} to set
        """
        for attribute, value in attributes.items():
            self.send_command(obj, attribute, value)

    def get_stats(self, obj, stat_name):
        """ Send CLI command that returns list of integer counters.

        :param obj: requested object.
        :param stat_name: statistics command name.
        :return: list of counters.
        :rtype: list(int)
        """
        return [int(v) for v in self.get_attribute(obj, stat_name).split()]
