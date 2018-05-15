from math import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import sys

#Datatypes
class PARTICLES:
    Xpos = 0.0
    Ypos = 0.0
    Zpos = 0.0
    Xmov = 0.0
    Red = 0.0
    Green = 0.0
    Blue = 0.0
    Direction = 0.0
    Acceleration = 0.0
    Deceleration = 0.0
    Scalez = 0.0
    Visible = False

#Variables
texture = []
ParticleCount = 70
Particle = [PARTICLES() for i in range(0,ParticleCount-1)]
n = 0
def square ():
    glBindTexture(GL_TEXTURE_2D, texture[0])
    
    glBegin(GL_QUADS)
    glTexCoord2d(0.0,0.0)
    glVertex2d(-1.0,-1.0)
    glTexCoord2d(1.0,0.0)
    glVertex2d(1.0,-1.0)
    glTexCoord2d(1.0,1.0)
    glVertex2d(1.0,1.0)
    glTexCoord2d(0.0,1.0)
    glEnd()

def glCreateParticles():
    if(Particle != None):
        for i in range(0,ParticleCount-1):
            Particle[i].Xpos = 0
            Particle[i].Ypos = -5
            Particle[i].Zpos = -5
            Particle[i].Xmov = (((((( (2 - 1 + 1) * random.random()%11) + 1) - 1 + 1) *random.random()%11) + 1) * 0.005) - (((((((2 - 1 + 1) * random.random()%11) + 1) - 1 + 1) * random.random()%11) + 1) * 0.005)
            Particle[i].Zmov = (((((((2 - 1 + 1) * random.random()%11) + 1) - 1 + 1) * random.random()%11) + 1) * 0.005) - (((((((2 - 1 + 1) * random.random()%11) + 1) - 1 + 1) * random.random()%11) + 1) * 0.005)
            Particle[i].Red = 1
            Particle[i].Green = 1
            Particle[i].Blue = 1
            Particle[i].Scalez = 0.25
            Particle[i].Direction = 0
            Particle[i].Acceleration = 0.05
            #Particle[i].Acceleration = ((((((8 - 5 + 2) * random.random()%11) + 5) - 1 + 1) * random.random()%11) + 1) * 0.01
            Particle[i].Deceleration = 0.0025

def glUpdateParticles():
    global n

    if(n > ParticleCount-1):
        n = ParticleCount-1

    for i in range(0,n):
        glColor3f (Particle[i].Red, Particle[i].Green, Particle[i].Blue)

        Particle[i].Ypos = Particle[i].Ypos + Particle[i].Xmov
        # Particle[i].Deceleration = Particle[i].Deceleration + 0.0025

        Particle[i].Xpos = Particle[i].Xpos + Particle[i].Acceleration - Particle[i].Deceleration
        Particle[i].Zpos = Particle[i].Zpos + Particle[i].Zmov

        Particle[i].Direction = Particle[i].Direction + ((((((0.5 - 0.1 + 0.1) * random.random()%11) + 1) - 1 + 1) * random.random()%11) + 1)

        Particle[i].Scalez+=0.001
        if (Particle[i].Xpos < -5 or Particle[i].Xpos > 10):
            Particle[i].Xpos = 0
            Particle[i].Ypos = -5
            Particle[i].Zpos = -5
            Particle[i].Red = 1
            Particle[i].Green = 1
            Particle[i].Blue = 1
            Particle[i].Direction = 0
            Particle[i].Scalez = 0.25
            Particle[i].Acceleration = 0.05
            #Particle[i].Acceleration = ((((((8 - 5 + 2) * random.random()%11) + 5) - 1 + 1) * random.random()%11) + 1) * 0.01
            Particle[i].Deceleration = 0.0025

    n+=1
	
