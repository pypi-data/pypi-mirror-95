/*
* Created on Apr 5, 2018
*
* @author: maxime
* \file : SceneLab0.qml
*
*/
import Leddar 1.0
import UI3D 1.0

Actors
{
    id: component
    property bool visible : true
    property alias target : target_
    property alias wall: wall_
    Box
    {
        id: target_

        dimensions : [.25,.217,.01]
        center : [0, .180, wall_.center[2] - .16]
        effect: Effect
        {
            shader0: EmissiveProgram{color: Qt.rgba(.2,.2,.2,.8)}
        }
        visible: component.visible
    }
    Box
    {
        id: stand_
        dimensions : [.175, 1,.01]
        center : [0, .8, 1.853-.205]
        color: Qt.rgba(0,0,1,.8)
        visible: component.visible
    }
    Box
    {
        id: wall_
        dimensions : [4, 3,.01]
        center : [0, 0, 1.853]
        color: Qt.rgba(0,0,1,.8)
        visible: component.visible
    }
    Box
    {
        id: wallLeft_
        dimensions : [.325, wall_.dimensions[1],.01]
        center : [1.163+dimensions[0]/2, 0, 1.853 - .215]
        color: wall_.color
        visible: wall_.visible
    }
    Box
    {
        id: wallRight_
        dimensions: [.01, wall_.dimensions[1],4]
        center: [-1.606, 0, 1.853 - dimensions[2]/2]
        color: wall_.color
        visible: wall_.visible
        renderRank: 10
    }
}