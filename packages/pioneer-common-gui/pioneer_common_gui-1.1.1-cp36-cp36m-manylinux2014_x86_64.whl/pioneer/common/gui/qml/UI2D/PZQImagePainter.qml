import QtQuick 2.9
import Leddar 1.0

QImagePainter
{
    id: component

    width: parent.width
    height: parent.height
    transform : [Scale{id: s_}, Translate{id: t_}]
    z: -1
    property var pick // Tried to use signals here, ended up with segfaults, will use functors instead
    property var leaved
    MouseArea
    {
        anchors.fill: parent
        acceptedButtons: Qt.AllButtons 
        onWheel:
        {
            s_.origin.x = wheel.x;
            s_.origin.y = wheel.y;
            s_.xScale += s_.xScale * wheel.angleDelta.y / 120 / 10;
            s_.xScale = Math.max(1.0, s_.xScale);
            s_.yScale = s_.xScale;
        }
        property int startX : 0
        property int startY : 0
        onPressed: 
        {
            if (mouse.buttons == Qt.LeftButton)
            {
                if(mouse.modifiers == Qt.ShiftModifier)
                {
                    var mapped = component.mapToImage(mouse.x, mouse.y)
                    component.pick(mouse.buttons, mouse.modifiers, mapped.x, mapped.y)
                }
                else
                {
                    startX = mouse.x; 
                    startY = mouse.y
                }
            }
        }
        onExited: component.leaved()
        function clamp(v, min, max)
        {
            return Math.min(Math.max(v, min), max);
        }
        hoverEnabled: true
        onPositionChanged:
        {
            if (mouse.buttons == Qt.LeftButton)
            {
                t_.x += (mouse.x - startX);

                var w = component.width*s_.xScale
                t_.x = clamp(t_.x, component.width/2-w/2, w/2-component.width/2)


                var h = component.height*s_.yScale
                t_.y += (mouse.y - startY);
                t_.y = clamp(t_.y, component.height/2-h/2, h/2-component.height/2)
            }
            else if (mouse.buttons == 0)
            {
                var mapped = component.mapToImage(mouse.x, mouse.y)

                component.pick(mouse.buttons, mouse.modifiers, mapped.x, mapped.y)
            }
        }
        onDoubleClicked:
        {
            t_.x = t_.y = 0;
            s_.xScale = s_.yScale = 1;
        }

    }
}
