from UM.Extension import Extension
from UM.Scene.Selection import Selection
from UM.Math.Vector import Vector

from cura.CuraApplication import CuraApplication

from typing import Dict, Type, TYPE_CHECKING, List, Optional, cast

import os.path

try:
	from cura.ApplicationMetadata import CuraSDKVersion
except ImportError: # Cura <= 3.6   
	CuraSDKVersion = "6.0.0"
if CuraSDKVersion >= "8.0.0":
	from PyQt6.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot, pyqtProperty #To find the QML for the dialogue window.
	from PyQt6.QtQml import QQmlComponent, QQmlContext #To create the dialogue window.
else:
	from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot, pyqtProperty #To find the QML for the dialogue window.
	from PyQt5.QtQml import QQmlComponent, QQmlContext #To create the dialogue window.

from UM.Application import Application #To listen to the event of creating the main window, and get the QML engine.
from UM.Logger import Logger #Adding messages to the log.
from UM.PluginRegistry import PluginRegistry #Getting the location of Hello.qml.

from .PowerCostSettings import getConfig

from UM.i18n import i18nCatalog
catalog = i18nCatalog("cura")

class PowerCostExtension(QObject, Extension):
	def __init__(self, app: CuraApplication) -> None:
		super().__init__()		
		self._app = app
		self._printPowerCost = 0.0
		self._app.mainWindowChanged.connect(self.connectEvents)
	
	printPowerCostChanged = pyqtSignal()
	
	@pyqtProperty(float, notify = printPowerCostChanged)
	def printPowerCost(self) -> float:
		return self._printPowerCost

	def connectEvents(self) -> None:
		qml_file_path = os.path.join(PluginRegistry.getInstance().getPluginPath(self.getPluginId()), "PowerCostWidget.qml")
		self._component = self._app.createQmlComponent(qml_file_path, { "manager": self })
		Logger.log("i", qml_file_path)
		Logger.log("i", self._component)
		self._app.addAdditionalComponent("saveButton", self._component)
		self._app.getPrintInformation().currentPrintTimeChanged.connect(self.currentPrintTimeChanged)

	def currentPrintTimeChanged(self):
		currentPrintTime = self._app.getPrintInformation().currentPrintTime
		self._printPowerCost = 0.0
		if currentPrintTime.valid and not currentPrintTime.isTotalDurationZero:
			config = getConfig()
			if config:
				try:
					powerConsumptionInWatts = float(config.get("power_consumption_average", "0.0").strip().replace(',', '.'))
					powerCostPerKWh = float(config.get("power_cost_per_kwh", "0.0").strip().replace(',', '.'))
				except ValueError:
					powerConsumptionInWatts = 0.0
					powerCostPerKWh = 0.0
				if powerConsumptionInWatts > 0.0 and powerCostPerKWh > 0.0:
					powerCostPerHour = powerConsumptionInWatts / 1000.0 * powerCostPerKWh
					printTimeInHours = int(self._app.getPrintInformation().currentPrintTime) / 3600.0
					self._printPowerCost = printTimeInHours * powerCostPerHour
		self.printPowerCostChanged.emit()