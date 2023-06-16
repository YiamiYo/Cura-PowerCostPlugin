import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import UM 1.2 as UM
import Cura 1.1 as Cura

Cura.MachineAction {

	UM.I18nCatalog { id: catalog; name: "cura" }

	id: base
	anchors.fill: parent
	
	property int columnWidth: (parent.width - 2.0 * UM.Theme.getSize("default_margin").width - 25) | 0
	property int columnSpacing: UM.Theme.getSize("default_margin").height
	property int labelWidth: (columnWidth * 2.0 / 3.0 - UM.Theme.getSize("default_margin").width - 25) | 0
	property int controlWidth: (columnWidth / 3.0) | 0
	property var labelFont: UM.Theme.getFont("default")

	function save(closeDialog) {
		manager.saveConfig({
			power_cost_per_kwh: powerCostPerKWhField.valueText,
			power_consumption_average: powerConsumptionAverageField.valueText
		})
		if(closeDialog) {
			actionDialog.close()
		}
	}

	function cancel(closeDialog) {
		if(closeDialog) {
			actionDialog.close()
		}
	}

	Connections {
		target: actionDialog
		onAccepted: save(false)
		onRejected: cancel(false)
		onClosing: cancel(false)
	}

	Item {
		id: powerPane

		RowLayout {
			anchors {
				top: parent.top
				left: parent.left
				right: parent.right
				margins: UM.Theme.getSize("default_margin").width
			}
			spacing: UM.Theme.getSize("default_margin").width

			Column {
				Layout.fillWidth: true
				Layout.alignment: Qt.AlignTop

				spacing: UM.Theme.getSize("default_margin").height

				Cura.NumericTextFieldWithUnit {
					id: powerCostPerKWhField

					width: parent.width - 40
					x: 25
					valueText: manager.settingsPowerCostPerKWh
					labelText: catalog.i18nc("@label", "Power Cost")
					unitText: UM.Preferences.getValue("cura/currency") + " / " + catalog.i18nc("@label", "KWh")
					labelFont: base.labelFont
					labelWidth: base.labelWidth
					controlWidth: base.controlWidth
				}

				Cura.NumericTextFieldWithUnit {
					id: powerConsumptionAverageField

					width: parent.width - 40
					x: 25
					valueText: manager.settingsPowerConsumptionAverage
					labelText: catalog.i18nc("@label", "Power Consumption Average")
					unitText: catalog.i18nc("@label", "W")
					labelFont: base.labelFont
					labelWidth: base.labelWidth
					controlWidth: base.controlWidth
				}
			}
		}
	}

	Item {
		id: actionButtons

		anchors{
			bottom: parent.bottom
			left: parent.left
			right: parent.right
			topMargin: UM.Theme.getSize("default_margin").height
			bottomMargin: UM.Theme.getSize("wide_margin").height
		}

		Flow  {
			Layout.fillWidth: true
			layoutDirection: Qt.RightToLeft 
			anchors.fill: parent
			spacing: UM.Theme.getSize("default_margin").width

			Cura.SecondaryButton {
				id: cancelButton
				text: catalog.i18nc("@action:button", "Cancel")
				onClicked: { cancel(true) }
			}

			Cura.PrimaryButton {
				id: saveButton
				text: catalog.i18nc("@action:button", "Save")
				onClicked: { save(true) }
			}
		}
	}
}