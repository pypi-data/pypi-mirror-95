/*
* Created on May 30, 2019
*
* \author: maxime
* \filename: root_POCFrancois.qml
*/


import QtQuick 2.9
import QtQuick.Window 2.7
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11
import Leddar 1.0
import Examples 1.0
import MultiSensorViewer 1.0
import QtQml.Models 2.1
import UI2D 1.0
import UI3D 1.0


Viewport
{
    /// support for wait_key()
    focus: true
    property string key: ''
    Keys.onPressed: key = event.text
    property alias slider: slider_
    ///

    width:800
    height: 600
    Slider
    {
        id: slider_
        anchors.left: parent.left
        anchors.right: parent.right
    }
    actors: Actors
    {
        id: actors_
        //GridXZ{}
    }
}