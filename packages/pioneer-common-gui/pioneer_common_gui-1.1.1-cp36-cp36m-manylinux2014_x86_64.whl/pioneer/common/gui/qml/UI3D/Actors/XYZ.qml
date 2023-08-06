/*
* Created on Feb 14, 2018
*
* @author: maxime
* \file : XYZ.qml
*
*/

import QtQuick 2.5
import Leddar 1.0
import UI3D 1.0
Actors
{
  id: component
  property bool visible : true
  property alias transform: x_.transform
  property real scale: 1
  Line
  {
    id: x_
    visible: component.visible
    from: [0,0,0]
    to: [scale,0,0]
    color: "red"
    // transform: input alias
  }
  Line
  {
    id: y_
    visible: component.visible
    from: [0,0,0]
    to: [0,scale,0]
    color: "green"
    transform: component.transform
  }
  Line
  {
    id: z_
    visible: component.visible
    from: [0,0,0]
    to: [0,0,scale]
    color: "blue"
    transform: component.transform
  }
}
