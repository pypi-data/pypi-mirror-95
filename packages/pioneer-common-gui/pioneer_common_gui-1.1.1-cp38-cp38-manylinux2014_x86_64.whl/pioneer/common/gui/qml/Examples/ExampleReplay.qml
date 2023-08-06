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
    anchors.fill: parent
    Column
    {

        Slider
        {
            id: slider_
            width: component.width
            value: ereplay_.t
            maximumValue: ereplay_.nFrames-1
            minimumValue: 0
            stepSize: 1
        }

        Row
        {
            Column
            {
                SpinBox
                {
                    id: spinbox_
                    value: ereplay_.t
                    maximumValue: ereplay_.nFrames-1
                    minimumValue: 0
                    stepSize: 1
                    Binding {
                        target: ereplay_
                        property: 't'
                        value: slider_.value
                    }
                    Binding {
                        target: ereplay_
                        property: 't'
                        value: spinbox_.value
                    }
                }

            }
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
                onClicked: {ereplay_.t = 0; animation_.restart()}
            }
            CheckBox
            {
                id: mainVisible_
                text: "show 'in motion'"
                checked : true
            }
            CheckBox
            {
                id: refVisible_
                text: "show 'reference'"
                checked : false
            }
            Column
            {
                SpinBox
                {
                    id: bank_
                    value: 4
                    maximumValue: 4
                    minimumValue: 0
                    stepSize: 1
                    decimals: 0
                }
                SpinBox
                {
                    id: delay_
                    value: 40
                    maximumValue: 4000
                    minimumValue: -4000
                    stepSize: 20
                    decimals: 0
                }
                Text
                {
                    text: "yaw: " + ereplay_.yaw * 180/Math.PI
                }
            }
        }
        QImagePainter
        {
            imageArray: ImageArray
            {
                specs: ereplay_.specs
                data: ereplay_.data
                channels: ereplay_.channels
                imageMode: ImageArray.AMPLITUDE
            }
            width: 320
            height: 80
        }
        TracesChart
        {
            id: chart_
            v: 8//ereplay_.specs.v
            h: 32//ereplay_.specs.h
            basePoints : 64
            normalizeTraces : true
            traces: ereplay_.traces

            width: 200
            height: 400
        }

    }

    ReplayCapture
    {
        id: ereplay_
        datasetFilePath: "/home/maxime/nas/exportedDataset/20181122_180049_RecFile_dataCalib_LCA2Flir_left_stationnement_interieur_exported/LCA2left_perception_ds.pkl"
        t: 0
        NumberAnimation on t
        {
            id: animation_;
            running: false;
            loops: NumberAnimation.Infinite;
            from: 0
            to: ereplay_.nFrames-1;
            duration: 8000
        }
    }

    actors: Actors
    {
        Sensor
        {
            specs: geometry_.echo.specs
            transform: echoActor_.transform
        }
        Actor
        {

            id: echoActor_
            visible: mainVisible_.checked
            transform: Rotation
            {
                quaternion: qFromAA(Qt.vector3d(0,1,0), ereplay_.yaw)
            }
            geometry: Geometry
            {
                id: geometry_
                property var echo : ereplay_
                primitiveType: Geometry.TRIANGLES
                indices: could_.indices
                attribs: AmplitudeAttribs
                {
                    vertices : SurfaceCloud
                    {
                        id: could_
                        specs: ereplay_.specs
                        data: ereplay_.data
                        channels: ereplay_.channels
                    }
                    amplitude: vertices.amplitudes
                }
            }

            onClicked:
            {
                chart_.toggleCell(could_.channel(id))
            }

            effect: Effect
            {
                shader0: AmplitudesProgram{color: "blue"}
            }
        }
    }
}

