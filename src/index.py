# IF3260: Computer Graphics
# Texture Mapping - Immediate

# --Libraries and Packages--
import sys
import numpy
import _thread
from math import *
from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from tkinter import *
from PIL import Image

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

data = []
dim1 = []
dim2 = []

# lighting
spec_r = 1.0
spec_g = 1.0
spec_b = 1.0

ambient_r = 0.0
ambient_g = 0.0
ambient_b = 0.0

diffuse_r = 1.0
diffuse_g = 1.0
diffuse_b = 1.0

shine = 10.0


# --CLASSES--
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
		
camera = Camera()

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

# Slider Thread
def showSlider():
	global spec_r, spec_g, spec_b
	global ambient_r, ambient_g, ambient_b
	global diffuse_r, diffuse_g, diffuse_b
	global shine

	thread = Tk()
	thread.title('Brightness')
	#~ slider = Insert(END, "Set Brightness\n")
	slider = Scale(thread, from_= 0, to = 100, orient = HORIZONTAL)
	slider.pack()
	shine = slider.get()
	print(slider.get())
	#main()
	thread.mainloop()
	#thread.update_idletasks()
	#thread.update()

# Lighting
def renderLight():
	global spec_r, spec_g, spec_b
	global ambient_r, ambient_g, ambient_b
	global diffuse_r, diffuse_g, diffuse_b
	global shine
	
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHTING)

	glEnable(GL_DEPTH_TEST)
	glDepthFunc(GL_LEQUAL)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	
	glShadeModel(GL_SMOOTH)
	
	#glEnable(GL_COLOR_MATERIAL)
	#glColorMaterial(GL_FRONT, GL_DIFFUSE)
	glEnable(GL_TEXTURE_2D)
	
	specReflection = [spec_r, spec_g, spec_b]
	glLightfv(GL_LIGHT0, GL_POSITION, [4.0, 4.0, 4.0, 1.0])
	mat_specular = [ 1.0, 1.0, 1.0, 1.0 ]
	mat_shininess = [shine]
	#~ light_position = [ 1.0, 1.0, 1.0, 0.0 ]
	glMaterialfv(GL_FRONT, GL_SPECULAR, specReflection)
	glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
	glMaterialfv(GL_FRONT, GL_AMBIENT, [ambient_r, ambient_g, ambient_b, 1.0])
	glMaterialfv(GL_FRONT, GL_DIFFUSE, [diffuse_r, diffuse_g, diffuse_b, 1.0])
	#glMaterialfv(GL_FRONT, GL_SPECULAR, specReflection)	
	#glMateriali(GL_FRONT, GL_SHININESS, shine)

def drawCar():
	global data
	z = 1.5 

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
	glBegin(GL_QUADS)
	glColor3f(0.9,0.9,0.9)
	glVertex3f(3.006, -0.65, -z+0.101)
	glVertex3f(3.006, -0.35, -z+0.101)
	glVertex3f(3.006, -0.35, -z+0.601)
	glVertex3f(3.006, -0.65, -z+0.601)

	glVertex3f(3.006, -0.65, z-0.101)
	glVertex3f(3.006, -0.35, z-0.101)
	glVertex3f(3.006, -0.35, z-0.601)
	glVertex3f(3.006, -0.65, z-0.601)
	
	glColor3f(0.6,0.2,0.2)
	glVertex3f(-3.006, -0.65, -z+0.101)
	glVertex3f(-3.006, -0.35, -z+0.101)
	glVertex3f(-3.006, -0.35, -z+0.601)
	glVertex3f(-3.006, -0.65, -z+0.601)

	glVertex3f(-3.006, -0.65, z-0.101)
	glVertex3f(-3.006, -0.35, z-0.101)
	glVertex3f(-3.006, -0.35, z-0.601)
	glVertex3f(-3.006, -0.65, z-0.601)

	glColor3f(0,0,0)
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
	
	glColor3f(226/255, 152/255, 22/255)
	glVertex3f(2.95, -0.35, z+0.0015)
	glVertex3f(2.985, -0.35, z+0.0015)
	glVertex3f(2.985, -0.65, z+0.0015)
	glVertex3f(2.95, -0.65, z+0.0015)

	glVertex3f(2.95, -0.35, -z-0.0015)
	glVertex3f(2.985, -0.35, -z-0.0015)
	glVertex3f(2.985, -0.65, -z-0.0015)
	glVertex3f(2.95, -0.65, -z-0.0015)
	glEnd()
	'''
	#front window glass
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_BLEND)
	glColor4f(90/255, 90/255, 90/255, 0.3)
	glBegin(GL_QUADS)
	glVertex3f(0.65, 1.42, -z)
	glVertex3f(0.65, 1.42, -z)
	glVertex3f(1.15, 0.34, -z)
	glVertex3f(1.15, 0.34, -z)
	glEnd()
	glDisable(GL_BLEND)
		
	#right window glass
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_BLEND)
	glColor4f(90/255, 90/255, 90/255, 0.3)
	glBegin(GL_QUADS)
	glVertex3f(-3.0, 1.5, z-0.01)
	glVertex3f(0.5, 1.5, z-0.01)
	glVertex3f(1.2, 0.25, z-0.01)
	glVertex3f(-3.0, 0.25, z-0.01)
	glEnd()
	glDisable(GL_BLEND)

	#front window glass
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_BLEND)
	glColor4f(90/255, 90/255, 90/255, 0.3)
	glBegin(GL_QUADS)
	glVertex3f(0.5, 1.5, -z)
	glVertex3f(0.5, 1.5, z)
	glVertex3f(1.2, 0.25, z)
	glVertex3f(1.2, 0.25, -z)
	glEnd()
	glDisable(GL_BLEND)

	#back window glass
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_BLEND)
	glColor4f(90/255, 90/255, 90/255, 0.3)
	glBegin(GL_QUADS)
	glVertex3f(-2.99, 0.25, -z+0.5)
	glVertex3f(-2.99, 0.25, z-0.5)
	glVertex3f(-2.99, 1.0, z-0.5)
	glVertex3f(-2.99, 1.0, -z+0.5)
	glEnd()
	glDisable(GL_BLEND)
	'''
	loadTexture(data[1],dim1[2],dim1[3])
	glEnable(GL_TEXTURE_2D)
	# Car's Wheel
	glColor3f(0.0, 0.0, 0.0)
	# quadric = gluNewQuadric()
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

