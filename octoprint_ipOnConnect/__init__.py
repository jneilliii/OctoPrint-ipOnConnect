# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import socket
import threading

class ipOnConnectPlugin(octoprint.plugin.SettingsPlugin,
						octoprint.plugin.StartupPlugin,
						octoprint.plugin.EventHandlerPlugin,
						octoprint.plugin.TemplatePlugin):
						
	##~~ SettingsPlugin mixin
	
	def get_settings_defaults(self):
		return dict(delay=0,addTrailingChar=False,useM70=0,displayTime="10")
						
	##~~ StartupPlugin mixin
	
	def on_after_startup(self):	
		t = threading.Timer(int(self._settings.get(["delay"])),self.get_ip_and_send)
		t.start()
		
	##-- EventHandler mixin 
	
	def on_event(self, event, payload):
		if event == "Connected" or event == "ConnectivityChanged":
			t = threading.Timer(int(self._settings.get(["delay"])),self.get_ip_and_send)
			t.start()
			
	##~~ TemplatePlugin mixin

	def get_template_configs(self):
		return [dict(type='settings', custom_bindings=False, template='ipOnConnect_settings.jinja2')]

	##~~ Utility functions
	
	def get_ip_and_send(self):
		server_ip = [(s.connect((self._settings.global_get(["server","onlineCheck","host"]), self._settings.global_get(["server","onlineCheck","port"]))), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
		self._logger.info("ipOnConnectPlugin: " + server_ip)
		if self._settings.get(["addTrailingChar"]):
			server_ip += "_"
		if self._settings.get(["useM70"]):
			message = "M70 P" + self._settings.get(["displayTime"]) + " (" + server_ip + ")"
		else:
			message = "M117 " + server_ip
		self._printer.commands(message)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			ipOnConnect=dict(
				displayName="ipOnConnect",
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

__plugin_name__ = "ipOnConnect"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = ipOnConnectPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

