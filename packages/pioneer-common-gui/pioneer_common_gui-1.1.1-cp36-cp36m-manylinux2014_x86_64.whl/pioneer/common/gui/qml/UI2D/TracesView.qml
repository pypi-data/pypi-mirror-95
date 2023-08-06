import QtQuick 2.9
import QtQuick.Controls 2.5
import QtCharts 2.3

import Leddar 1.0

ChartView
{
    id: component

    property int maxCounts: Math.pow(2,14)
    property int basePoints: 512
    property alias normalizeTraces: ds_.normalize
    property alias traces : ds_.traces

    
    signal roiChanged()

    function isInROI(channel)
    {
        var roi = ds_.getROI()
        var relative_index = channel - roi[0]
        return relative_index >= 0 && relative_index < roi[1];
    }
    property var selected : ({})
    function clear()
    {
        for (var channel in selected)
        {
            var s  = selected[channel];
            if(s)
                toggleIndex(channel)
        }
    }
    function toggleIndex(channel)
    {


        var r = selected[channel]

        if(r === null || r === undefined)
        {
            if(!isInROI(channel))
                throw Error("Index out of range: " + channel);

            var series = component.createSeries(ChartView.SeriesTypeLine, channel/*series label*/, axisX, axisY1)
            selected[channel] = series
            // series.useOpenGL = true;
            Object.defineProperty(series, 'channel',
            {
                enumerable: false,
                configurable: false,
                writable: false,
                value: channel - ds_.getROI()[0]
            });
        }
        else
        {
            view_.removeSeries(selected[channel])
            selected[channel] = null
        }
        ds_.makeDirty();
        return selected[channel]
    }

    TracesDataSource
    {
        id: ds_
    }
    
    Timer
    {
        interval: 50
        running: true
        repeat: true
        property var oldRoi: ds_.getROI()
        onTriggered:
        {
            if(ds_.dirty)
            {
                var roi = ds_.getROI()

                if(!(roi.length === oldRoi.length && roi.every(function(value, index) { return value === oldRoi[index]})))
                {
                    component.roiChanged();
                }
                for(var i = 0; i < component.count; i++)
                {
                    var s = component.series(i)
                    ds_.refresh(s, i, s.channel)
                }

            }
        }
    }

    title: "Traces"
    antialiasing: true
    width: parent.width
    height: parent.height*3/4

    MouseArea
    {
        acceptedButtons: Qt.AllButtons
        anchors.fill: parent

        Rectangle
        {
            id: zoomBox_
            color: Qt.rgba(0,0,1,0.5)
        }
        property rect scroll : Qt.rect(0,0,0,0)

        onPressed:
        {
            zoomBox_.visible = false;
            scroll.x = zoomBox_.x = mouse.x;
            scroll.y = zoomBox_.y = mouse.y;
            zoomBox_.width = 0;
            zoomBox_.height = 0;

            switch(mouse.button)
            {
                case Qt.LeftButton:
                    zoomBox_.visible = true;
                    break;
                case Qt.MiddleButton:
                    _scroll(-scroll.width , -scroll.height)
                    component.zoomReset();
            }
        }

        function _scroll(scroll_x, scroll_y)
        {
            if (scroll_x < 0)
                component.scrollLeft(scroll_x)
            else
                component.scrollRight(-scroll_x)

            if (scroll_y < 0)
                component.scrollUp(scroll_y)
            else
                component.scrollDown(-scroll_y)

            scroll.width += scroll_x;
            scroll.height += scroll_y;
        }
        onPositionChanged:
        {
            zoomBox_.width = mouse.x - zoomBox_.x
            zoomBox_.height = mouse.y - zoomBox_.y
            if (mouse.buttons & Qt.RightButton)
            {
                var scroll_x = mouse.x - scroll.x
                var scroll_y = mouse.y - scroll.y

                _scroll(scroll_x, scroll_y)

                scroll.x = mouse.x;
                scroll.y = mouse.y;
            }
        }
        onReleased:
        {
            if(zoomBox_.visible)
            {
                zoomBox_.visible = false
                component.zoomIn(Qt.rect(zoomBox_.x, zoomBox_.y, zoomBox_.width, zoomBox_.height))
            }
        }
        onWheel:
        {
            console.log(wheel.angleDelta)
            if (wheel.angleDelta.y > 0)
                component.zoom(1.1);
            else
                component.zoom(0.9);

        }
    }
    ValueAxis {
        id: axisY1
        min: -component.maxCounts
        max: component.maxCounts
    }


    ValueAxis {
        id: axisX
        min: 0
        max: component.basePoints
    }

}
