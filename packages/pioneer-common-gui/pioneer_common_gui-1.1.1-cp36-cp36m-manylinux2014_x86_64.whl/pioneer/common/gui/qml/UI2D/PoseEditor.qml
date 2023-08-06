import QtQuick 2.9
import QtQuick.Controls 2.5
import QtQuick.Controls 1.5 as Controls1
import QtQuick.Layouts 1.9

RowLayout
{
    id: component

    property string key : "" // support for wait_key()

    property alias px     : x_.value
    property alias py     : y_.value
    property alias pz     : z_.value
    property alias rx    : rx_.value
    property alias ry    : ry_.value
    property alias rz    : rz_.value
    property alias pscale : scale_.value

    readonly property var pose : ({x: px, y: py, z: pz, rx: rx, ry: ry, rz: rz})

    property bool rxVisible: true
    property bool ryVisible: true
    property bool scaleVisible: false

    Label
    {
        text: "x: "
    }
    Controls1.SpinBox
    {
        id: x_
        selectByMouse: true;
        decimals: stepSize_.currentText.length - 2; value: 0; stepSize: parseFloat(stepSize_.currentText); maximumValue: 180; minimumValue: -180
        Keys.onPressed: component.key = event.text // support for wait_key()
    }
    Label
    {
        text: "y: "
    }
    Controls1.SpinBox
    {
        id: y_
        selectByMouse: true;
        decimals: stepSize_.currentText.length - 2; value: 0; stepSize: parseFloat(stepSize_.currentText); maximumValue: 180; minimumValue: -180;
        Keys.onPressed: component.key = event.text // support for wait_key()
    }
    Label
    {
        text: "z: "
    }
    Controls1.SpinBox
    {
        id: z_
        selectByMouse: true;
        decimals: stepSize_.currentText.length - 2; value: 0; stepSize: parseFloat(stepSize_.currentText); maximumValue: 180; minimumValue: -180;
        Keys.onPressed: component.key = event.text // support for wait_key()
    }
    Label
    {
        text: "rx: "
        visible: component.rxVisible
    }
    Controls1.SpinBox
    {
        id: rx_
        selectByMouse: true;
        decimals: stepSize_.currentText.length - 2; value: 0; stepSize: parseFloat(stepSize_.currentText); maximumValue: 180; minimumValue: -180;
        Keys.onPressed: component.key = event.text // support for wait_key()
        visible: component.rxVisible
    }
    Label
    {
        text: "ry: "
        visible: component.ryVisible
    }
    Controls1.SpinBox
    {
        id: ry_
        selectByMouse: true;
        decimals: stepSize_.currentText.length - 1; value: 0; stepSize: parseFloat(stepSize_.currentText); maximumValue: 180; minimumValue: -180;
        Keys.onPressed: component.key = event.text // support for wait_key()
        visible: component.ryVisible
    }
    Label
    {
        text: "rz: "
    }
    Controls1.SpinBox
    {
        id: rz_
        selectByMouse: true;
        decimals: stepSize_.currentText.length - 2; value: 0; stepSize: parseFloat(stepSize_.currentText); maximumValue: 180; minimumValue: -180;
        Keys.onPressed: component.key = event.text // support for wait_key()
    }
    Label
    {
        text: "scale: "
        visible: component.scaleVisible
    }
    Controls1.SpinBox
    {
        id: scale_
        selectByMouse: true;
        decimals: Math.max(2, stepSize_.currentText.length - 2); value: 1; stepSize: parseFloat(stepSize_.currentText);
        Keys.onPressed: component.key = event.text // support for wait_key()
        visible: component.scaleVisible
    }
    Label
    {
        text: "step size: "
    }
    ComboBox
    {
        id: stepSize_
        currentIndex: 2
        model: [1, 0.1, 0.01, 0.0001]
        
    }
}