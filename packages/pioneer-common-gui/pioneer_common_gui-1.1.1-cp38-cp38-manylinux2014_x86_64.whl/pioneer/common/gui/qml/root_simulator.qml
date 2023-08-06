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
    

    property alias lcaPackages: packages_
    property alias denseLcaPackages: denseLcaPackages_
    property alias lcaTransform: lcaTransform_
    property alias lcaSpecs: lca_.specs
    property alias denseLcaSpecs: denseLca_.specs

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
                packages: VariantProduct{id: packages_}
                transform: MatrixTransform{id: lcaTransform_}
            }
            LCAActor
            {
                id: denseLca_
                visible: dense_.checked
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
            RowLayout
            {
                id: controls_
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
            }
            
            FigureWithToolbar
            {
                id: imgFigure_
                Keys.onPressed: component.key = event.text/// support for wait_key()
                Layout.fillWidth: true
                Layout.preferredHeight: imgdWindow_.height - controls_.height
            }
        }
    }
}

