/*
* Created on Sep 7, 2018
*
* \author: Maxime Lemonnier
* \filename: TracesChart.qml
*/

import QtQuick 2.12
import QtQuick.Controls 2.5
import QtCharts 2.3

Column
{
    id: component

    property int v
    property int h
    property alias basePoints : view_.basePoints
    property alias maxCounts : view_.maxCounts
    property alias normalizeTraces : view_.normalizeTraces
    property alias traces : view_.traces

    width: 500
    height: 800


    function toggleCell(v, h)
    {
        canvas_.toggleCell(v, h);
    }

    Row
    {
        Button
        {
            text: 'clear selection'
            onClicked: {canvas_.selected = []; canvas_.requestPaint(); view_.clear();}
        }
        Button
        {
            text: 'reset zoom'
            onClicked: view_.zoomReset()
        }
    }


    Row
    {
        Canvas 
        {
            id: canvas_
            property real magnify: 4
            width: h * magnify
            height: v * magnify
            property var selected : []

            function toCoord(x, y)
            {
                return Qt.point(Math.floor(x/magnify), Math.floor(y/magnify));
            }
            function toggleCell(v, h)
            {
                var s = view_.toggleIndex(v * component.h + h);
                
                if(s)
                    selected.push({x: h, y: v, color: s.color});
                else
                {
                    var i = selected.findIndex(function (element) 
                    {
                        return element.x == h && element.y == v;
                    });

                    if(i == -1)
                        throw Error("Unexpected index");

                    selected.splice(i, 1);
                }
                    
                requestPaint();
            }
            
            onPaint: 
            {
                var ctx = getContext("2d");
                ctx.fillStyle = Qt.tint("grey", "grey")
                ctx.fillRect(0, 0, width, height);

                ctx.fillStyle = Qt.tint("green", "green")

                for(var x = 0; x < h; x++)
                {
                    for(var y = 0; y < v; y++)
                    {
                        if(view_.isInROI(y * h + x))
                            ctx.fillRect(x*magnify, y*magnify, magnify, magnify);
                    }
                }

                for(var i in selected)
                {
                    var s = selected[i]
                    ctx.fillStyle = s.color
                    ctx.fillRect(s.x*magnify, s.y*magnify, magnify, magnify);
                }
            }

            Rectangle
            {
                id: cursor_
                z : 10
                property int h: 0
                property int v: 0
                property int channel: cursor_.v * component.h + cursor_.h
                property bool isInRoi: view_.isInROI(channel);
                border.width : 1
                visible: mouseArea_.containsMouse
                color: isInRoi ? 'green' : 'red'
                Column
                {
                    id: column_
                    anchors.fill: parent
                    leftPadding: 5
                    rightPadding: 5
                    Label{text: 'chan ' + cursor_.channel + ' (' + cursor_.v + ', ' + cursor_.h + ')'}
                }
                width: column_.implicitWidth
                height: column_.implicitHeight
            }


            MouseArea
            {
                id: mouseArea_

                anchors.fill: parent

                cursorShape: cursor_.isInRoi ? Qt.PointingHandCursor : Qt.ForbiddenCursor

                hoverEnabled: true

                onPositionChanged:
                {
                    var pt = canvas_.toCoord(mouse.x, mouse.y)
                    cursor_.x = mouse.x-cursor_.width/2;
                    cursor_.y = mouse.y+25;
                    cursor_.h = pt.x;
                    cursor_.v = pt.y;
                }


                onPressed: 
                {
                    if (mouse.buttons == Qt.LeftButton)
                    {
                        var pt = canvas_.toCoord(mouse.x, mouse.y);

                        canvas_.toggleCell(pt.y, pt.x)
                    }
                }
            }
        }

        
        TracesView
        {
            id: view_
            onRoiChanged: canvas_.requestPaint()
            width: component.width - canvas_.width
            height: component.height - 50
        }
    }
}