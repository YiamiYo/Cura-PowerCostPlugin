import os
import json
from typing import Dict, Type, TYPE_CHECKING, List, Optional, cast

try:
	from cura.ApplicationMetadata import CuraSDKVersion
except ImportError: # Cura <= 3.6   
	CuraSDKVersion = "6.0.0"
if CuraSDKVersion >= "8.0.0":
	from PyQt6.QtCore import QObject, QVariant, pyqtSlot, pyqtProperty, pyqtSignal
else:
	from PyQt5.QtCore import QObject, QVariant, pyqtSlot, pyqtProperty, pyqtSignal

from cura.CuraApplication import CuraApplication
from cura.MachineAction import MachineAction

from UM.Logger import Logger
from UM.Settings.ContainerRegistry import ContainerRegistry
from UM.Settings.DefinitionContainer import DefinitionContainer
from UM.i18n import i18nCatalog

catalog = i18nCatalog("cura")

from .PowerCostSettings import getConfig, saveConfig

class PowerCostMachineAction(MachineAction):
	def __init__(self, app: CuraApplication) -> None:
		super().__init__("PowerCostMachineAction", catalog.i18nc("@action", "Power Cost Settings"))
		self._qml_url = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'PowerCostMachineSettings.qml')
		self._app = app
		self._app.globalContainerStackChanged.connect(self._onGlobalContainerStackChanged)
		self._app.getContainerRegistry().containerAdded.connect(self._onContainerAdded)

	def _onGlobalContainerStackChanged(self) -> None:
		self.settingsPowerCostPerKWhChanged.emit()  # todo: move to global settings?
		self.settingsPowerConsumptionAverageChanged.emit()
 
	def _onContainerAdded(self, container) -> None:
		# Add this action as a supported action to all machine definitions
		if isinstance(container, DefinitionContainer) and container.getMetaDataEntry("type") == "machine":
			self._app.getMachineActionManager().addSupportedAction(container.getId(), self.getKey())

	settingsPowerCostPerKWhChanged = pyqtSignal()
	settingsPowerConsumptionAverageChanged = pyqtSignal()

	@pyqtProperty(str, notify = settingsPowerCostPerKWhChanged)
	def settingsPowerCostPerKWh(self) -> Optional[str]:
		config = getConfig()
		return config.get("power_cost_per_kwh", "0.0") if config else "0.0"

	@pyqtProperty(str, notify = settingsPowerConsumptionAverageChanged)
	def settingsPowerConsumptionAverage(self) -> Optional[str]:
		config = getConfig()
		return config.get("power_consumption_average", "0.0") if config else "0.0"

	@pyqtSlot(QVariant)
	def saveConfig(self, paramsQJSValObj):
		oldConfig = getConfig()
		config = paramsQJSValObj.toVariant()
		saveConfig(config)
		self._app.globalContainerStackChanged.emit()

	@pyqtSlot()
	def deleteConfig(self):
		if deleteConfig():
			self._app.globalContainerStackChanged.emit()