def glDrawParticles():
    for i in range(0,ParticleCount-1):
        glPushMatrix()
        

        glTranslatef (Particle[i].Xpos, Particle[i].Ypos, Particle[i].Zpos)
        glRotatef (Particle[i].Direction - 10, 0, 0, 1)
    
        glScalef (Particle[i].Scalez, Particle[i].Scalez, Particle[i].Scalez)
        
        glDisable (GL_DEPTH_TEST)
        glEnable (GL_BLEND)
        
            
        #glBlendFunc (GL_DST_COLOR, GL_ZERO)
        
        glBindTexture (GL_TEXTURE_2D, int(texture[0]))
        

        glBegin (GL_QUADS)
        glTexCoord2d (0, 0)
        glVertex3f (-1, -1, 0)
        glTexCoord2d (1, 0)
        glVertex3f (1, -1, 0)
        glTexCoord2d (1, 1)
        glVertex3f (1, 1, 0)
        glTexCoord2d (0, 1)
        glVertex3f (-1, 1, 0)
        glEnd()
        
        glBlendFunc (GL_ONE, GL_ONE)
        glBindTexture (GL_TEXTURE_2D, int(texture[1]))
        
        glBegin (GL_QUADS)
        glTexCoord2d (0, 0)
        glVertex3f (-1, -1, 0)
        glTexCoord2d (1, 0)
        glVertex3f (1, -1, 0)
        glTexCoord2d (1, 1)
        glVertex3f (1, 1, 0)
        glTexCoord2d (0, 1)
        glVertex3f (-1, 1, 0)
        glEnd()
        
            
        glEnable(GL_DEPTH_TEST)

        glPopMatrix()

def display():
    glClearDepth (1)
    glClearColor (0.0,0.0,0.0,1.0)
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef (0,0,-10)
    glUpdateParticles()
    glDrawParticles()
    glutSwapBuffers()

def init():
    glEnable( GL_TEXTURE_2D )
    glEnable(GL_DEPTH_TEST)

    glCreateParticles()

    #temp, x, y = loadImage("Smoke10.png")
	
    temp_texture_mask = float(LoadTextureRAW("particle_mask.raw",256,256)) #load our texture
    texture.append(temp_texture_mask)
    temp_texture = float(LoadTextureRAW("particle.raw",256,256)) #load our texture
    texture.append(temp_texture)

def reshape(w,h):
    glViewport (0, 0,w ,h )
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()
    gluPerspective (60, w / h, 1.0, 100.0)
    glMatrixMode (GL_MODELVIEW)
    # glLoadIdentity ()

def main():
    # glutInit(len(sys.argv),sys.argv)
    glutInit()
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize (500, 500)
    glutInitWindowPosition (100, 100)
    glutCreateWindow (b"A basic OpenGL Window")
    init()
    glutDisplayFunc (display)
    glutIdleFunc (display)
    glutReshapeFunc (reshape(500,500))
    glutMainLoop ()
    print("nyahaha")
    return

#function to load the RAW file

def LoadTextureRAW(filename,width,height):
    # GLuint texture;
    # unsigned char * data;
    # FILE * file;
    file = open( filename, "rb" )
    if ( file == None ): 
        return 0

    data = file.read()
    # data = (unsigned char *)malloc( width * height * 3 );

    # fread( data, width * height * 3, 1, file );
    file.close()
    
    texture = 0
    glGenTextures(1, texture)            

    glBindTexture(GL_TEXTURE_2D, texture)

    glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexEnvi( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE )

    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_NEAREST )

    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,GL_LINEAR )

    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, width, height, GL_RGB, GL_UNSIGNED_BYTE, data)
    
    # free( data )

    return texture

def loadImage(filename):
    image = Image.open(filename)
    ix = image.size[0]
    iy = image.size[1]
    data = numpy.array(list(image.getdata()),  dtype=numpy.int64)

    return data, ix, iy

def loadTexture(data, ix, iy):
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

def FreeTexture(texture):
    glDeleteTextures(1,texture)

main()
