/*
* Created on Feb 14, 2018
*
* \author: maxime
* \filename: Example1.qml
*/


import QtQuick 2.9
import QtQuick.Controls 1.4
import QtCharts 2.0

import Leddar 1.0
import UI3D 1.0
import UI2D 1.0

Viewport
{
    id: component
    property string ip : '192.168.0.20'
    anchors.fill: parent

    Column
    {
    	QImagePainter
        {
	        imageArray: ImageArray
	        {
	            specs: edevice_.specs
	            data: edevice_.data
	            channels: edevice_.channels
		        imageMode: ImageArray.AMPLITUDE
	        }
            width: 1280
            height: 640
        }
        SpinBox
        {
            id: vbank_
            value: 0
            maximumValue: 3
            minimumValue: 0
            stepSize: 1
            decimals: 0
        }
        SpinBox
        {
            id: hbank_
            value: 0
            maximumValue: 4
            minimumValue: 0
            stepSize: 1
            decimals: 0
        }
    }
    actors: Actors
    {

        Actor
        {
            //visible: false;
            id: echoActor_
            objectName: 'echoActor_'
            geometry: Geometry
            {
                id: geometry_
                primitiveType: Geometry.TRIANGLES
                indices: could_.indices
                attribs: AmplitudeAttribs
                {
                    vertices : SurfaceCloud
                    {
                        id: could_
                        specs: live_.specs
                        packages: PackageFilter
    				    {
    				        filter : {'amp_min': -1e6, 'amp_max': 1e6, 'dist_min': 0.0, 'dist_max': 150.0}
    				        packages : LiveCapture
    		                {
    		                	id: live_
    		                    ip: component.ip
    		                    running: true
    		                }
    	                }
                        //bankSelection: hbank_.value < hbank_.maximumValue ? [[vbank_.value,hbank_.value]] : []
                    }
                    amplitude: vertices.amplitudes
                }
            }

            effect: Effect
            {
                shader0: AmplitudesProgram{color: "blue"}
            }
        }


        Sensor
        {
            //visible: false
            specs: geometry_.echo.specs
            transform: echoActor_.transform
        }


    }
}

