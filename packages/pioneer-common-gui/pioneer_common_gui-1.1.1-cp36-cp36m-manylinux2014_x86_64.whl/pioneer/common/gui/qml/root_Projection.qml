/*
* Created on May 30, 2019
*
* \author: maxime
* \filename: root_Projection.qml
*/


import QtQuick 2.9
import QtQuick.Window 2.7
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11
import Leddar 1.0
import Examples 1.0
import MultiSensorViewer 1.0
import QtQml.Models 2.1
import UI2D 1.0
import UI3D 1.0


Viewport
{
    property alias surfaceCloud: surfaceCloud_
    property alias model: cb_.currentIndex
    /// support for wait_key()
    focus: true
    property string key: ''
    Keys.onPressed: key = event.text
    ///
    function resetCamera()
    {
        var up  = Qt.vector3d(0,-1,0)
        var eye = Qt.vector3d(0,0,-10)
        var tf_Ref_from_Local = Qt.matrix4x4()
        camera.center = tf_Ref_from_Local.times(Qt.vector3d(0,0,0))
        camera.up     = tf_Ref_from_Local.times(up.toVector4d()).toVector3d()
        camera.eye    = tf_Ref_from_Local.times(eye)
    }
    Component.onCompleted: resetCamera()
    width:800
    height: 600
    RowLayout
    {
        Text {text: '<font color="white"> projection model </font>'}
        ComboBox
        {
            id: cb_
            model: ["old", "spherical", "ortho"]
        }
    }

    actors: Actors
    {
        id: actors_
        GridXZ{}
        Actor
        {

            geometry: Geometry
            {
                id: surfaceCloud_
                primitiveType: Geometry.TRIANGLES
                indices: ArrayUInt1{id: indices_}
                attribs: AmplitudeAttribs
                {
                    id: amplitudeAttribs_
                    vertices : ArrayFloat3{id: vertices_}
                    amplitude: ArrayFloat1{id: amplitudes_}
                }
            }
            
            effect: Effect
            {
                shader0: ColorMapProgram{id: cmap_}
            }
        }
    }
}