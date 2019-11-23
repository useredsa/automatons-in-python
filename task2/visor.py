#!/usr/bin/python3
# -----------------------------------------------------------------------------
# Este script emplea parte del código de ejemplo de Nicolas P. Rougier.
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo, log
from glumpy.transforms import Trackball, Position

vertex = """
uniform mat4 m_model;
uniform mat4 m_view;
uniform mat4 m_normal;
attribute vec3 position;
attribute vec3 normal;
varying vec3 v_normal;
varying vec3 v_position;

void main()
{
    gl_Position = <transform>;
    vec4 P = m_view * m_model* vec4(position, 1.0);
    v_position = P.xyz / P.w;
    v_normal = vec3(m_normal * vec4(normal,0.0));
}
"""

fragment = """
varying vec3 v_normal;
varying vec3 v_position;

const vec3 light_position = vec3(1.0,1.0,1.0);
const vec3 ambient_color = vec3(0.0, 0.0, 0.1);
const vec3 diffuse_color = vec3(0.125, 0.125, 0.75);
const vec3 specular_color = vec3(1.0, 1.0, 1.0);
const float shininess = 128.0;
const float gamma = 2.2;

void main()
{
    vec3 normal= normalize(v_normal);
    vec3 light_direction = normalize(light_position - v_position);
    float lambertian = max(dot(light_direction,normal), 0.0);
    float specular = 0.0;
    if (lambertian > 0.0)
    {
        vec3 view_direction = normalize(-v_position);
        vec3 half_direction = normalize(light_direction + view_direction);
        float specular_angle = max(dot(half_direction, normal), 0.0);
        specular = pow(specular_angle, shininess);
    }
    vec3 color_linear = ambient_color +
                        lambertian * diffuse_color +
                        specular * specular_color;
    vec3 color_gamma = pow(color_linear, vec3(1.0/gamma));
    gl_FragColor = vec4(color_gamma, 1.0);
}
"""

obj = gloo.Program(vertex, fragment)
window = app.Window(width=640, height=480, color=(0.1,0.1,0.1,1.0))

def update():
    model = obj['transform']['model'].reshape(4,4)
    view  = obj['transform']['view'].reshape(4,4)
    obj['m_view']  = view
    obj['m_model'] = model
    obj['m_normal'] = np.array(np.matrix(np.dot(view, model)).I.T)
    
@window.event
def on_draw(dt):
    window.clear()
    obj.draw(gl.GL_TRIANGLES)

@window.event
def on_mouse_drag(x, y, dx, dy, button):
    update()
    
@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)
    update()

def mostrar(V,T,N,F_V,F_T,F_N):
    # Building the vertices
    V = np.array(V)
    F_V = np.array(F_V)
    vtype = [('position', np.float32, 3)]
    
    if len(N):
        N = np.array(N)
        F_N = np.array(F_N)
        vtype.append(('normal', np.float32, 3))
        
    vertices = np.empty(len(F_V),vtype)
    vertices["position"] = V[F_V,:3]
    if len(N) and len(F_N):
        vertices["normal"] = N[F_N]
    vertices = vertices.view(gloo.VertexBuffer)

    # Centering and scaling to fit the unit box
    xmin,xmax = vertices["position"][:,0].min(), vertices["position"][:,0].max()
    ymin,ymax = vertices["position"][:,1].min(), vertices["position"][:,1].max()
    zmin,zmax = vertices["position"][:,2].min(), vertices["position"][:,2].max()
    vertices["position"][:,0] -= (xmax+xmin)/2.0
    vertices["position"][:,1] -= (ymax+ymin)/2.0
    vertices["position"][:,2] -= (zmax+zmin)/2.0
    scale = max(max(xmax-xmin,ymax-ymin), zmax-zmin) / 2.0
    vertices["position"] /= scale

    obj.bind(vertices)
    trackball = Trackball(Position("position"))
    obj['transform'] = trackball
    trackball.theta, trackball.phi, trackball.zoom = 90,0,18 
    window.attach(obj['transform'])
    app.run()
