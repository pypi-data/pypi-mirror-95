/*
* Created on Apr 2, 2018
*
* @author: maxime
* \file : Box.qml
*
*/

import QtQuick 2.5
import Leddar 1.0
import UI3D 1.0

Actor
{
    id: component


    property int lineWidth: 1

    property color color: Qt.rgba(.3,.3,.3,1)

    property real span : 250
    property real div : 5
    property bool isXY: false


    geometry: Geometry
    {
        primitiveType: Geometry.LINES;

        indices: ArrayUInt1
        {
            input:
            {
    			var l = [];
    			var n = component.span*2/component.div;

				for(var i = 0; i < n*n; i += n)
					l.push(i, i+n-1);

				for(var i = 0; i < n; i += 1)
					l.push(i, (n-1)*n+i);

				return l;
            }

        }
        attribs: Attribs
        {
            vertices : ArrayFloat3
            {
                input:
                {
            		var l = [];
            		for(var x = -component.span; x < component.span; x += component.div)
            			for(var y = -component.span; y < component.span; y += component.div)
            				l.push(isXY ? [x, y, 0] : [x, 0, y]);
            		return l;
            	}
            }
        }
    }

    effect: Effect
    {
		lineWidth: component.lineWidth
		shader0: EmissiveProgram{ color: component.color }
    }
}