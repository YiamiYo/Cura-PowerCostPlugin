import re
import json
from enum import Enum

from cura.CuraApplication import CuraApplication

from UM.Logger import Logger

POWERCOST_SETTINGS = "powercost/instances"

def _loadConfig():
	application = CuraApplication.getInstance()
	globalContainerStack = application.getGlobalContainerStack()
	if not globalContainerStack:
		return {}, None
	printerId = globalContainerStack.getId()
	preferences = application.getPreferences()
	settingsJson = preferences.getValue(POWERCOST_SETTINGS)
	if settingsJson is None:
		settings = {}
		preferences.addPreference(POWERCOST_SETTINGS, json.dumps(settings))
	else:
		settings = json.loads(settingsJson)
	return settings, printerId

def getConfig() -> dict:
	settings, printerId = _loadConfig()
	
	if printerId in settings:
		return settings[printerId]
	return {}

def saveConfig(config: dict) -> dict:
	settings, printerId = _loadConfig()
	settings[printerId] = config
	preferences = CuraApplication.getInstance().getPreferences()
	preferences.setValue(POWERCOST_SETTINGS, json.dumps(settings))
	return settings