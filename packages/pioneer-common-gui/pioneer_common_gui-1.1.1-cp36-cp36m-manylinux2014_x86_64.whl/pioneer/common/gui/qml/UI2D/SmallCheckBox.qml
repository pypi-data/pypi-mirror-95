import QtQuick 2.9
import QtQuick.Controls 2.5

CheckBox
{
    font.pointSize: 8
    indicator.width: 15
    indicator.height: 15
    Component.onCompleted: indicator.children[0].scale = 0.5
}