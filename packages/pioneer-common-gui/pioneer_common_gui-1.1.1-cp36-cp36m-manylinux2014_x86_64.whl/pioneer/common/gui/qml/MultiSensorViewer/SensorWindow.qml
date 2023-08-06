/*
* Created on Mar 25, 2019
*
* \author: maxime
* \filename: SensorWindow.qml
*/

import MPLBackend 1.0
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


ApplicationWindow
{
    id: component
    title: "LeddarTech configuration for " + component.ip
    width: 800
    height: 600
    

    property alias live: live_
    property alias ip : live_.ip
    property alias running: live_.running

    menuBar: MenuBar {
        Menu
        {
            title: "View"
            MenuItem {id: amplitudesMenu_; text: "2d images"; onTriggered: {amplitude_.visible = true; amplitude_.raise()} }
            MenuItem {id: tracesMenu_; text: "Traces"; onTriggered: {traces_.visible = true; traces_.raise()} } 
        }
    }

    onClosing: 
    {
        amplitude_.close()
        traces_.close()
    } 

    function toggleCell(v, h)
    {
        chart_.toggleCell(v, h);
        tracesMenu_.triggered()
    }
    LiveSensorConfigPanel
    {
        id: panel_
        anchors.fill: parent
        live: LiveCapture
        {
            id: live_
            //ip: input alias
            //running: input alias
            //tracesMode: LiveCapture.RAW
            //tracesROI: [0, 11008]
        }
    }
    Window
    {
        id: amplitude_
        title: "LeddarTech Image Viewer"
        width: 800; height: 600
        Echoes2dViewer
        {
            anchors.fill: parent
            provider.packages: live_
            provider.onClicked: component.toggleCell(v, h)
        }
    }
    Window
    {
        id: traces_
        width: 800
        height: 600
        title: "Traces"

        TracesChart
        {
            id: chart_
            anchors.fill: parent
            v: live_.specs ? live_.specs['v'] : 0
            h: live_.specs ? live_.specs['h'] : 0

            basePoints : 512 //highest possible value
            normalizeTraces : true
            traces: live_.traces
        }
    }
}