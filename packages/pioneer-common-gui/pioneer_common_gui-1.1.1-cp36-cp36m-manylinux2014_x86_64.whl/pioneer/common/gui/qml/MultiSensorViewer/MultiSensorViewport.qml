/*
* Created on Dec 12, 2018
*
* \author: maxime
*/


import QtQuick 2.5
import QtQuick.Controls 1.4
import Leddar 1.0
import UI3D 1.0
import UI2D 1.0
Viewport
{
    id: component

    property color frustrumColor: "blue"
    property bool metaFrustrumVisible: false
    property var model : []
    anchors.fill: parent

    actors: Actors
    {
    	GridXZ
    	{
    		color: component.frustrumColor
    	}
    	Actors
	    {
	        instanciator: Instantiator
	        {
	            id: instantiator_
	            model: component.model.length
	            delegate: Actors
	            {
					id: instance_
					readonly property var model: component.model[index]
				    Sensor
				    {
				    	id: metaFrustrum_
				        visible: component.visible && component.metaFrustrumVisible
				        specs: ({'v': 64, 'h': 128, 'v_fov': instance_.model.specs.h_fov, 'h_fov': 80})
				        transform: Translation
		                {
		                    translate: instance_.model.translate
		                }
				        color: component.frustrumColor
				        depth: model.frustrumDepth
				    }
					LCAActor
		            {
		                colorMap: 'jet' //model.colorMap
		                frustrumColor: component.frustrumColor
		                visible: model.visible
		                minAmplitude: model.ampMin3d
		                maxAmplitude: model.ampMax3d
		                frustrumDepth: model.frustrumDepth
		                specs: instance_.model.specs
		                packages: instance_.model.packages
		                transform: Translation
		                {
		                    translate: instance_.model.translate
		                    parentTransform: Rotation
		                    {
		                        quaternion: qFromEuler(instance_.model.euler[0], instance_.model.euler[1], instance_.model.euler[2])
		                    }
		                }
		            }
	            }
	        }
	    }
    }
}

