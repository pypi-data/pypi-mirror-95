import QtQuick 2.9
import QtQuick.Window 2.9
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.11

import Leddar 1.0
import UI2D 1.0


Column
{
    id: component
    property var imageArray
    property var tracesChart
    property alias range : range_
    signal clickedChannel(int v, int h)
    Column
    {
        id: controls_
        Row
        {
            Label{text: range_.first.value; width: 50}
            RangeSlider
            {
                id: range_
                from: -Math.pow(2, 14)
                to: Math.pow(2, 20)
                first.value: from
                second.value: 10000
                width: amplitude_.width - 100
            }
            Label{text: range_.second.value; width: 50}
        }
        Row
        {
            ComboBox
            {
                id: colormap_
                model: ["viridis", "plasma", "cool", "copper"]
            }
            CheckBox
            {
                id: colormapInvert_
                text: "inverted"
                checked: false
            }
            CheckBox
            {
                id: log_
                text: "log scale"
                checked: true
            }
            CheckBox
            {
                id: interpolate_
                text: "Interpolate (test mode)"
                checked: false
            }
            Label
            {
                text: "Toggle traces: Shift+LeftButton\nPan: LeftButton\nZoom: wheel\nReset: Double+LeftButton"
            }
            Label
            {
                property alias p : viewer_.picked
                text: p ? ("value: " + p.value + " @ [" + p.x + ", " + p.y + "] (index: " + p.index + ")") : ""
            }
        }
    }
    
    anchors.fill: parent
    PZQImagePainter
    {
        id: viewer_
        property var picked: null
        height: parent.height - controls_.implicitHeight
        imageArray: ColorMapFliter
        {
            min: range_.first.value
            max: range_.second.value
            log: log_.checked
            interpolate: interpolate_.checked
            colorMap: (colormap_.currentText == '' ? colormap_.model[0]: colormap_.currentText) 
                    + (colormapInvert_.checked ? "_r" : "")
            imageArray: component.imageArray
        }
        pick: function (buttons, modifiers, imageX, imageY)
        {
            imageX = Math.floor(imageX)
            imageY = Math.floor(imageY)
            if(buttons == 0)
            {
                var img = component.imageArray
                var rows = img.shape[0]
                var cols = img.shape[1]
                console.log(rows, cols, imageY, imageX)
                picked = {value: img.value([imageY, imageX]) //row, col
                    , x: imageX
                    , y: imageY
                    , index: (cols * imageY + imageX)};
            }
            else if(buttons == Qt.LeftButton && modifiers == Qt.ShiftModifier)
            {
                component.clickedChannel(imageY, imageX); //v, h
            }
        }
        leaved: function(){ picked = null}
    }
}