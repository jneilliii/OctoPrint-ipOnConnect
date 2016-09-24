# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import socket

class ipOnConnectPlugin(octoprint.plugin.StartupPlugin,octoprint.plugin.EventHandlerPlugin):
	def on_after_startup(self):
		self._logger.info("ipOnConnectPlugin: " + [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
	
	##-- Attempt at using comm.protocol.scripts hook --not working
	def message_on_connect(comm, script_type, script_name, *args, **kwargs):
		if not script_type == "gcode" or not script_name == "afterPrinterConnected":
			return None

		prefix = None
		postfix = "M117 " + [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
		return prefix, postfix
		
	##-- EventHandler hook 
	def on_event(self, event, payload):
		if event == "Connected":
			self._printer.command("M117 " + [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])

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
		"octoprint.comm.protocol.scripts": __plugin_implementation__.message_on_connect
	}

