/*
* Created on Feb 26, 2018
*
* \author: maxime
* \file : AmplitudesProgram.qml
*/

import QtQuick 2.5
import Leddar 1.0

GLSLProgram
{
    id: component
    property color color : "black"
    uniforms: ({color: color})
    vertexShader: "
                        #version 410
                        uniform highp mat4 matrix;
                        uniform highp float point_size;
                        in highp vec4 vertices;
                        in highp vec3 normals;
                        in highp float amplitude;

                        out float a;
                        void main()
                        {
                            gl_Position = matrix*vertices;
                            gl_PointSize = point_size;
                            a = amplitude;
                        }
                   "
    fragmentShader: "
                        #version 410
                        uniform highp vec4 color;
                        in float a;
                        layout(location = 0) out vec4 frag_color;
                        layout(location = 1) out vec4 frag_color_copy;
                        void main()
                        {
                            float t = (.25 + a) / 1.25; //ensure minimal visibility
                            frag_color_copy = frag_color = vec4(color.x * t, color.y * t, color.z * t, color.w);
                        }
                    "
}