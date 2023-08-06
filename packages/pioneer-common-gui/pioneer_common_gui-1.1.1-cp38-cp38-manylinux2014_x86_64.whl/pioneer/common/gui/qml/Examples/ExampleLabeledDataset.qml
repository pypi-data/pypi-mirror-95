/*
* Created on Feb 14, 2018
*
* \author: maxime
* \filename: Example1.qml
*/


import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Controls 2.4 as Ctrl24
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
            Ctrl24.ComboBox {
                id: labelTypeCombo
                // width: 200
                // height: 200
                model: [ "class_labels", "instance_labels" ]
            }
        }
        // PZQImagePainter
        QImagePainter
        {
            imageArray: rightCamImage_
            width: 720
            height: 540
            // width: 1440
            // height: 1080

        }
    }

    // this is important for the key processing code below
    focus: true
    Keys.onPressed: {
        if (event.key == Qt.Key_Left) {
            if(slider_.value > 0) {
                slider_.value = slider_.value-1
            }
            console.log("index", slider_.value);
            event.accepted = true;
        }
        if (event.key == Qt.Key_Right) {
            if(slider_.value < slider_.maximumValue) {
                slider_.value = slider_.value+1
            }
            console.log("index", slider_.value);
            event.accepted = true;
        }
    }

    Dataset
    {
        id: ds_
        // syncList:['flir_tfl_img', 'lca3_bfc_ech', 'lca3_bfc_maskrcnn_labels', 'flir_tfl_maskrcnn_labels']
        syncList:['flir_tfl_img', 'lca3_bfc_ech', 'lca3_bfc_predicted_labels', 'flir_tfl_maskrcnn_labels']
        path: component.path
    }

    DatasetSelector
    {
        id: lcaLeft_
        name: "lca3_bfc_ech"
        index : slider_.value
        dataset: ds_
    }


    LCASegmentationLabels
    {
        id: lcaLeftSegLabels_
        packages : DatasetSelector
        {
            id: lcaLeftSegLabelsSelector_
            name: "lca3_bfc_predicted_labels"
            // name: "lca3_bfc_maskrcnn_labels"
            index : slider_.value
            dataset: ds_
        }
        labelType: labelTypeCombo.model[labelTypeCombo.currentIndex]
    }

    SegmentationLabelsImageFilter
    {
        id: rightCamImageFilter_
        packages: DatasetSelector
        {
            id: rightCamImageSelector_
            name: "flir_tfl_img"
            index : slider_.value
            dataset: ds_
        }
        labels: DatasetSelector
        {
            id: rightCamImageFilterSelector_
            name: "flir_tfl_maskrcnn_labels"
            index : slider_.value
            dataset: ds_
        }
    }

    BGRToRGBFilter {
        id: rightCamImage_
        imageArray: rightCamImageFilter_
    }

    actors: Actors
    {
        Actor
        {

            id: echoActor_
            visible: mainVisible_.checked

            transform: Rotation {
                // rotate by 90 degree to align scan axis with horizon
                quaternion: qFromAA(Qt.vector3d(0,0,1), 90*Math.PI/180)
                // reflect wrt to the x-axis (dataset dependent?)
                parentTransform: MatrixTransform {
                    matrix: Qt.matrix4x4( -1, 0, 0, 0
                                         , 0, 1, 0, 0
                                         , 0, 0, 1, 0
                                         , 0, 0, 0, 1)
                }
            }
            geometry: Geometry
            {
                id: geometry_
                primitiveType: Geometry.POINTS
                indices: cloud_.indices
                attribs: SegmentationLabelsAttribs
                {
                    vertices : PointCloud
                    {
                        id: cloud_
                        // v and h are swapped since they correspond to laser
                        // scan axis and apd axis rather than horizontal and
                        // vertical.
                        specs: {{'v': 256, 'h': 64, 'v_fov': 60, 'h_fov': 20}}
                        packages: lcaLeft_
                    }
                    labels: lcaLeftSegLabels_.labels
                }
            }

            onClicked:
            {
                // chart_.toggleCell(cloud_.channel(id))
            }

            effect: Effect
            {
                pointSize: 2
                shader0: SegmentationLabelsProgram{color: "blue"}
            }
        }
    }
}

