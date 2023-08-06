/*
* Created on Feb 14, 2018
*
* \author: maxime
* \filename: Points.qml
*/


import QtQuick 2.5
import QtQuick.Controls 1.4
import Leddar 1.0
import UI3D 1.0

Actor
{
	id: component

	property alias points : attribs_.vertices
	property alias color : program_.color
	property alias pointSize: effect_.pointSize

	geometry: Geometry
	{
		primitiveType: Geometry.POINTS
		attribs: Attribs
		{
			id: attribs_
		}
	}
	effect: Effect
	{
		id: effect_

		shader0: EmissiveProgram
		{
			id: program_
		}
	}
}