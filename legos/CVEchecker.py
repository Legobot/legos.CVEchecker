#!/usr/bin/env python

import logging

from Legobot.Lego import Lego
from Legobot.Utilities import Utilities as utils

__author__ = "Nitrax <nitrax@lokisec.fr>"
__copyright__ = "Copyright 2017, Legobot"

logger = logging.getLogger(__name__)


class LegoCVEchecker(Lego):
    """LegoCVEchecker allows to perform researches on CVEs.

    Args:
        Lego: Lego
    """

    @staticmethod
    def listening_for(message):
        """Check if the message contains a command that LegoCVEchecker support.

        Args:
            message: The message send by the Legobot framework

        Returns:
            Bool: Return True if the command is supported
        """
        if utils.isNotEmpty(message['text']):
            return message['text'].startswith('!cve')

    def handle(self, message):
        tokens = message['text'].split()

        if ' ' in message['text']:
            if len(tokens) > 2:
                try:
                    self._parse(tokens)
                except IndexError:
                    self.reply(message, 'Syntax error: !help CVEchecker for further information', self._handle_opts(message))
        else:
            self.reply(message, 'Syntax error: !help CVEchecker for further information', self._handle_opts(message))

    def _parse(self, tokens):
        """Parse parameters

        Args:
            self: self
            tokens: tokens
        """
        opts = [
            {'param': '-s', 'value': None},
            {'param': '--limit', 'value': 10},
            {'param': '--severity', 'value': 'low'}
        ]

        for i in range(1, len(tokens)):
            for opt in opts:
                if tokens[i] in opt['param']:
                    opt['value'] = tokens[i + 1]
                    break

        return opts

    def _handle_opts(self, message):
        """Identify and set the message sourche channel.

        Args:
            self: self
            message: The message send by the Legobot framework

        Returns:
            Array: Options needed to send back the response to the
                Legobot framework
        """
        try:
            target = message['metadata']['source_channel']
            opts = {'target': target}
        except IndexError:
            opts = None
            logger.error('''Could not identify message source in message:
                                    {}'''.format(str(message)))

        return opts

    @staticmethod
    def get_name():
        """Get the class name.

        Args:
            self: self

        Returns:
            str: Class name
        """
        return 'CVEchecker'

    @staticmethod
    def get_help():
        """Get helper

        Args:
            self: self

        Returns:
            str: Helper
        """
        return '!cve -s {query | CVE} --limit NB --severity {low | medium | high}'
