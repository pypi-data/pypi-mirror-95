import QtQuick 2.9
import QtQuick.Window 2.7
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.9
import Leddar 1.0
import Examples 1.0
import MultiSensorViewer 1.0
import QtQml.Models 2.1
import UI2D 1.0
import UI3D 1.0

ApplicationWindow
{
    id: component

    // LeddarVP.set_args() API:
    width: 800
    height: 600
    property var specs : ({v: 128, h:64, v_fov: 30, h_fov: 40})
    property var echoes
    property var traces
    property alias basePoints: chart_.basePoints
    property alias maxCounts: chart_.maxCounts
    property color color : 'blue'
    property matrix4x4 matrix
    // End LeddarVP.set_args() API

    property alias key: viewport_.key
    Viewport
    {
        id: viewport_
        //// this is necessary for LeddarVP.show()'s 'wait key' code:
        focus: true
        property string key: ''
        Keys.onPressed: key = event.text
        /// End LeddarVP.show() API
        Rectangle
        {
            color:"lightgrey"
            width: parent.width
            height: row_.implicitHeight
            Row
            {
                id: row_
                Text{text: "v bank: "}
                SpinBox
                {
                    id: vBank_
                    value: -1
                    from: -1
                    to: component.specs.v-1
                }
                Text{text: "h bank: "}
                SpinBox
                {
                    id: hBank_
                    value: -1
                    from: -1
                    to: 3
                }
            }
        }

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
                bankSelection: [[vBank_.value,hBank_.value]]
                packages : VariantProduct{variant: component.echoes}
                transform: MatrixTransform{matrix: component.matrix}
            }
        }
    }
    Window
    {
        width: 800
        height: 600
        title: "Traces"
        visibility: component.visibility

        TracesChart
        {
            id: chart_
            anchors.fill: parent
            v: component.specs.v
            h: component.specs.h
            normalizeTraces : true
            traces: VariantProduct{ variant:component.traces}
        }
    }
}
