/*
* Created on Feb 26, 2019
*
* @author: maxime
* \file : Actors.qml
*
*/

import QtQuick 2.5
import Leddar 1.0
import UI3D 1.0

#PySide2 workaround
Actors_
{

    default property list<Renderable> renderables_;

    renderables:
    {
        var l = [];
        for (var i = 0; i < renderables_.length; i++)
            l.push(renderables_[i]);
        console.log(l)
        return l;
    }

}