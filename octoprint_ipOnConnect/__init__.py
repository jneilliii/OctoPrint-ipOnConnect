# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import socket

class ipOnConnectPlugin():

	def message_on_connect(comm, script_type, script_name, *args, **kwargs):
		if not script_type == "gcode" or not script_name == "afterPrinterConnected":
			return None

		ip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
		prefix = None
		postfix = "M117 IP:" + ip
		return prefix, postfix

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			ipOnConnect=dict(
				displayName="ipOnConnect Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="jneilliii",
				repo="OctoPrint-ipOnConnect",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/jneilliii/OctoPrint-ipOnConnect/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "ipOnConnect Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ipOnConnectPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.scripts": message_on_connect
	}

