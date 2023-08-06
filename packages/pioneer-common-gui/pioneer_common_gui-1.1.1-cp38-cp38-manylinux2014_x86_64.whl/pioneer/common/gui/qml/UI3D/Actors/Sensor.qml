/*
* Created on Feb 28, 2018
*
* @author: maxime
* \file : Sensor.qml
*
*/

import QtQuick 2.5
import Leddar 1.0
import UI3D 1.0

Actor
{
	id: component
	property alias specs : referential_.specs
	property alias color: program_.color
	property alias depth: referential_.depth

	geometry: Geometry
	{
		primitiveType: Geometry.LINES;

		indices: referential_.indices
		attribs: Attribs
		{
			vertices : SensorReferential
			{
				id: referential_
			}
		}
	}

    effect: Effect
    {
	    shader0: EmissiveProgram{id: program_}
	}
}