# Initialization
def InitGL(Width, Height): 
 
	glClearColor(0.0, 0.0, 0.0, 0.0)
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
	#global X_AXIS,Y_AXIS,Z_AXIS
	#global DIRECTION
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
 
	glLoadIdentity()

	renderLight()
	
	camera.apply()
	camera.rotate(xrot*0.001, 0.0, 0.0)
	camera.rotate(0, yrot*0.001, 0.0)
 
	# glBindTexture(GL_TEXTURE_2D, ID)
	# Draw Car
	drawCar()
	# Draw Cube (multiple quads)
	'''glBegin(GL_QUADS);
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
	glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
	glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
	glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
	glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0);
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0);
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
	glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0);
	glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0);
	glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
	glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
	glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
	glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
	glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
	glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
	glEnd();
	idle()
	#X_AXIS = X_AXIS - 0.30
	#Z_AXIS = Z_AXIS - 0.30'''
	idle()
	glutSwapBuffers()
 
 
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

thread = Tk()      
def main():
	global data, dim1, dim2, thread
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
	glutInitWindowSize(640,480)
	glutInitWindowPosition(200,200)

	window = glutCreateWindow(b'OpenGL Python Textured Cube')
 
	glutDisplayFunc(DrawGLScene)
	glutIdleFunc(DrawGLScene)
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

	# arr, x, y = loadImage("../img/tes.jpg")
	# dim2.append(x)
	# dim2.append(y)
	# data.append(arr)
	
	glutMainLoop()
	
#if __name__ == "__main__":
	#thread = _thread.start_new_thread(showSlider, ())	
	#showSlider()
	#thread2 = _thread.start_new_thread(main1,())	

def updateValue(event):
	global spec_r, spec_g, spec_b
	global ambient_r, ambient_g, ambient_b
	global diffuse_r, diffuse_g, diffuse_b
	global shine
	shine = 100 - shine_val.get()
	diffuse_r = diff_r.get()/100.0
	diffuse_g = diff_g.get()/100.0
	diffuse_b = diff_b.get()/100.0

	spec_r = spc_r.get()/100.0
	spec_g = spc_g.get()/100.0
	spec_b = spc_b.get()/100.0

	ambient_r = amb_r.get()/100.0
	ambient_g = amb_g.get()/100.0
	ambient_b = amb_b.get()/100.0

thread.title('Brightness')
#~ slider = Insert(END, "Set Brightness\n")
shine_val = Scale(thread, from_= 0, to = 100, orient = HORIZONTAL, command=updateValue)
shine_val.set(0)
shine_val.pack()

diff_r = Scale(thread, from_= 0, to = 100, orient = HORIZONTAL, command=updateValue)
diff_r.set(0)
diff_r.pack()

diff_g = Scale(thread, from_= 0, to = 100, orient = HORIZONTAL, command=updateValue)
diff_g.set(0)
diff_g.pack()

diff_b = Scale(thread, from_= 0, to = 100, orient = HORIZONTAL, command=updateValue)
diff_b.set(0)
diff_b.pack()

spc_r = Scale(thread, from_= 0, to = 100, orient = HORIZONTAL, command=updateValue)
spc_r.set(0)
spc_r.pack()

spc_g = Scale(thread, from_= 0, to = 100, orient = HORIZONTAL, command=updateValue)
spc_g.set(0)
spc_g.pack()

spc_b = Scale(thread, from_= 0, to = 100, orient = HORIZONTAL, command=updateValue)
spc_b.set(0)
spc_b.pack()

amb_r = Scale(thread, from_= 0, to = 100, orient = HORIZONTAL, command=updateValue)
amb_r.set(0)
amb_r.pack()

amb_g = Scale(thread, from_= 0, to = 100, orient = HORIZONTAL, command=updateValue)
amb_g.set(0)
amb_g.pack()

amb_b = Scale(thread, from_= 0, to = 100, orient = HORIZONTAL, command=updateValue)
amb_b.set(0)
amb_b.pack()

#print(slider.get())
_thread.start_new_thread(main, ())
thread.mainloop()
	
