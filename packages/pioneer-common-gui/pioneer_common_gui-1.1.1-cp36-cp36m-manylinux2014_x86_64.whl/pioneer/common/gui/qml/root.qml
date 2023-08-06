import QtQuick 2.0
import Examples 1.0
import Leddar 1.0
import UI3D 1.0
Item
{
    width: 800
    height: 600


    ExampleSim{}
    /*Viewport
    {
        anchors.fill: parent

        actors: Actors
        {
            Actor
            {
                id: component
                property real lineWidth : 1
                property color color : "black"
                property var from : [0,0,0]
                property var to : [1,0,0]

                geometry: Geometry
                {
                    primitiveType: Geometry.LINES
                    attribs: Attribs
                    {
                        vertices: ArrayFloat3
                        {
//                            input: [component.from, component.to]
                        }
                    }
                }
                effect: Effect
                {
//                    lineWidth: component.lineWidth
                    shader0:
                        GLSLProgram
                        {
//                            property color color : "black"
//                            property color backColor : "red"
//                            uniforms: ({color: color, backColor: backColor})
                            vertexShader: "
                                                #version 410
                                                in highp vec4 vertices;
                                                in highp vec3 normals;
                                                uniform highp mat4 matrix;
                                                void main()
                                                {
                                                    gl_Position = matrix*vertices;
                                                }
                                           "
                            fragmentShader: "
                                                #version 410
                                                uniform highp vec4 color;
                                                uniform highp vec4 backColor;
                                                out vec4 frag_color;
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
                                                }
                                            "
                        }// color: component.color }
                }
            }
//            SceneLab1
//            {
//                id: scene_
//                //visible: false
//            }
        }
    }*/
}
