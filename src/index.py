# IF3260: Computer Graphics
# Texture Mapping - Immediate

# --Libraries and Packages--
import sys
import random
import numpy
import _thread
import tkinter
from math import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from tkinter import *
from PIL import Image

# --Constant and Global Variables--
# --Particles Settings--
MAX_PARTICLES = 1000

slowdown = 2.0
velocity = 0.0
zoom = -40.0
pan = 0.0
tilt = 0.0
accum = -10.0

# --Camera Settings--
# Camera Angle
angle = 0.0

# Camera Coordinate
x = 0.0
y = 0.0
z = 0.0

# Camera Direction
dx = 0.0
dy = 0.0
dz = 0.0

# --Mouse Settings--
xrot = 0.0
yrot = 0.0
 
xdiff = 0.0
ydiff = 0.0

mouseDown = False

# Texture
data = []
dim1 = []
dim2 = []

# Lighting
spec = 1.0

ambient = 1.0

diffuse = 1.0

shine = 10.0


# --CLASSES--
class Particles:
	# Life
	alive = False	# Is the particle alive
	life = 0.0		# Particle lifespan
	fade = 0.0 		# Decay
	# Color
	red = 0.0
	green = 0.0
	blue = 0.0
	# Position/direction
	xPos = 0.0
	yPos = 0.0
	zPos = 0.0
	# Velocity/Direction, only goes down in y dir
	vel = 0.0
	# Gravity
	gravity = 0.0

class Camera:
	def __init__(self):
		self.position = (0.0, 0.0, 0.0)
		self.rotation = (0.0, 0.0, 0.0)
		
	def translate(self, dx, dy, dz):
		x, y, z = self.position
		self.position = (x + dx, y + dy, z + dz)
		
	def rotate(self, dx, dy, dz):
		x, y, z = self.rotation
		self.rotation = (x + dx, y + dy, z + dz)
		
	def apply(self):
		glTranslate(*self.position)
		glRotated(self.rotation[0], -1, 0, 0)
		glRotated(self.rotation[1], 0, -1, 0)
		glRotated(self.rotation[2], 0, 0, -1)

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

# Invoke Class
camera = Camera()
particle = [Particles() for i in range(0,MAX_PARTICLES)]
texture = []
ParticleCount = 100
Particle = [PARTICLES() for i in range(0,ParticleCount-1)]
n = 0

# Key Processing Unit
def processNormalKeys(key, x, y):
	if (key == 27):
		exit(0)

def processSpecialKeys(key, xx, yy):
	global x, z, dX, dZ, angle
	fraction = 0.1
	movespeed = 1
	
	if (key == GLUT_KEY_LEFT):
		camera.translate(movespeed, 0, 0)
	elif (key == GLUT_KEY_RIGHT):
		camera.translate(-movespeed, 0, 0)
	elif (key == GLUT_KEY_UP):
		camera.translate(0, -movespeed, 0)
	elif (key == GLUT_KEY_DOWN):
		camera.translate(0, movespeed, 0)
	elif (key == GLUT_KEY_PAGE_UP):
		camera.translate(0, 0, movespeed)
	elif (key == GLUT_KEY_PAGE_DOWN):
		camera.translate(0, 0, -movespeed)

# Mouse Processing Unit
def mouseMotion(x, y):
	global yrot, xrot, mouseDown
	if (mouseDown):
		yrot = - x + xdiff
		xrot = - y - ydiff
		
