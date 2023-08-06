/*
* Created on Dec 12, 2018
*
* \author: maxime
* \filename: LCAActor.qml
*/

import QtQuick 2.9
import Leddar 1.0
import UI3D 1.0
import QtQuick.Controls 2.4

Actors
{
    id: component

    //cheddar_config api:
    property alias bankSelection: cloud_.bankSelection 
    property alias minAmplitude : cloud_.minAmplitude 
    property alias maxAmplitude : cloud_.maxAmplitude 
    property alias specs        : cloud_.specs 
    property alias packages     : cloud_.packages

    // das api:
    property alias indices      : geometry_.indices
    property alias vertices     : amplitudeAttribs_.vertices
    property alias amplitude    : amplitudeAttribs_.amplitude

    property alias cloud: cloud_

    property string colorMap : 'jet'
    property color frustrumColor: Qt.rgba(.3,.3,.3,1)
    property bool visible: true
    property alias transform : echoActor_.transform
    property alias frustrumDepth: frustrum_.depth

    property var clickEcho //(int v, int h)
    Sensor
    {
    	id: frustrum_
    	objectName: component.objectName + "_frustrum"
        visible: component.visible
        specs: cloud_.specs
        transform: echoActor_.transform
        color: component.frustrumColor
    }
    property var cursor: Rectangle
    {
    	id: cursor_
    	property real distance: 0
        property real amplitude: 0
        property int timestamp: 0
        property int flag: 0
    	property int h: 0
    	property int v: 0
    	border.width : 1
    	visible:false
    	onVisibleChanged:
    	{
    		if(visible)
    			cursorTimer_.start();
    	}
    	color: 'gray'
    	Column
    	{
    		id: column_
    		anchors.fill: parent
    		leftPadding: 5
    		rightPadding: 5
    		Label{text:'channel (v,h): ' + cursor_.v + ', ' + cursor_.h}
    		Label{text:'distance: ' + cursor_.distance.toFixed(2)}
            Label{text:'amplitude: ' + cursor_.amplitude.toFixed(0)}
            Label{text:'ts offset: ' + cursor_.timestamp}
            Label{text:'flag: ' + cursor_.flag}
    	}
    	width: column_.implicitWidth
    	height: column_.implicitHeight
    	Timer
    	{
    		id: cursorTimer_
    		interval: 100
    		onTriggered: cursor_.visible = false
    	}
    }
    Actor
    {

        id: echoActor_
        objectName: component.objectName + "_echoActor"
        visible: component.visible
        geometry: Geometry
        {
            id: geometry_
            primitiveType: Geometry.TRIANGLES
            indices: cloud_.indices
            attribs: AmplitudeAttribs
            {
                id: amplitudeAttribs_
                vertices : SurfaceCloud
                {
                    id: cloud_
                    objectName: "cloud"
                    //bankSelection: input alias 
                    //minAmplitude : input alias 
                    //maxAmplitude : input alias 
                    //specs        : input alias 
                    //packages     : input alias 
                }
                amplitude: cloud_.amplitudes
            }
        }
        onClicked:
        {
            console.log('actor clicked!')
            var info = cloud_.channelInfo(id);
            if (component.clickEcho !== undefined)
                component.clickEcho(info.v, info.h)
        }
        onHovered:
        {
            var info = cloud_.channelInfo(id);
            component.cursor.parent = viewport;
            component.cursor.x = event.pos.x+5;
            component.cursor.y = event.pos.y;
            component.cursor.v = info.v;
            component.cursor.h = info.h;
            component.cursor.distance = info.distance;
            component.cursor.amplitude = info.amplitude;
            component.cursor.timestamp = info.timestamp;
            component.cursor.flag = info.flag;
            component.cursor.visible = true;
        }
        effect: Effect
        {
            shader0: ColorMapProgram{defaultColorMap.colorMap: component.colorMap}
        }
    }
}