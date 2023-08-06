/*
* Created on Feb 14, 2018
*
* \author: maxime
* \filename: Example1.qml
*/


import QtQuick 2.5
import QtQuick.Controls 1.4
import QtCharts 2.0
import Leddar 1.0
import UI3D 1.0
import UI2D 1.0
Viewport
{
    id: component

    property string path: ""
    anchors.fill: parent
    Column
    {

        Slider
        {
            id: slider_
            width: component.width
            value: 0
            maximumValue: lcaLeftSelector_.nIndices-1
            minimumValue: 0
            stepSize: 1
            NumberAnimation on value
            {
                id: animation_;
                running: false;
                loops: NumberAnimation.Infinite;
                from: 0
                to: slider_.maximumValue-1;
                duration: 8000
            }
        }

        Row
        {

            Button
            {
                text: "play"
                onClicked: animation_.running ? animation_.resume() : animation_.start()
            }
            Button
            {
                text: "pause"
                onClicked: animation_.pause()
            }
            Button
            {
                text: "rewind"
                onClicked:
                {
                    slider_.value = 0;
                }
            }
        }
        QImagePainter
        {
            imageArray: ImageArray
            {
                specs: cloud_.specs
                data: lcaLeft_.data
                channels: lcaLeft_.channels
                imageMode: ImageArray.AMPLITUDE
            }
            width: 320
            height: 80
        }
        TracesChart
        {
            id: chart_
            v: cloud_.specs.v
            h: cloud_.specs.h
            basePoints : 64
            normalizeTraces : true
            traces: DatasetSelector
            {
                dataset: ds_
                index: lcaLeftSelector_.index
                name: "lca2_bfl_trr"
            }

            width: 300
            height: 400
        }

    }

    LCAEchoes
    {
        id: lcaLeft_
        packages : DatasetSelector
        {
            id: lcaLeftSelector_
            dataset: Dataset
            {
                id: ds_
                syncList:['lca2_bfl_ech', 'lca2_bfl_trr', 'flir_tfl']
                path: component.path
            }
            name: "lca2_bfl_ech"
            index : slider_.value
        }
    }

    actors: Actors
    {
        Sensor
        {
            specs: cloud_.specs
            transform: echoActor_.transform
        }
        Actor
        {

            id: echoActor_
            visible: mainVisible_.checked
            geometry: Geometry
            {
                id: geometry_
                primitiveType: Geometry.TRIANGLES
                indices: cloud_.indices
                attribs: AmplitudeAttribs
                {
                    vertices : SurfaceCloud
                    {
                        id: cloud_
                        specs: {{'v': 8, 'h': 32, 'v_fov': 20, 'h_fov': 60}}
                        data: lcaLeft_.data
                        channels: lcaLeft_.channels
                    }
                    amplitude: vertices.amplitudes
                }
            }

            onClicked:
            {
                chart_.toggleCell(cloud_.channel(id))
            }

            effect: Effect
            {
                shader0: AmplitudesProgram{color: "blue"}
            }
        }
    }
}

