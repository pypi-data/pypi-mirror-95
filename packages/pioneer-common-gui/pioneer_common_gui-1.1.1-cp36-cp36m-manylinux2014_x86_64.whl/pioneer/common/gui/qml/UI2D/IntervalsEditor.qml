import QtQuick 2.9
import QtQuick.Controls 2.5
import Misc 1.0

TextField
{
    id: component

    property QtObject cursorsOwner : QtObject 
    {
        id: defaultOwner_
        property var cursors: []
    }
    property alias defaultCursors: defaultOwner_.cursors //only usefull if cursorOwner is defaultOwner_.
    
    property real max: Number.MAX_VALUE

    selectByMouse: true

    function cursorsToText()
    {
        //python list of tuples reprensenting an interval
        var text = ""
        for (var i = 1; i < component.cursorsOwner.cursors.length; i+=2)
        {
            text += "["+ component.cursorsOwner.cursors[i-1] + ", " + component.cursorsOwner.cursors[i] + "]"
            
            text += (i+2 < component.cursorsOwner.cursors.length) ? "," : ""
        }
        return "[" + text + "]";
    }

    text: cursorsToText()

    Binding on text
    {
        value: component.cursorsToText()
    }

    onEditingFinished: 
    {
        try
        {
            var parsed = JSON.parse(text);
            var l = [];
            for (var i in parsed)
            {
                l.push(...parsed[i]);
            }
            
            Utils.sort(l)
            
            if (l[0] < 0 || l[l.length-1] >= component.max)
                throw "At least one index out of bounds [0," + (component.max-1) + "] : " + JSON.stringify(l)

            component.cursorsOwner.cursors = l;
        }
        catch(e)
        {
            console.log("Caught exception: " + e);
            text = component.cursorsToText()
            return;
        }
    }
}