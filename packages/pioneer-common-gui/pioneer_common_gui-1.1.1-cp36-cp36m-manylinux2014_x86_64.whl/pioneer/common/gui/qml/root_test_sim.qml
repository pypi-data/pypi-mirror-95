/*
* Created on Feb 14, 2018
*
* \author: maxime
* \filename: Example1.qml
*/

import MPLBackend 1.0
import QtQuick 2.9
import QtQuick.Controls 2.5
import QtQuick.Controls 1.5 as Controls1
import QtQuick.Window 2.7
import QtQuick.Layouts 1.9
import Leddar 1.0
import UI3D 1.0
import Misc 1.0

ApplicationWindow
{
    id: component
    /// support for wait_key()
    property string key: ''
    
    property alias density: density_.value
    property alias vfov: vfov_.value
    property alias hfov: hfov_.value
    property alias v: v_.value
    property alias h: h_.value

    property alias sweepMin: sweepMin_.value
    property alias sweepMax: sweepMax_.value
    property alias sweepStep: sweepStep_.value

    property alias lcaPackages: packages_
    property alias denseLcaPackages: denseLcaPackages_
    property alias lcaTransform: lcaTransform_
    property alias wfContributions: wfContributions_.checked
    
    signal clearClicked()
    signal saveClicked()
    signal sweepAnglesClicked()
    signal sweepDistancesClicked()
    signal sweepPulseWidthClicked()
    signal sweepTilingClicked()
    signal sweepNoiseClicked()

    readonly property var settings: ({
        pulseWidth: pulseWidth_.value
        , angleY: angleY_.value
        , angleX: angleX_.value
        , oversampling: oversampling_.value
        , dx: dx_.value
        , dy: dy_.value
        , wallDistance: wallDistance_.value
        , specs: lca_.specs
        , density: component.density
        , texture: texture_.currentText
        , tile: tile_.value
        , noise: noise_.value
        , radius: radius_.value})
    
    readonly property alias viewport: viewport_

    readonly property alias imgWindow: imgdWindow_
    readonly property alias imgFigure: imgFigure_    

    readonly property alias lca: lca_
    readonly property alias lcaCloud: lca_.cloud
    ///
    height: 900
    width: 900

  
    Viewport
    {
        id: viewport_
        
        focus: true
        Keys.onPressed: component.key = event.text/// support for wait_key()
        anchors.fill: parent
        actors: Actors
        {
            LCAActor
            {
                id: lca_
                visible: sparse_.checked
                specs: ({v:component.v, h:component.h, v_fov:component.vfov, h_fov:component.hfov})
                packages: VariantProduct{id: packages_}
                transform: MatrixTransform{id: lcaTransform_}
            }
            LCAActor
            {
                id: denseLca_
                visible: dense_.checked
                specs: ({v:component.v*component.density, h:component.h*component.density, v_fov:component.vfov, h_fov:component.hfov})
                packages: VariantProduct{id: denseLcaPackages_}
                transform: lcaTransform_
            }
        }
    }

    Window
    {
        id: imgdWindow_
        x:800
        width: 1200
        height: 900
        visible: false
        ColumnLayout
        {
            anchors.fill: parent
            GridLayout
            {
                id: controls_
                // flow: GridLayout.TopToBottom
                columns: 2
                RowLayout
                {
                    Text{text: "pulse width (ns): "; Layout.preferredWidth: 200} 
                    SpinBox
                    {
                        id: pulseWidth_
                        value: 16
                        from:1
                        to:100
                        stepSize:1
                        editable: true
                    }
                }
                RowLayout
                {
                    Text{text: "oversampling: "; Layout.preferredWidth: 200} 
                    SpinBox
                    {
                        id: oversampling_
                        value: 8
                        from:1
                        to:16
                        stepSize:1
                        editable: true
                    }
                }

                RowLayout
                {
                    Text{text: "wall y angle: "; Layout.preferredWidth: 200} 
                    SpinBox
                    {
                        id: angleY_
                        value: 0
                        from:0
                        to:90
                        stepSize:5
                        editable: true
                    }
                }
                RowLayout
                {
                    Text{text: "wall x angle: "; Layout.preferredWidth: 200} 
                    SpinBox
                    {
                        id: angleX_
                        value: 0
                        from:0
                        to:90
                        stepSize:5
                        editable: true
                    }
                }
                RowLayout
                {
                    Text{text: "wall y: "; Layout.preferredWidth: 200} 
                    SpinBox
                    {
                        id: dy_
                        value: 0
                        from:-10
                        to:10
                        stepSize:1
                        editable: true
                    }
                }
                RowLayout
                {
                    Text{text: "wall x: "; Layout.preferredWidth: 200} 
                    SpinBox
                    {
                        id: dx_
                        value: 0
                        from:-10
                        to:10
                        stepSize:1
                        editable: true
                    }
                }
                RowLayout
                {
                    Text{text: "wall distance: "; Layout.preferredWidth: 200} 
                    SpinBox
                    {
                        id: wallDistance_
                        value: 25
                        from:5
                        to:100
                        stepSize:5
                        editable: true
                    }
                }
                RowLayout
                {
                    Text{text: "density: "; Layout.preferredWidth: 200} 
                    SpinBox
                    {
                        id: density_
                        value: 18
                        from:1
                        to:100
                        stepSize:1
                        editable: true
                    }
                }

                RowLayout
                {
                    Text{text: "vfov: "; Layout.preferredWidth: 200} 
                    SpinBox
                    {
                        id: vfov_
                        value: 18
                        from:1
                        to:100
                        stepSize:1
                        editable: true
                    }
                }
                RowLayout
                {
                    Text{text: "hfov: "; Layout.preferredWidth: 200} 
                    SpinBox
                    {
                        id: hfov_
                        value: 18
                        from:1
                        to:100
                        stepSize:1
                        editable: true
                    }
                }

                RowLayout
                {
                    Text{text: "v: "; Layout.preferredWidth: 200} 
                    SpinBox
                    {
                        id: v_
                        value: 9
                        from:1
                        to:100
                        stepSize:1
                        editable: true
                    }
                }
                RowLayout
                {
                    Text{text: "h: "; Layout.preferredWidth: 200} 
                    SpinBox
                    {
                        id: h_
                        value: 9
                        from:1
                        to:100
                        stepSize:1
                        editable: true
                    }
                }
                
                RowLayout
                {
                    Text{text: "texture: "; Layout.preferredWidth: 200} 
                    ComboBox
                    {
                        id: texture_
                        editable: true
                        currentIndex : 5 
                        model: [""
                            , "banded_0002.jpg"
                            , "banded_0090.jpg"
                            , "bumpy_0143.jpg"
                            , "smeared_0022.jpg"
                            , "chequered_0109.jpg"]
                    }
                    SpinBox
                    {
                        id: tile_
                        value: 1
                        from:1
                        to:100
                        stepSize:1
                        editable: true
                    }
                }
                RowLayout
                {
                    Text{text: "noise: "; Layout.preferredWidth: 200} 
                    SpinBox
                    {
                        id: noise_
                        value:0
                        from:0
                        to:100
                        stepSize:1
                        editable: true
                    }
                }
                RowLayout
                {
                    Text{text: "radius (mm): "; Layout.preferredWidth: 200} 
                    SpinBox
                    {
                        id: radius_
                        value:0
                        from:0
                        to:10000
                        stepSize:50
                        editable: true
                    }
                }
            }
            GridLayout
            {
                columns: 8
                id: tools_

                Button
                {
                    id: sweepAngles_
                    text: "sweep angles"
                    onClicked: component.sweepAnglesClicked()
                }
                Button
                {
                    id: sweepDistances_
                    text: "sweep distances"
                    onClicked: component.sweepDistancesClicked()
                }
                Button
                {
                    id: sweepPulseWidth_
                    text: "sweep pulse width"
                    onClicked: component.sweepPulseWidthClicked()
                }
                Button
                {
                    id: sweepTiling_
                    text: "sweep tiling"
                    onClicked: component.sweepTilingClicked()
                }
                Button
                {
                    id: sweepNoise_
                    text: "sweep noise"
                    onClicked: component.sweepNoiseClicked()
                }
                SpinBox
                {
                    id: sweepMin_
                    value:0
                    from:0
                    to:100
                    stepSize:1
                    editable: true
                }
                SpinBox
                {
                    id: sweepMax_
                    value: 50
                    from:1
                    to:100
                    stepSize:1
                    editable: true
                }
                SpinBox
                {
                    id: sweepStep_
                    value: 5
                    from:1
                    to:10
                    stepSize:1
                    editable: true
                }
                Button
                {
                    id: clear_
                    text: "clear plots"
                    onClicked: component.clearClicked()
                }
                Button
                {
                    id: save_
                    text: "save to file"
                    onClicked: component.saveClicked()
                }
                CheckBox
                {
                    id: sparse_
                    text: "sparse"
                    checked: false
                }
                CheckBox
                {
                    id: dense_
                    text: "dense"
                    checked: true
                }
                CheckBox
                {
                    id: wfContributions_
                    text: "wf contrib plot"
                    checked: false
                }
            }
            FigureWithToolbar
            {
                Keys.onPressed: component.key = event.text/// support for wait_key()
                id: imgFigure_
                Layout.fillWidth: true
                Layout.preferredHeight: imgdWindow_.height - controls_.height - tools_.height
            }
        }
    }
}

