/*
* Created on July 16, 2019
*
* \author: maxime
* \filename: Echoes2dViewer.qml
*/

import MPLBackend 1.0
import QtQuick 2.9
import QtQuick.Window 2.7
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11
import Leddar 1.0






ColumnLayout
{
    id: component

    property alias provider: provider_

    RowLayout
    {
        ComboBox
        {
            id: options_
            Layout.fillWidth: true
            model: ["amplitudes:max_amplitudes", "distances:max_amplitudes"]
        }
        ComboBox
        {
            id: colormap_
            model: ["viridis", "plasma", "cool", "copper"]
        }
        CheckBox
        {
            id : logScale_
            text: "log scale"
        }

        CheckBox
        {
            id : flip_
            text: "flip up/down"
            // checked: true
        }
        CheckBox
        {
            id : rotated_
            text: "rotated"
            // checked: true
        }
    }

    RowLayout
    {
        Label{text: range_.first.value.toFixed(2); width: 50}
        RangeSlider
        {
            id: range_
            enabled: !dynamicRange_.checked
            from: (dynamicRange_.checked ? provider_.dynamicMin : parseFloat(manualRangeMin_.text)).toFixed(2)
            to  : (dynamicRange_.checked ? provider_.dynamicMax : parseFloat(manualRangeMax_.text)).toFixed(2)
            first.value: from.toFixed(2)
            second.value: to.toFixed(2)
            Layout.fillWidth: true
        }
        Label{text: range_.second.value.toFixed(2); width: 50}
        CheckBox
        {
            id : dynamicRange_
            text: "dynamic range"
            checked: true
        }
        Text{text: " || "}
        Text{text: "Min: "; width: 50}
        TextField 
        {
            id: manualRangeMin_
            text: provider_.absoluteMin
            selectByMouse: true
            enabled: !dynamicRange_.checked
        }
        Text{text: "Max: "; width: 50}
        TextField 
        {
            id: manualRangeMax_
            text: provider_.absoluteMax
            width: 50
            selectByMouse: true
            
            enabled: !dynamicRange_.checked
        }
    }
    FigureWithToolbar
    {
        figureProvider: EchoesMPLFigureProvider
        {
            id: provider_

            min: range_.first.value
            max: range_.second.value
            dynamicRange: dynamicRange_.checked
            colorMap: colormap_.currentText
            logScale: logScale_.checked
            flipud: flip_.checked
            rot90: rotated_.checked
            autoUpdate: true
            options: options_.currentText

            

        }
        Layout.fillWidth: true
        Layout.fillHeight: true
    }
} 