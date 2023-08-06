/*
* Created on Feb 14, 2018
*
* \author: maxime
* \filename: Example1.qml
*/

import MPLBackend 1.0
import QtQuick 2.9
import QtQuick.Controls 2.5
import QtQuick.Window 2.7
import QtQuick.Layouts 1.9
import Leddar 1.0
import UI3D 1.0
import UI2D 1.0
import Misc 1.0

ApplicationWindow
{
    id: component
    /// support for wait_key()
    property string key: ''
    
    /// Python API
    property int nActors: 0
    property alias selectedActor: actor_.value
    property alias fileName: fileName_.text
    property alias type: type_.currentText
    readonly property alias pose    : pose_
    readonly property alias viewport: viewport_

    signal saveClicked(int index)
    ///
    width: 800
    height: 600

    ColumnLayout
    {
        anchors.fill: parent
        Viewport
        {
            id: viewport_
            Layout.fillWidth: true
            Layout.fillHeight: true
            focus: true
            Keys.onPressed: component.key = event.text // support for wait_key()
            actors: Actors
            {
            }
        }
        ColumnLayout
        {
            id: controls_
            Layout.preferredHeight: controls_.implicitHeight
            RowLayout
            {
                Layout.fillWidth: true
                ComboBox 
                {
                    id: type_
                    model: [ "car", "pedestrian" ]
                }
                Label
                {
                    text: "current: "
                }
                SpinBox
                {
                    id: actor_
                    value: 0; from: 0; to: component.nActors-1

                    Keys.onPressed: component.key = event.text // support for wait_key()
                }
                Label
                {
                    Layout.preferredWidth: implicitWidth
                    id: fileName_
                    // text: input alias
                }
                Button
                {
                    text: "save"
                    onClicked: component.saveClicked(actor_.value)
                }
            }
            PoseEditor
            {
                id: pose_
                Layout.fillWidth: true
                onKeyChanged: component.key = pose_.key // support for wait_key()
                rxVisible: false
                ryVisible: false
                scaleVisible: true
            }
        }

    }


}

