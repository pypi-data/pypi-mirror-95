/*
* Created on Apr 2, 2018
*
* @author: maxime
* \file : Box.qml
*
*/

import QtQuick 2.5
import Leddar 1.0
import UI3D 1.0

Actor
{
    id: component


    property var center : [0,0,0]
    property var dimensions : [1,1,1]

    property var min : center.map(function(c, i){return c - dimensions[i]/2})
    property var max : center.map(function(c, i){return c + dimensions[i]/2})
    property alias color: program_.color

    property bool filled: true

    geometry: Geometry
    {
        primitiveType: filled ? Geometry.TRIANGLES : Geometry.LINES;

        indices: ArrayUInt1
        {
            input: filled ? [0,1,3, 3,2,0, /**/ 7,5,4, 4,6,7, /**/ 4,5,1, 1,0,4, /**/ 5,7,3, 3,1,5, /**/ 6,2,3, 3,7,6, /**/ 4,0,2, 2,6,4]
                          : [0,1, 1,3, 3,2, 2,0, /**/  4,5, 5,7, 7,6, 6,4, /**/ 0,4, 1,5, 2,6, 3,7]
        }
        attribs: Attribs
        {
            vertices : ArrayFloat3
            {
                input:
                [
                  [min[0], min[1], min[2]] //0
                , [min[0], min[1], max[2]] //1
                , [min[0], max[1], min[2]] //2
                , [min[0], max[1], max[2]] //3
                , [max[0], min[1], min[2]] //4
                , [max[0], min[1], max[2]] //5
                , [max[0], max[1], min[2]] //6
                , [max[0], max[1], max[2]] //7
                ]
            }
            normals: ArrayFloat3
            {
                 input:
                 [
                 [-0.577350269,-0.577350269,-0.577350269] //0
                ,[-0.577350269,-0.577350269, 0.577350269] //1
                ,[-0.577350269, 0.577350269,-0.577350269] //2
                ,[-0.577350269, 0.577350269, 0.577350269] //3
                ,[ 0.577350269,-0.577350269,-0.577350269] //4
                ,[ 0.577350269,-0.577350269, 0.577350269] //5
                ,[ 0.577350269, 0.577350269,-0.577350269] //6
                ,[ 0.577350269, 0.577350269, 0.577350269] //7
                ]
            }
        }
    }

    effect: Effect
    {
        shader0: MaterialProgram{id: program_; }
    }
}