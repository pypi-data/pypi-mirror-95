import QtQuick 2.9
import Leddar 1.0
import MultiSensorViewer 1.0
import UI3D 1.0

Item
{
    id: component

    // LeddarVP.set_args() API:
    width: 800
    height: 600
    property var vertices // Nx3 float32 numpy array
    property var amplitudes // N float32 numpy array
    property color color : 'blue'
    property matrix4x4 matrix
    property int pointSize: 5
    // End LeddarVP.set_args() API


    //// this is necessary for LeddarVP.show()'s 'wait key' code:
    focus: true
    property string key: ''
    Keys.onPressed: key = event.text
    /// End LeddarVP.show() API

    Viewport
    {
        anchors.fill: parent
        actors: Actors
        {
            Actor
            {

                id: echoActor_
                visible: component.visible
                geometry: Geometry
                {
                    id: geometry_
                    primitiveType: Geometry.POINTS
                    attribs: AmplitudeAttribs
                    {
                        vertices : ArrayFloat3
                        {
                            input: component.vertices
                        }
                        amplitude: ArrayFloat1
                        {
                            input: component.amplitudes
                        }
                    }
                }
                effect: Effect
                {
                    pointSize: component.pointSize
                    shader0: AmplitudesProgram{color: component.color}
                }
            }
        }
    }

}
