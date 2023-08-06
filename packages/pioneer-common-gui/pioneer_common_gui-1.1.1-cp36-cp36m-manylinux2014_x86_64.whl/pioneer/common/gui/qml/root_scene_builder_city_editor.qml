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
    property alias selectedCity: actor_.value
    readonly property alias viewport: viewport_
    property alias info: info_.text
    property int nCities: 2

    signal saveClicked()
    signal loadClicked()
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
                Label
                {
                    text: "current: "
                }
                SpinBox
                {
                    id: actor_
                    value: 0; from: 0; to: component.nCities-1

                    Keys.onPressed: component.key = event.text // support for wait_key()
                }
                Button
                {
                    text: "save"
                    onClicked: component.saveClicked()
                }
                Button
                {
                    text: "load"
                    onClicked: component.loadClicked()
                }
                Text 
                {
                    id: info_
                }
            }
        }

    }


}

