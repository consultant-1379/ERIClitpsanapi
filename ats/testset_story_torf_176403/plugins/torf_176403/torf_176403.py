##############################################################################
# Copyright Ericsson AB 2017
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
#
##############################################################################

from litp.core.plugin import Plugin
from litp.core.execution_manager import CallbackTask


class Torf_176403(Plugin):

    def create_configuration(self, plugin_api_context):

        a_node = plugin_api_context.query("node")[0]
        task = CallbackTask(a_node,
                            "Mock operation on any Node",
                            self.cb_dummy_task,
                            node_name=a_node.hostname)
        return [task]

    def cb_dummy_task(self, host_name):
        """Dummy Task"""
        pass
