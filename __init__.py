# Copyright (c) 2023 YiamiYo
# The PowerCostPlugin is released under the terms of the MIT License

from . import PowerCostExtension, PowerCostMachineAction
from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("PowerCostPlugin")


def getMetaData():
	return {}


def register(app):
	return {
		"extension": PowerCostExtension.PowerCostExtension(app),
		"machine_action": PowerCostMachineAction.PowerCostMachineAction(app)
	}