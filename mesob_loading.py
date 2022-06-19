import glfw
from OpenGL.GL import *
from loader import ShaderLoader
import numpy
import pyrr
from PIL import Image
from loader.ObjLoader import *

def window_resize(window, width, height):
    glViewport(0, 0, width, height)

def main():

    # initialize glfw
    if not glfw.init():
        return

    glfw.window_hint(glfw.RESIZABLE, GL_FALSE)

    window = glfw.create_window(900, 700, "My OpenGL window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)

    obj = ObjLoader()
    obj.load_model("resource/modified.obj")


    shader = ShaderLoader.compile_shader("shaders/vert.vs", "shaders/frag.fs")

    glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
    glBufferData(GL_ARRAY_BUFFER, obj.model.itemsize * len(obj.model), obj.model, GL_STATIC_DRAW)

    #position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, obj.model.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    #texture
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, obj.model.itemsize , ctypes.c_void_p(len(obj.vertex_index)))
    glEnableVertexAttribArray(1)

    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # load image
    image = Image.open("resource/mesob_texture.png")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE,numpy.array(list(image.transpose(Image.FLIP_TOP_BOTTOM).getdata()), numpy.uint8))
    glEnable(GL_TEXTURE_2D)


    glUseProgram(shader)

    glClearColor(0.5, 0.4, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glUniformMatrix4fv(glGetUniformLocation(shader, "view"), 1, GL_FALSE, pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -7.0])))
    glUniformMatrix4fv(glGetUniformLocation(shader, "projection"), 1, GL_FALSE, pyrr.matrix44.create_perspective_projection_matrix(65.0, 800 / 600, 0.1, 100.0))
    glUniformMatrix4fv(glGetUniformLocation(shader, "model"), 1, GL_FALSE, pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0])))



    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time() )

        transformLoc = glGetUniformLocation(shader, "transform")
        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, rot_y)

        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
