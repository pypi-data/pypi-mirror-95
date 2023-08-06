/*
* Created on Feb 14, 2018
*
* \author: maxime
* \filename: Example1.qml
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
import Misc 1.0 //contains Utils.js
ApplicationWindow
{
    id: component
    property string ip : "192.168.4.0"
    width: 800
    height: 600

    function toClosestPowOf2(current, new_value)
    {
        var f =  new_value > current? Math.ceil : Math.floor
        var exp = f(Math.log2(new_value))
        return Math.pow(2, exp)
    }
    menuBar: MenuBar {
        Menu
        {
            title: "File"
            MenuItem { text: "connect"; onTriggered: popup.open() }
        }
    }
    
    Component.onCompleted: popup.open()
    
    

    onClosing: 
    {
        for (var w in popup.sensorWindows)
            popup.sensorWindows[w].sensorWindow.close()
    } 

    Popup
    {
        id: popup
        anchors.centerIn: parent
        width: 600
        height: 300
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParen

        readonly property var sensorWindows  : Utils.listOfInstances(sensorWindows_)

        Column
        {
            Row
            {
                Label
                {
                    id: type_
                    width: 400
                    text: 'type'
                }
                Label
                {
                    id: address_
                    width: 100
                    text: 'address'
                }
                Label
                {
                    id: connected_
                    width: 100
                    text: 'connected'
                }
                
            }
            Timer
            {
                interval: 1000
                running: false // segfault bug when epeater_.model changes. probably an issue with destroying a SensorWindow
                repeat: true
                
                onTriggered:
                {
                    var devs = LeddarUtils.devices('Ethernet')
                    if (devs.length != sensorWindows_.model.length)
                        sensorWindows_.model = devs
                }
            }
            Repeater
            {
                id: sensorWindows_
                model: LeddarUtils.devices('Ethernet')
                Row
                {
                    objectName: modelData.address
                    Label
                    {
                        width: type_.width
                        text: modelData.name
                    }
                    Label
                    {
                        width: address_.width
                        text: modelData.address
                    }
                    CheckBox
                    {
                        onCheckedChanged:
                        {
                            if(checked)
                            {
                                actors_.addActor(actor_)
                                sensorWindow_.visible = true;
                                sensorWindow_.running = true;
                                sensorWindow_.raise();
                            }
                            else
                            {
                                actors_.removeActor(actor_)
                                sensorWindow_.visible = false;
                                sensorWindow_.running = false;
                            }
                            popup.close();
                        }
                        
                    }
                    property var sensorWindow : SensorWindow
                    {
                        id: sensorWindow_
                        ip: running ? modelData.address : ''
                    }
                    property var actor : LCAActor
                    {
                        id: actor_
                        minAmplitude: 0
                        maxAmplitude: 5000
                        specs: sensorWindow_.live.specs
                        packages: sensorWindow_.live
                        colorMap: 'viridis'
                        clickEcho: function(v,h)
                        {
                            sensorWindow_.toggleCell(v, h)
                        }
                    }
                    
                }
            }
        }
    }


    

    Viewport
    {
        anchors.fill: parent

        actors: Actors
        {
            id: actors_
            GridXZ{}
        }
    }
}