def mouse(button, state, x, y):
	global xdiff, ydiff, mouseDown
	if (button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
		mouseDown = True
		xdiff = x + yrot
		ydiff = -y - xrot
	else:
		mouseDown = False

def idle():
	global mouseDown, xrot, yrot
	if (not mouseDown):
		
		if(xrot > 1):
			xrot -= 0.005 * xrot
		elif(xrot < -1):
			xrot += 0.005 * -xrot 
		else:
			xrot = 0

		if(yrot > 1):
			yrot -= 0.005 * yrot
		elif(yrot < -1):
			yrot += 0.005 * -yrot
		else:
			yrot = 0			

# Rain Particle System
def initParticles(i):
	particle[i].alive = True
	particle[i].life = 1.0
	particle[i].fade = (random.random() %100) /1000.0 +0.003

	particle[i].xPos = random.randint(-20,20)
	particle[i].yPos = random.randint(5,10)
	particle[i].zPos = random.randint(20,60)

	particle[i].red = 0.5
	particle[i].green = 0.5
	particle[i].blue = 1.0

	particle[i].vel = velocity
	particle[i].gravity = -(random.uniform(1.0,2.0))
	
def init():
	glShadeModel(GL_SMOOTH)
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glClearDepth(1.0)
	glEnable(GL_DEPTH_TEST)

	# Initialize particles
	for loop in range(0, MAX_PARTICLES):
		initParticles(loop)
		
def drawRain():
	loadTexture(data[0],dim1[0],dim1[1])
	glEnable(GL_TEXTURE_2D)
	for loop in range(0, MAX_PARTICLES, 2):
		if (particle[loop].alive == True):
			x = particle[loop].xPos
			y = particle[loop].yPos
			z = particle[loop].zPos + zoom

			# Draw particles
			glColor3f(0.5, 0.5, 1.0)
			glBegin(GL_LINES)
			glVertex3f(x, y, z)
			glVertex3f(x, y+0.5, z)
			glEnd()

			# Update values
			# Move
			# Adjust slowdown for speed!
			particle[loop].yPos += particle[loop].vel / (slowdown*10)
			particle[loop].vel += particle[loop].gravity
			# Decay
			particle[loop].life -= particle[loop].fade

			if (particle[loop].yPos <= 0):
				particle[loop].life = -1.0
			# Revive
			if (particle[loop].life < 0.0):
				initParticles(loop)
	glDisable(GL_TEXTURE_2D)

# Lighting
def renderLight():
	global spec
	global ambient
	global diffuse
	global shine
	
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHTING)

	glEnable(GL_DEPTH_TEST)
	glDepthFunc(GL_LEQUAL)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	
	glShadeModel(GL_SMOOTH)
	
	glEnable(GL_TEXTURE_2D)
	
	specReflection = [spec, spec, spec]
	glLightfv(GL_LIGHT0, GL_POSITION, [4.0, 4.0, 4.0, 1.0])
	mat_specular = [ 1.0, 1.0, 1.0, 1.0 ]
	mat_shininess = [shine]
	glMaterialfv(GL_FRONT, GL_SPECULAR, specReflection)
	glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
	glMaterialfv(GL_FRONT, GL_AMBIENT, [ambient, ambient, ambient, 1.0])
	glMaterialfv(GL_FRONT, GL_DIFFUSE, [diffuse, diffuse, diffuse, 1.0])

def displaySmoke():
	for i in range(0,ParticleCount-1):
		glEnable(GL_DEPTH_TEST)
		glPushMatrix()

		glTranslatef (Particle[i].Xpos, Particle[i].Ypos, Particle[i].Zpos)
		glRotatef (Particle[i].Direction - 10, 0, 0, 1)

		glScalef (Particle[i].Scalez, Particle[i].Scalez, Particle[i].Scalez)

		glEnable (GL_BLEND)
		glBlendFunc (GL_DST_COLOR, GL_ZERO)

		s = 0.3
		glBegin (GL_QUADS)
		glColor3f(50,50,50)
		glVertex3f (-s, -s, s)
		glVertex3f (s, -s, s)
		glVertex3f (s, s, s)
		glVertex3f (-s, s, s)
		glEnd()

		glBegin (GL_QUADS)
		glVertex3f (-s, -s, -s)
		glVertex3f (s, -s, -s)
		glVertex3f (s, s, -s)
		glVertex3f (-s, s, -s)
		glEnd()

		glBegin (GL_QUADS)
		glVertex3f (-s, s, s)
		glVertex3f (-s, s, -s)
		glVertex3f (s, s, -s)
		glVertex3f (s, s, s)
		glEnd()

		glBegin (GL_QUADS)
		glVertex3f (-s, -s, s)
		glVertex3f (-s, -s, -s)
		glVertex3f (s, -s, -s)
		glVertex3f (s, -s, s)
		glEnd()

		glBegin (GL_QUADS)
		glVertex3f (s, -s, s)
		glVertex3f (s, s, s)
		glVertex3f (s, s, -s)
		glVertex3f (s, -s, -s)
		glEnd()

		glBegin (GL_QUADS)
		glVertex3f (-s, -s, s)
		glVertex3f (-s, s, s)
		glVertex3f (-s, s, -s)
		glVertex3f (-s, -s, -s)
		glEnd()

		glBlendColor(30/256,30/256,30/256,256/256)
		glBlendFunc (GL_CONSTANT_COLOR, GL_CONSTANT_COLOR)

		glBegin (GL_QUADS)
		glVertex3f (-s, -s, s)
		glVertex3f (s, -s, s)
		glVertex3f (s, s, s)
		glVertex3f (-s, s, s)
		glEnd()

		glBegin (GL_QUADS)
		glVertex3f (-s, -s, -s)
		glVertex3f (s, -s, -s)
		glVertex3f (s, s, -s)
		glVertex3f (-s, s, -s)
		glEnd()

		glBegin (GL_QUADS)
		glVertex3f (-s, s, s)
		glVertex3f (-s, s, -s)
		glVertex3f (s, s, -s)
		glVertex3f (s, s, s)
		glEnd()

		glBegin (GL_QUADS)
		glVertex3f (-s, -s, s)
		glVertex3f (-s, -s, -s)
		glVertex3f (s, -s, -s)
		glVertex3f (s, -s, s)
		glEnd()

		glBegin (GL_QUADS)
		glVertex3f (s, -s, s)
		glVertex3f (s, s, s)
		glVertex3f (s, s, -s)
		glVertex3f (s, -s, -s)
		glEnd()

		glBegin (GL_QUADS)
		glVertex3f (-s, -s, s)
		glVertex3f (-s, s, s)
		glVertex3f (-s, s, -s)
		glVertex3f (-s, -s, -s)
		glEnd()
		
		glDisable(GL_BLEND)
		
		glPopMatrix()

