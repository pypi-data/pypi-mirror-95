/*
* Created on Feb 14, 2018
*
* \author: maxime
* \filename: CalibLidarCamera.qml
*/


import QtQuick 2.5
import QtQuick.Controls 1.4
import Leddar 1.0
import UI3D 1.0
Item
{
    id: component

    property int serialNumber : 18260349
    property var patternSpecs : ({nx: 13, ny: 10, size : 0.028, name: serialNumber})
    property var camSpecs : ({h: 1440, v: 1080, pixel_size : 3.45e-6, f: 3.1e-3})

    anchors.fill: parent
    Column
    {
        Text{text: "specs: " + JSON.stringify(calibrator_.patternSpecs); wrapMode: Text.WordWrap}
        Text{width: component.width; text: "progress: " + JSON.stringify(calibrator_.outputs); wrapMode: Text.WordWrap}
        Button
        {
            text: "calibrate"
            onClicked: calibrator_.calibrate()
        }
        Button
        {
            text: "save"
            onClicked: calibrator_.save(path_.text)
        }
        Button
        {
            text: "load"
            onClicked: calibrator_.load(path_.text)
        }
        TextField{id: path_; text: "calibration_" + cam0_.serialNumber + ".tgz"}

        Row
        {
            QImagePainter
            {

                imageArray: ROSCalibratorFilter
                {
                    id: calibrator_;
                    imageArray: PySpinCamera
                    {
                        id: cam0_
                        serialNumber: component.serialNumber
                        assynchronous: true
                    }
                    patternSpecs: component.patternSpecs
                    camSpecs: component.camSpecs
                    name: component.serialNumber.toString()
                }
                width: 640
                height: 480
                opacity: 0.8
            }
            QImagePainter
            {

                imageArray: Undistort
                {
                    imageArray: cam0_
                    path: path_.text
                }
                width: 640
                height: 480
                opacity: 0.8
            }
        }

    }
}

