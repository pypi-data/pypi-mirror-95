/*
* Created on Apr 2, 2018
*
* \author: maxime
* \file : MaterialProgram.qml
*/

import QtQuick 2.5
import Leddar 1.0

GLSLProgram
{
    id: component
    property color color : "black"
    property color backColor : "red"
    property real shininess : 5
    uniforms: ({color: component.color, backColor: component.backColor, shininess: component.shininess})
    vertexShader:
    "
                        #version 410
                        // Adpated from https://en.wikibooks.org/wiki/GLSL_Programming/GLUT/Specular_Highlights
                        in vec4 vertices;
                        in vec3 normals;
                        uniform mat4 model_matrix, view_matrix, projection_matrix;
                        uniform mat3 normal_matrix;
                        uniform mat4 view_matrix_inv;

                        uniform vec4 color;
                        uniform vec4 backColor;
                        uniform float shininess;
                        // TODO add material uniforms

                        out vec4 front_color; // color for front face
                        out vec4 back_color; // color for back face

                        struct light_source
                        {
                            vec4 position;
                            vec4 diffuse;
                            vec4 specular;
                            float constant_attenuation, linear_attenuation, quadratic_attenuation;
                            float spot_cutoff, spot_exponent;
                            vec3 spot_direction;
                        };

                        light_source light0 = light_source(
                            vec4(0,0,0, 1.0),
                            vec4(1.0,  1.0,  1.0, 1.0),
                            vec4(1.0,  1.0,  1.0, 1.0),
                            0.0, .2, 0.0,
                            180.0, 0.0,
                            vec3(0.0, 0.0, 0.0)
                        );
                        vec4 scene_ambient = vec4(0.2, 0.2, 0.2, 1.0);

                        struct material
                        {
                            vec4 ambient;
                            vec4 diffuse;
                            vec4 specular;
                            float shininess;
                        };
                        material front_material = material(
                            vec4(1.0, 1.0, 1.0, 1.0),
                            color,
                            vec4(1.0, 1.0, 1.0, 1.0),
                            shininess
                        );

                        material back_material = material(
                            vec4(1.0, 1.0, 1.0, 1.0),
                            backColor,
                            vec4(1.0, 1.0, 1.0, 1.0),
                            0
                        );

                        void main(void)
                        {
                            mat4 mvp = projection_matrix*view_matrix*model_matrix;
                            vec3 normal_direction = normalize(normal_matrix * normals);
                            vec4 view_position = view_matrix_inv * vec4(0.0, 0.0, 0.0, 1.0);
                            vec3 view_direction = normalize(vec3(view_position - model_matrix * vertices));
                            vec3 light_direction;
                            float attenuation;

                            light0.position = view_position;
                            if (light0.position.w == 0.0) // directional light
                            {
                                attenuation = 1.0; // no attenuation
                                light_direction = normalize(vec3(light0.position));
                            }
                            else // point or spot light (or other kind of light)
                            {
                                vec3 vertex_to_light_source = vec3(light0.position - model_matrix * vertices);
                                float distance = length(vertex_to_light_source);
                                light_direction = normalize(vertex_to_light_source);
                                attenuation = 1.0 / (light0.constant_attenuation
                                + light0.linear_attenuation * distance
                                + light0.quadratic_attenuation * distance * distance);
                                if (light0.spot_cutoff <= 90.0) // spotlight
                                {
                                    float clamped_cosine = max(0.0, dot(-light_direction, normalize(light0.spot_direction)));
                                    if (clamped_cosine < cos(radians(light0.spot_cutoff))) // outside of spotlight cone
                                    {
                                        attenuation = 0.0;
                                    }
                                    else
                                    {
                                        attenuation = attenuation * pow(clamped_cosine, light0.spot_exponent);
                                    }
                                }
                            }

                            // Computation of lighting for front faces

                            vec3 ambient_lighting = vec3(scene_ambient) * vec3(front_material.ambient);

                            vec3 diffuse_reflection = attenuation
                            * vec3(light0.diffuse) * vec3(front_material.diffuse)
                                * max(0.0, dot(normal_direction, light_direction));

                            vec3 specular_reflection;
                            if (dot(normal_direction, light_direction) < 0.0) // light source on the wrong side?
                                    {
                                specular_reflection = vec3(0.0, 0.0, 0.0); // no specular reflection
                                    }
                            else // light source on the right side
                            {
                                specular_reflection = attenuation * vec3(light0.specular) * vec3(front_material.specular)
                                * pow(max(0.0, dot(reflect(-light_direction, normal_direction), view_direction)),
                                    front_material.shininess);
                            }

                            front_color = vec4(ambient_lighting + diffuse_reflection + specular_reflection, front_material.diffuse.w);

                            // Computation of lighting for back faces (uses negative normal_direction and back material colors)

                            vec3 back_ambient_lighting = vec3(scene_ambient) * vec3(back_material.ambient);

                            vec3 back_diffuse_reflection = attenuation
                            * vec3(light0.diffuse) * vec3(back_material.diffuse)
                                * max(0.0, dot(-normal_direction, light_direction));

                            back_color = vec4(back_ambient_lighting + back_diffuse_reflection, back_material.diffuse.w);

                            gl_Position = mvp * vertices;
                        }
        "
        fragmentShader:
        "
                        #version 410
                        in vec4 front_color;
                        in vec4 back_color;
                        layout(location = 0) out vec4 frag_color;
                        layout(location = 1) out vec4 frag_color_copy;
                        void main()
                        {
                            if (gl_FrontFacing) // is the fragment part of a front face?
                            {
                                frag_color = front_color;
                            }
                            else // fragment is part of a back face
                            {
                                frag_color = back_color;
                            }
                            frag_color_copy = frag_color;
                        }
        "
    }