def LoadTextureRAW(filename,width,height):
	file = open( filename, "rb" )
	if ( file == None ): 
		return 0

	data = file.read()
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

	return texture

# Terrain
def drawTerrain():
	global data
	z = 1.5
	
	loadTexture(data[6], dim1[12], dim1[13])
	glEnable(GL_TEXTURE_2D)
	for i in range(-2,2):
		for j in range(-2,2):
			glBegin(GL_QUADS)
			glTexCoord2f(0.0, 0.0); glVertex3f(0.0+i*10, -1.65, 0.0+j*10)
			glTexCoord2f(1.0, 0.0); glVertex3f(10.0+i*10, -1.65, 0.0+j*10)
			glTexCoord2f(1.0, 1.0); glVertex3f(10.0+i*10, -1.65, 10.0+j*10)
			glTexCoord2f(0.0, 1.0); glVertex3f(0.0+i*10, -1.65, 10.0+j*10)
			glEnd()
	glDisable(GL_TEXTURE_2D)

def drawCar():
	global data
	z = 1.5 

	# Road
	loadTexture(data[2],dim1[4],dim1[5])
	glEnable(GL_TEXTURE_2D)
	glColor3f(206/255, 20/255, 55/255)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-20.0, -1.6, -z -3.0)
	glTexCoord2f(1.0, 0.0); glVertex3f(20.0, -1.6, -z -3.0)
	glTexCoord2f(1.0, 1.0); glVertex3f(20.0, -1.6, z + 3.0) 
	glTexCoord2f(0.0, 1.0); glVertex3f(-20.0, -1.6, z + 3.0)
	glEnd()
	glDisable(GL_TEXTURE_2D)

	loadTexture(data[0],dim1[0],dim1[1])
	#back window frame
	
	glEnable(GL_TEXTURE_2D)
	glColor3f(206/255, 20/255, 55/255)
	glBegin(GL_QUADS)
	glNormal3f(1.0,1.0,1.0)	
	glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, 0.25, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(-3.0, 0.25, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(-3.0, -1.0, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, -1.0, -z)
	glEnd()

	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, 1.5, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(-3.0, 1.5, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(-3.0, 1.0, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 1.0, -z)
	glEnd()

	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, 0.25, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(-3.0, 0.25, -z+0.5)
	glTexCoord2f(1.0, 1.0); glVertex3f(-3.0, 1.0, -z+0.5)
	glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 1.0, -z)
	glEnd()

	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, 0.25, z-0.5)
	glTexCoord2f(1.0, 0.0); glVertex3f(-3.0, 0.25, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(-3.0, 1.0, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 1.0, z-0.5)
	glEnd()

	#top
	glColor3f(240/255, 20/255, 55/255)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, 1.5, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(-3.0, 1.5, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(0.6, 1.5, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(0.6, 1.5, -z)
	glEnd()

	#bottom
	glColor3f(190/255, 20/255, 55/255)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, -1.0, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(-3.0, -1.0, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(3.0, -1.0, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(3.0, -1.0, -z)
	glEnd()

	#front
	glColor3f(206/255, 20/255, 55/255)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(3.0, -1.0, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(3.0, 0.15, -z)
	glTexCoord2f(1.0, 1.0); glVertex3f(3.0, 0.15, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(3.0, -1.0, z)
	glEnd()

	#front cover
	glColor3f(230/255, 20/255, 55/255)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(3.0, 0.15, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(1.2, 0.25, -z)
	glTexCoord2f(1.0, 1.0); glVertex3f(1.2, 0.25, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(3.0, 0.15, z)
	glEnd()

	#front window frame
	glColor3f(235/255, 20/255, 55/255)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(0.6, 1.5, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(0.6, 1.5, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(0.65, 1.42, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(0.65, 1.42, -z)

	glTexCoord2f(0.0, 0.0); glVertex3f(1.15, 0.34, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(1.15, 0.34, -z+0.1)
	glTexCoord2f(1.0, 1.0); glVertex3f(0.65, 1.42, -z+0.1)
	glTexCoord2f(0.0, 1.0); glVertex3f(0.65, 1.42, -z)

	glTexCoord2f(0.0, 0.0); glVertex3f(1.15, 0.34, z)
	glTexCoord2f(1.0, 0.0); glVertex3f(1.15, 0.34, z-0.1)
	glTexCoord2f(1.0, 1.0); glVertex3f(0.65, 1.42, z-0.1)
	glTexCoord2f(0.0, 1.0); glVertex3f(0.65, 1.42, z)

	glTexCoord2f(0.0, 0.0); glVertex3f(1.15, 0.34, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(1.15, 0.34, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(1.2, 0.25, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(1.2, 0.25, -z)
	glEnd()

	#left above (window frame part)
	glColor3f(206/255, 20/255, 55/255)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, 1.5, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(0.6, 1.5, -z)
	glTexCoord2f(1.0, 1.0); glVertex3f(0.696, 1.3, -z)
	glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 1.3, -z)
	glEnd()

	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, 1.3, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(-3.0, 0.25, -z)
	glTexCoord2f(1.0, 1.0); glVertex3f(-2.5, 0.25, -z)
	glTexCoord2f(0.0, 1.0); glVertex3f(-2.5, 1.3, -z)
	glEnd()

	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.2, 1.3, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(-1.2, 0.25, -z)
	glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, 0.25, -z)
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, 1.3, -z)
	glEnd()

	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(1.2, 0.25, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(0.696, 1.3, -z)
	glTexCoord2f(1.0, 1.0); glVertex3f(0.496, 1.3, -z)
	glTexCoord2f(0.0, 1.0); glVertex3f(1.0, 0.25, -z)
	glEnd()

	#left back
	glBegin(GL_POLYGON)
	glTexCoord2f(0.0, 0.0); glVertex3f(1.2, 0.25, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(1.2, -1.0, -z)
	glTexCoord2f(1.0, 1.0); glVertex3f(-3.0, -1.0, -z)
	glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 0.25, -z)
	glEnd()

	#left front
	glBegin(GL_POLYGON)
	glTexCoord2f(0.0, 0.0); glVertex3f(1.2, 0.25, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(3.0, 0.15, -z)
	glTexCoord2f(1.0, 1.0); glVertex3f(3.0, -1.0, -z)
	glTexCoord2f(0.0, 1.0); glVertex3f(1.2, -1.0, -z)
	glEnd()

	#right above (window frame part)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, 1.5, z)
	glTexCoord2f(1.0, 0.0); glVertex3f(0.6, 1.5, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(0.696, 1.3, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 1.3, z)
	glEnd()

	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, 1.3, z)
	glTexCoord2f(1.0, 0.0); glVertex3f(-3.0, 0.25, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(-2.5, 0.25, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(-2.5, 1.3, z)
	glEnd()

	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.2, 1.3, z)
	glTexCoord2f(1.0, 0.0); glVertex3f(-1.2, 0.25, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, 0.25, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, 1.3, z)
	glEnd()

	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(1.2, 0.25, z)
	glTexCoord2f(1.0, 0.0); glVertex3f(0.696, 1.3, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(0.496, 1.3, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(1.0, 0.25, z)
	glEnd()

	#right back
	glBegin(GL_POLYGON)
	glTexCoord2f(0.0, 0.0); glVertex3f(1.2, 0.25, z)
	glTexCoord2f(1.0, 0.0); glVertex3f(1.2, -1.0, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(-3.0, -1.0, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 0.25, z)
	glEnd()

	#right front
	glBegin(GL_POLYGON)
	glTexCoord2f(0.0, 0.0); glVertex3f(1.2, 0.25, z)
	glTexCoord2f(1.0, 0.0); glVertex3f(3.0, 0.15, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(3.0, -1.0, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(1.2, -1.0, z)
	glEnd()
	glDisable(GL_TEXTURE_2D)

	#lampu
	loadTexture(data[3],dim1[6],dim1[7])
	glEnable(GL_TEXTURE_2D)
	glBegin(GL_QUADS)
	glColor3f(0.9,0.9,0.9)
	glTexCoord2f(0.0, 0.0); glVertex3f(3.006, -0.65, -z+0.101)
	glTexCoord2f(1.0, 0.0); glVertex3f(3.006, -0.35, -z+0.101)
	glTexCoord2f(1.0, 1.0); glVertex3f(3.006, -0.35, -z+0.601)
	glTexCoord2f(0.0, 1.0); glVertex3f(3.006, -0.65, -z+0.601)

	glTexCoord2f(0.0, 0.0); glVertex3f(3.006, -0.65, z-0.101)
	glTexCoord2f(0.0, 1.0); glVertex3f(3.006, -0.35, z-0.101)
	glTexCoord2f(1.0, 1.0); glVertex3f(3.006, -0.35, z-0.601)
	glTexCoord2f(1.0, 0.0); glVertex3f(3.006, -0.65, z-0.601)
	glEnd()
	glDisable(GL_TEXTURE_2D)

	loadTexture(data[5],dim1[10],dim1[11])
	glEnable(GL_TEXTURE_2D)
	glColor3f(0.6,0.2,0.2)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-3.006, -0.65, -z+0.101)
	glTexCoord2f(1.0, 0.0); glVertex3f(-3.006, -0.35, -z+0.101)
	glTexCoord2f(1.0, 1.0); glVertex3f(-3.006, -0.35, -z+0.601)
	glTexCoord2f(0.0, 1.0); glVertex3f(-3.006, -0.65, -z+0.601)

	glTexCoord2f(0.0, 0.0); glVertex3f(-3.006, -0.65, z-0.101)
	glTexCoord2f(0.0, 1.0); glVertex3f(-3.006, -0.35, z-0.101)
	glTexCoord2f(1.0, 1.0); glVertex3f(-3.006, -0.35, z-0.601)
	glTexCoord2f(1.0, 0.0); glVertex3f(-3.006, -0.65, z-0.601)
	glEnd()
	glDisable(GL_TEXTURE_2D)

	glColor3f(0,0,0)
	glBegin(GL_QUADS)	
	glVertex3f(3.006, -0.6, -z+1)
	glVertex3f(3.006, -0.37, -z+1)
	glVertex3f(3.006, -0.37, z-1)
	glVertex3f(3.006, -0.6, z-1)
	#lampu2
	glColor3f(0.6,0.6,0.6)
	glVertex3f(3.005, -0.7, -z)
	glVertex3f(3.005, -0.3, -z)
	glVertex3f(3.005, -0.3, z)
	glVertex3f(3.005, -0.7, z)

	glVertex3f(-3.005, -0.7, -z)
	glVertex3f(-3.005, -0.3, -z)
	glVertex3f(-3.005, -0.3, z)
	glVertex3f(-3.005, -0.7, z)

	glVertex3f(2.9, -0.3, -z-0.0014)
	glVertex3f(3.0, -0.3, -z-0.0014)
	glVertex3f(3.0, -0.7, -z-0.0014)
	glVertex3f(2.9, -0.7, -z-0.0014)

	glVertex3f(2.9, -0.3, z+0.0014)
	glVertex3f(3.0, -0.3, z+0.0014)
	glVertex3f(3.0, -0.7, z+0.0014)
	glVertex3f(2.9, -0.7, z+0.0014)
	glEnd()

	loadTexture(data[4],dim1[7],dim1[8])
	glEnable(GL_TEXTURE_2D)
	glColor3f(226/255, 152/255, 22/255)
	glBegin(GL_QUADS)	
	glTexCoord2f(1.0, 0.0); glVertex3f(2.95, -0.35, z+0.0015)
	glTexCoord2f(1.0, 1.0); glVertex3f(2.985, -0.35, z+0.0015)
	glTexCoord2f(0.0, 1.0); glVertex3f(2.985, -0.65, z+0.0015)
	glTexCoord2f(0.0, 0.0); glVertex3f(2.95, -0.65, z+0.0015)

	glTexCoord2f(1.0, 0.0); glVertex3f(2.95, -0.35, -z-0.0015)
	glTexCoord2f(1.0, 1.0); glVertex3f(2.985, -0.35, -z-0.0015)
	glTexCoord2f(0.0, 1.0); glVertex3f(2.985, -0.65, -z-0.0015)
	glTexCoord2f(0.0, 0.0); glVertex3f(2.95, -0.65, -z-0.0015)
	glEnd()
	glDisable(GL_TEXTURE_2D)
	
	# Car's Wheel
	loadTexture(data[1],dim1[2],dim1[3])
	glEnable(GL_TEXTURE_2D)
	glColor3f(0.0, 0.0, 0.0)
	quadric = gluNewQuadric()
	gluQuadricNormals(quadric, GLU_SMOOTH)
	gluQuadricTexture(quadric, GL_TRUE)
	glTranslatef(1.7,-1.0,-1.7)
	gluCylinder(quadric,0.6,0.6,0.2,15,15)
	gluDisk(quadric, 0, 0.6, 15, 15)
	glTranslatef(0.0,0.0,0.2)
	gluDisk(quadric, 0, 0.6, 15, 15)
	
	glTranslatef(0.0, 0.0, -0.2)
	glTranslatef(-3.3, 0.0, 0.0)
	gluCylinder(quadric,0.6,0.6,0.2,15,15)
	gluDisk(quadric, 0, 0.6, 15, 15)
	glTranslatef(0.0,0.0,0.2)
	gluDisk(quadric, 0, 0.6, 15, 15)
	
	glTranslatef(0.0, 0.0, -0.2)
	glTranslatef(0.0, 0.0, 3.2)
	gluCylinder(quadric,0.6,0.6,0.2,15,15)
	gluDisk(quadric, 0, 0.6, 15, 15)
	glTranslatef(0.0,0.0,0.2)
	gluDisk(quadric, 0, 0.6, 15, 15)
	
	glTranslatef(0.0, 0.0, -0.2)
	glTranslatef(3.3, 0.0, 0.0)
	gluCylinder(quadric,0.6,0.6,0.2,15,15)
	gluDisk(quadric, 0, 0.6, 15, 15)
	glTranslatef(0.0,0.0,0.2)
	gluDisk(quadric, 0, 0.6, 15, 15)
	
	glColor3f(1.0, 1.0, 1.0)
	gluDisk(quadric, 0.2, 0.4, 15, 15)
	glTranslatef(-3.3, 0.0, 0.0)
	gluDisk(quadric, 0.2, 0.4, 15, 15)
	glTranslatef(0.0, 0.0, -0.2)
	glTranslatef(0.0, 0.0, -3.2)
	gluDisk(quadric, 0.2, 0.4, 15, 15)
	glTranslatef(+3.3, 0.0, 0.0)
	gluDisk(quadric, 0.2, 0.4, 15, 15)
	glDisable(GL_TEXTURE_2D)

def glCreateParticles():
	if(Particle != None):
		for i in range(0,ParticleCount-1):
			Particle[i].Xpos = -4.5
			Particle[i].Ypos = 0
			Particle[i].Zpos = 3
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

		Particle[i].Xpos = Particle[i].Xpos - Particle[i].Acceleration + Particle[i].Deceleration
		Particle[i].Zpos = Particle[i].Zpos + Particle[i].Zmov

		Particle[i].Direction = Particle[i].Direction + ((((((0.5 - 0.1 + 0.1) * random.random()%11) + 1) - 1 + 1) * random.random()%11) + 1)

		Particle[i].Scalez+=0.005
		if (Particle[i].Xpos < -8 or Particle[i].Xpos > 10):
			Particle[i].Xpos = -4.5
			Particle[i].Ypos = 0
			Particle[i].Zpos = 3
			Particle[i].Red = 1
			Particle[i].Green = 1
			Particle[i].Blue = 1
			Particle[i].Direction = 0
			Particle[i].Scalez = 0.25
			Particle[i].Acceleration = 0.05
			#Particle[i].Acceleration = ((((((8 - 5 + 2) * random.random()%11) + 5) - 1 + 1) * random.random()%11) + 1) * 0.01
			Particle[i].Deceleration = 0.0025

	n+=2
		
# Initialization
def InitGL(Width, Height): 
 
	glClearColor(0.4, 0.4, 0.9, 1.0)
	glClearDepth(1.0) 
	glDepthFunc(GL_LESS)
	glEnable(GL_DEPTH_TEST)
	glShadeModel(GL_SMOOTH)   
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)
 
	# initialize texture mapping
	glEnable(GL_TEXTURE_2D)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
 
def DrawGLScene():
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
 
	glLoadIdentity()

	renderLight()
	
	camera.apply()
	camera.rotate(xrot*0.001, 0.0, 0.0)
	camera.rotate(0, yrot*0.001, 0.0)
 
	# glBindTexture(GL_TEXTURE_2D, ID)
	# Draw Car
	drawTerrain()
	drawCar()
	drawRain()

	glUpdateParticles()
	displaySmoke()
	# Draw Cube (multiple quads)
	
	idle()
	glutSwapBuffers()


def display():
	glClearDepth (1)
	glClearColor (0.0,0.0,0.0,1.0)
	glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glTranslatef (0,0,-10)
	glUpdateParticles()
	glutSwapBuffers()

def reshape(w,h):
	glViewport (0, 0,w ,h )
	glMatrixMode (GL_PROJECTION)
	glLoadIdentity ()
	gluPerspective (60, w / h, 1.0, 100.0)
	glMatrixMode (GL_MODELVIEW)
	# glLoadIdentity ()

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
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

def idlePost():
	glutPostRedisplay()
	
def main():
	global data, dim1, dim2, thread
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
	glutInitWindowSize(640,480)
	glutInitWindowPosition(200,200)

	window = glutCreateWindow(b'IF3260: Computer Graphics')

	init()
	glCreateParticles()
	glutDisplayFunc(DrawGLScene)
	glutIdleFunc(idlePost)
	glutKeyboardFunc(processNormalKeys)
	glutSpecialFunc(processSpecialKeys)
	
	#Mouse Function
	glutMouseFunc(mouse)
	glutMotionFunc(mouseMotion)
	InitGL(640, 480)
	arr, x, y = loadImage("../img/blue.jpg")
	dim1.append(x)
	dim1.append(y)
	data.append(arr)

	arr2, x2, y2 = loadImage("../img/wheel.jpg")
	dim1.append(x2)
	dim1.append(y2)
	data.append(arr2)

	arr, x, y = loadImage("../img/road.jpg")
	dim1.append(x)
	dim1.append(y)
	data.append(arr)

	arr, x, y = loadImage("../img/lamp.jpg")
	dim1.append(x)
	dim1.append(y)
	data.append(arr)

	arr, x, y = loadImage("../img/yellow.jpg")
	dim1.append(x)
	dim1.append(y)
	data.append(arr)

	arr, x, y = loadImage("../img/mix_lamp.jpg")
	dim1.append(x)
	dim1.append(y)
	data.append(arr)
	
	arr, x, y = loadImage("../img/grass.jpg")
	dim1.append(x)
	dim1.append(y)
	data.append(arr)
	
	glutMainLoop()

def FreeTexture(texture):
	glDeleteTextures(1,texture)

def updateValue(event):
	global spec
	global ambient
	global diffuse
	global shine
	shine = 100 - shine_val.get()
	diffuse = diff.get()/100.0

	spec = spc.get()/100.0

	ambient = amb.get()/100.0

main()
