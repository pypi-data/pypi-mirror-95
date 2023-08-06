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
    property var echoes
    property color color : 'blue'
    property var specs
    property matrix4x4 matrix
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
        	GridXZ
        	{
        		color: actor_.frustrumColor
        	}
            LCAActor
            {
                id: actor_
                specs : component.specs
                packages : VariantProduct{variant: component.echoes}
                transform: MatrixTransform{matrix: component.matrix}
            }
        }
    }

}
