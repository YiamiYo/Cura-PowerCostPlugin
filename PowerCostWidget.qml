import QtQuick 2.7
import QtQuick.Controls 2.1
import UM 1.2 as UM
import Cura 1.0 as Cura

Rectangle {
	id: powerCostWidget
	color: UM.Theme.getColor("main_background")
	border.color: UM.Theme.getColor("lining")
	border.width: UM.Theme.getSize("default_lining").width
	radius: UM.Theme.getSize("default_radius").width
	width: childrenRect.width + UM.Theme.getSize("default_margin").width
	height: childrenRect.height + UM.Theme.getSize("default_margin").height
	anchors.bottom: parent ? parent.bottom : undefined
	anchors.bottomMargin: -UM.Theme.getSize("thick_margin").width
	visible: UM.Backend.state == UM.Backend.Done || UM.Backend.state == UM.Backend.Disabled

	Cura.IconWithText {
		id: printPowerCost
		anchors.verticalCenter: parent.verticalCenter
		anchors.horizontalCenter: parent.horizontalCenter
		font: UM.Theme.getFont("default")
		source: Qt.resolvedUrl("Lightning.svg")
		text: "%1 %2".arg(UM.Preferences.getValue("cura/currency")).arg(manager.printPowerCost.toFixed(2))
	}
}