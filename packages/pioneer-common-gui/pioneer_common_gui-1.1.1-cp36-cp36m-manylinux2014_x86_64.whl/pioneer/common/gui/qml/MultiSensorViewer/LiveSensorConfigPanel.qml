import QtQuick 2.9
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.11
import Leddar 1.0

Flickable
{
    id: component
    
    property var live

    contentWidth: rectangle_.width
    contentHeight: rectangle_.height
    clip: true
    flickableDirection: Flickable.VerticalFlick

    ScrollBar.vertical: ScrollBar {}

    Rectangle
    {
        id: rectangle_
        width : component.width
        height: content_.implicitHeight
        color: "white"
        Column
        {
            id: content_


            GridLayout
            {
                columns: 2
                Label
                {
                    text: 'ip: '
                }
                TextField
                {
                    id: ip_
                    width: 100
                    //validator: RegExpValidator { regExp: /\d{3}.\d{3}.\d{3}.\d{3}/ }
                    text: component.live.ip
                    onEditingFinished:
                    {
                        component.live.changeIP(text); //does no appear to be working..
                    }
                    Binding on text
                    {
                        delayed: true
                        value: component.live.ip
                    }
                }


                Label
                {
                    text: 'connection status: '
                }
                CheckBox
                {
                    checked: component.live.connected
                    enabled: false
                }
                Label
                {
                    text: 'running: '
                }
                CheckBox
                {
                    checked: component.live.running
                    onCheckedChanged: component.live.running = checked
                    Binding on checked
                    {
                        delayed: true
                        value: component.live.running
                    }
                }
                Label
                {
                    text: 'fps: '
                }
                Label
                {
                    text: component.live.fps.toFixed(1)
                }
                Label
                {
                    text: 'state: '
                }
                Label
                {
                    height: 200
                    width: 50
                    text: LeddarUtils.prettyPrint(component.live.states)
                    wrapMode: Text.WordWrap
                }
                Label{height: 25; width: 200; text: 'traces mode:'}
                ComboBox
                {
                    height: 25
                    textRole: "key"
                    model: ListModel 
                    {
                        id: model
                        ListElement { key: "NONE"; value: LiveCapture.NONE }
                        ListElement { key: "RAW"; value: LiveCapture.RAW }
                        ListElement { key: "PROCESSED"; value: LiveCapture.PROCESSED }
                    }

                    currentIndex: component.live.tracesMode

                    onActivated: 
                    {
                        component.live.tracesMode = model.get(currentIndex).value
                    }
                    
                }
                Label
                {
                    id: roiLabel_
                    visible: component.live.tracesMode != 0
                    text: 'traces roi (' + component.live.nChannels + ' channels): '
                }
                Row
                {
                    id: roi_

                    visible: roiLabel_.visible
                    
                    function setROI()
                    {
                        var f = parseInt(tracesROIFrom_.text)
                        var t = parseInt(tracesROITo_.text)

                        component.live.tracesROI = [f, t-f]
                    }
                    Text{text: "from "}
                    TextField 
                    {
                        id: tracesROIFrom_
                        width: 75
                        height: 25
                        text: component.live.tracesROI[0]
                        validator :  IntValidator 
                        { 
                            bottom: 0
                            top: component.live.nChannels - 1
                        }
                        selectByMouse: true
                        // inputMethodComposing: true
                        onEditingFinished:  roi_.setROI()
                        Binding on text
                        {
                            delayed: true
                            value: component.live.tracesROI[0]
                        }
                    }
                    Text{text: " to "}
                    TextField 
                    {
                        id: tracesROITo_
                        width: 75
                        height: 25
                        text: component.live.tracesROI[0] + component.live.trancesROI[1]
                        validator :  IntValidator 
                        { 
                            bottom: component.live.tracesROI[0]
                            top: component.live.nChannels
                        }
                        selectByMouse: true
                        // inputMethodComposing: true
                        onEditingFinished: roi_.setROI()
                        Binding on text
                        {
                            delayed: true
                            value: component.live.tracesROI[0] + component.live.tracesROI[1]
                        }
                    }
                    Button
                    {
                        text: "top"
                        onClicked: {tracesROITo_.text = component.live.nChannels; roi_.setROI()}
                    }


                }
                Button
                {
                    id: calibration_
                    text: 'Calibration'
                    checkable: true
                    checked: false
                }
                Text{text: '...'; visible: !calibration_.checked}
                Rectangle
                {
                    border.width: 1
                    visible: calibration_.checked
                    width: calibPanel_.width
                    height: calibPanel_.height
                    CalibPanel
                    {
                        id: calibPanel_
                        live: component.live
                    }
                }
                Button
                {
                    id: memory_
                    text: 'Memory'
                    checkable: true
                    checked: false
                }
                Text{text: '...'; visible: !memory_.checked}
                Rectangle
                {
                    border.width: 1
                    visible: memory_.checked
                    width: memoryPanel_.width
                    height: memoryPanel_.height
                    GridLayout
                    {
                        id: memoryPanel_
                        columns: 2
                        Label
                        {
                            text: 'zone: '
                        }
                        ComboBox
                        {
                            id: memoryZone_
                            model: [3, 4]
                        }

                        Label
                        {
                            text: 'address: '
                        }
                        TextField 
                        {
                            id: address_
                            placeholderText: "0x0000 - 0xFFFF"
                            validator: RegExpValidator { regExp: /0x[0-9A-F]{4}/ }
                        }
                        Label
                        {
                            text: 'value (32 bits): '
                        }
                        TextField 
                        {
                            id: value_
                            placeholderText: "0x00000000 - 0xFFFFFFFF"
                            validator: RegExpValidator { regExp: /0x[0-9A-F]{8}/ }
                            selectByMouse: true
                        }
                        Button
                        {
                            text: 'write!'
                            onClicked: 
                            {
                                var result = component.live.writeMemory(memoryZone_.model[memoryZone_.currentIndex], parseInt(address_.text), parseInt(value_.text))

                                if(result)
                                {
                                    console.log((value_.text.length - 2)/2)
                                    var val = component.live.readMemory(memoryZone_.model[memoryZone_.currentIndex], parseInt(address_.text), (value_.text.length - 2)/2)

                                    readBack_.text = "read back '" + val + "'"
                                }
                                else
                                {
                                    readBack_.text = "write failed!"
                                }
                            }
                        }
                        Label
                        {
                            id: readBack_
                        }
                        Label
                        {
                            text: "n bytes: "
                        }
                        TextField 
                        {
                            id: nBytes_
                            placeholderText: "1-4"
                            text: "4"
                            validator: RegExpValidator { regExp: /[0-9]{1}/ }
                            selectByMouse: true
                        }
                        Button
                        {
                            text: 'read!'
                            onClicked: 
                            {

                                var val = component.live.readMemory(memoryZone_.model[memoryZone_.currentIndex], parseInt(address_.text), parseInt(nBytes_.text))

                                read_.text = "read '" + val + "'"
                            }

                        }
                        TextEdit 
                        {
                            id: read_
                            readOnly: true
                            wrapMode: Text.WordWrap
                            selectByMouse: true
                        }
                    }
                }
            }

            Column
            {
                Repeater
                {
                    model: component.live.properties
                    Row
                    {
                        id: row_
                        property var values : component.live.connected ? component.live.getPropertyAvailableValues(modelData) : null
                        property bool isValid : values !== null && values !== undefined
                        Label{visible: row_.isValid; height: 25; width: 250; text: modelData}
                        CheckBox
                        {
                            visible: row_.isValid && row_.values['type'] == 'bool'
                            enabled: row_.isValid && !row_.values['const'] 
                            height: 20
                            checked: row_.isValid ? row_.values['current'] : false

                            onToggled:
                            {
                                component.live.setLeddarProperty(modelData, checked)
                            }
                        }
                        ComboBox
                        {
                            visible: row_.isValid && row_.values['type'] == 'list'
                            height: 25
                            model: row_.isValid ? row_.values['data'] : []
                            currentIndex: row_.isValid ? find(row_.values['current']) : 0

                            onActivated:
                            {
                                component.live.setLeddarProperty(modelData, model[index])
                            }
                        }
                        TextField 
                        {
                            visible: row_.isValid && row_.values['type'] == 'text' 
                            readOnly: row_.isValid && row_.values['const'] 
                            height: 25
                            selectByMouse: true
                            text: row_.isValid ? row_.values['current'] : ''
                            
                            Binding on text
                            {
                                delayed: true
                                value: row_.isValid ? row_.values['current'] : ''
                            }
                            onEditingFinished:
                            {
                                if(row_.values['current'] != text)
                                    component.live.setLeddarProperty(modelData, text)
                            }
                        }
                        TextField 
                        {
                            id: bitfield_
                            visible: row_.isValid && row_.values['type'] == 'bitfield' 
                            readOnly: row_.isValid && row_.values['const'] 
                            height: 25
                            selectByMouse: true
                            //validator: RegExpValidator { regExp: /0b[01]{8}/ }

                            function toBitfield()
                            {
                                return row_.isValid ? '0b' + String('00000000' + row_.values['current']).slice(-8): ''
                            }
                            text: toBitfield()
                            Binding on text
                            {
                                delayed: true
                                value: bitfield_.toBitfield()
                            }
                            onEditingFinished:
                            {
                                var newValue = text.replace(new RegExp("0b"), "")
                                if(row_.values['current'] != newValue)
                                {
                                    var rv = component.live.setLeddarProperty(modelData, newValue)
                                    if(!rv)
                                    {
                                        component.live.setLeddarProperty(modelData, '00000000') // work around "Several exclusive bits are set."
                                        component.live.setLeddarProperty(modelData, newValue)
                                    }
                                }
                            }
                        }
                        Row
                        {
                            visible: row_.isValid && row_.values['type'] == 'range' 
                            TextField 
                            {
                                readOnly: row_.isValid && row_.values['const'] 
                                height: 25
                                selectByMouse: true
                                text: row_.isValid ? row_.values['current'] : ''
                                validator :  DoubleValidator 
                                {
                                    id: validator_ 
                                    bottom: row_.isValid && row_.values['data'] ? parseFloat(row_.values['data'][0]) : 0
                                    top: row_.isValid && row_.values['data'] ? parseFloat(row_.values['data'][1]) : 1
                                }
                                Binding on text
                                {
                                    delayed: true
                                    value: row_.isValid ? row_.values['current'] : ''
                                }
                                onEditingFinished:
                                {
                                    if(row_.values['current'] != text)
                                        component.live.setLeddarProperty(modelData, text)
                                }
                            }
                            Row
                            {
                                visible: row_.isValid && !row_.values['const'];
                                Label{height: 25; text: " [" + validator_.bottom.toPrecision(5) + " - "}
                                Label{height: 25; text: validator_.top.toPrecision(5) + "]"}
                            }
                        }

                        Label
                        {
                            text: row_.isValid ? row_.values['description'] : ' '
                            font.italic: true
                        }
                    }
                }
            }
        }
    }


}