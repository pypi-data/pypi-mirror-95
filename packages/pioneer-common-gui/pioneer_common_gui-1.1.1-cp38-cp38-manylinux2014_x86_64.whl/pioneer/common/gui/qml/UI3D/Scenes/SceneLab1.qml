/*
* Created on May 29, 2018
*
* @author: maxime
* \file : SceneLab1.qml
*
*/
import Leddar 1.0
import UI3D 1.0




Actors
{
    id: component

    property bool visible : true

    property real wallDistance : 2.6
    property real leftWallX : 1.75
    property real rightWallX : -1.8

    property real boxZ: 1.8
    property real boxTopY: -.125
    property real boxBottomY: 1
    property real leftBoxX : .11
    property real rightBoxX : -.37

    readonly property alias sceneVertices: sceneVertices_
    readonly property alias sceneIndices : sceneIndices_
    XYZ{}
    Actor
    {
        id: scene_
        visible: component.visible
        geometry: Geometry
        {
            primitiveType: Geometry.TRIANGLES;

            indices: ArrayUInt1
            {
                id: sceneIndices_
                input:
                [
                    1, 3   ,0
                  , 1, 2   ,3
                  , 4, 2   ,1
                  , 4, 5   ,2
                  , 0, 7   ,6
                  , 0, 3   ,7
                  , 8,  11 ,10
                  , 11, 8  , 9
                ]
            }
            attribs: Attribs
            {
                vertices: ArrayFloat3
                {
                    id: sceneVertices_
                    input:
                    [
                    //back wall:
                      [rightWallX, -1 ,wallDistance   ] //0
                    , [ leftWallX, -1 ,wallDistance   ] //1
                    , [ leftWallX,  1 ,wallDistance   ] //2
                    , [rightWallX,  1 ,wallDistance   ] //3

                    //left wall
                    , [leftWallX,-1 ,0     ] //4
                    , [leftWallX, 1 ,0     ] //5

                    //right shelf
                    , [rightWallX,-1, wallDistance-.9 ] //6
                    , [rightWallX, 1, wallDistance-.9 ] //7

                    //box:
                    , [leftBoxX , boxTopY   , boxZ ] //8
                    , [leftBoxX , boxBottomY, boxZ ] //9
                    , [rightBoxX, boxTopY   , boxZ ] //10
                    , [rightBoxX, boxBottomY, boxZ ] //11
                    ]
                }
                normals: ArrayFloat3
                {
                     input:
                     [
                         [0, 0, 1] //0
                        ,[0, 0, 1] //1
                        ,[0, 0, 1] //2
                        ,[0, 0, 1] //3
                        ,[-1, 0, 0] //4
                        ,[-1, 0, 0] //5
                        ,[1, 0, 0] //6
                        ,[1, 0, 0] //7
                        ,[1, 0, 0] //8
                        ,[1, 0, 0] //9
                        ,[1, 0, 0] //10
                        ,[1, 0, 0] //11

                    ]
                }
            }
        }

        effect: Effect
        {
            shader0: MaterialProgram{color: Qt.rgba(.5, .5, .5, .8); backColor: "red"}
        }
    }
}