/*
* Created on Feb 14, 2018
*
* \author: maxime
* \file : Line.qml
*/

import QtQuick 2.5
import Leddar 1.0
import UI3D 1.0

Actor
{
	id: component
	property real lineWidth : 1
	property color color : "black"
	property var from : [0,0,0]
	property var to : [1,0,0]

	geometry: Geometry
	{
		primitiveType: Geometry.LINES
		attribs: Attribs
		{
			vertices: ArrayFloat3
			{
				input: [from, to]
			}
		}
	}
	effect: Effect
	{
		lineWidth: component.lineWidth
		shader0: EmissiveProgram{ color: component.color }
	}
}