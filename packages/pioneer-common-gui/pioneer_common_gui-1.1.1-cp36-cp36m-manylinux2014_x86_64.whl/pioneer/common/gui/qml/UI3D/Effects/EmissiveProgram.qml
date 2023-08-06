/*
* Created on Feb 14, 2018
*
* \author: maxime
* \file : EmissiveProgram.qml
*/

import QtQuick 2.5
import Leddar 1.0

GLSLProgram
{
    id: component
    property color color : "black"
    property color backColor : "red"
    uniforms: ({color: color, backColor: backColor})
    vertexShader: "
                        #version 410
                        in highp vec4 vertices;
                        in highp vec3 normals;
                        uniform highp mat4 matrix;
                        uniform highp float point_size;
                        void main()
                        {
                            gl_Position = matrix*vertices;
                            gl_PointSize = point_size;
                        }
                   "
    fragmentShader: "
                        #version 410
                        uniform highp vec4 color;
                        uniform highp vec4 backColor;
                        layout(location = 0) out vec4 frag_color;
                        layout(location = 1) out vec4 frag_color_copy;
                        void main()
                        {
                            if (gl_FrontFacing) // is the fragment part of a front face?
                            {
                                frag_color = color;
                            }
                            else // fragment is part of a back face
                            {
                                frag_color = backColor;
                            }
                            frag_color_copy = frag_color;
                        }
                    "
}