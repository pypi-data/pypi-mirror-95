/*
* Created on Feb 26, 2018
*
* \author: maxime
* \file : AmplitudesProgram.qml
*/

import QtQuick 2.5
import UI3D 1.0

EmissiveProgram
{
    vertexShader: "
                #version 410
                uniform highp mat4 matrix;
                in highp vec4 vertices;
                in highp vec4 colors;

                out vec4 color;
                void main()
                {
                    gl_Position = matrix*vertices;
                    color = colors;
                }
            "
    fragmentShader: "
                #version 410
                in vec4 color;
                layout(location = 0) out vec4 frag_color;
                layout(location = 1) out vec4 frag_color_copy;
                void main()
                {
                    frag_color_copy = frag_color = color;
                }
            "
}