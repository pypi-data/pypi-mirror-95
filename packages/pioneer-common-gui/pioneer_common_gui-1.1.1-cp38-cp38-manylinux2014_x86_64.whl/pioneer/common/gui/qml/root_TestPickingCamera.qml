/*
* Created on Jun 2, 2019
*
* \author: maxime
* \filename: root_TestPickingCamera.qml
*/


import QtQuick 2.9
import Leddar 1.0


Viewport
{
    /// support for wait_key()
    focus: true
    property string key: ''
    Keys.onPressed: key = event.text
    ///
    width: 800
    height: 800

    actors: Actors
    {
        id: actors_
        //GridXZ{}
    }
}