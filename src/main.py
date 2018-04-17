# IF3260: Computer Graphics
# Camera 3D Modelling

# --Libraries and Packages--
import sys

from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

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

# Lighting
def renderLight():
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHTING)

	glEnable(GL_DEPTH_TEST)
	glDepthFunc(GL_LEQUAL)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	
	glShadeModel(GL_SMOOTH)
	
	glEnable(GL_COLOR_MATERIAL)
	glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
	glEnable(GL_TEXTURE_2D)
	
	specReflection = [1.0, 1.0, 1.0, 1.0]
	glMaterialfv(GL_FRONT, GL_SPECULAR, specReflection)
	glMateriali(GL_FRONT, GL_SHININESS, 30)
	glLightfv(GL_LIGHT0, GL_POSITION, [2.0, 2.0, 2.0, 1.0])

# Scene to be Render
def renderScene():
	global x, z, dX, dZ, angle
	#Clear Color and Depth Buffers
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	#Reset transformations
	glLoadIdentity()
	
	renderLight()
	
	camera.apply()
	camera.rotate(xrot*0.001, 0.0, 0.0)
	camera.rotate(0, yrot*0.001, 0.0)
	# Draw Sphere
	glPushMatrix()
	glutSolidCube(1.5)
	glPopMatrix()

	idle()
	glutSwapBuffers()

def changeSize(w, h):
	#Prevent a divide by zero, when window is too short
	#(you cant make a window of zero width).
	if (h == 0):
		h = 1
	ratio = w * 1.0 / h

	#Use the Projection Matrix
	glMatrixMode(GL_PROJECTION)

	#Reset Matrix
	glLoadIdentity()

	#Set the viewport to be the entire window
	glViewport(0, 0, w, h)

	#Set the correct perspective.
	gluPerspective(45.0, ratio, 0.1, 100.0)

	#Get Back to the Modelview
	glMatrixMode(GL_MODELVIEW)
	
def loadTexture(filename):
	#texture
	texture = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, texture)

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

	img = Image.open(filename)
	data = numpy.array(list(img.getdata()), dtype=numpy.int64)
	print(len(data))
	width = 1000
	height = 1000
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
	glGenerateMipmap(GL_TEXTURE_2D)

	return texture

def main():

	#init GLUT and create window
	glutInit()
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
	glutInitWindowPosition(100,100)
	glutInitWindowSize(800,600)
	glutCreateWindow(b'IF3260: Computer Graphics')

	glMatrixMode(GL_PROJECTION)
	gluPerspective(60, 1, 1.0, 1000.0)
	glMatrixMode(GL_MODELVIEW)
	
	#register callbacks
	glutDisplayFunc(renderScene)
	glutReshapeFunc(changeSize)
	glutIdleFunc(renderScene)
	#glutKeyboardFunc(processNormalKeys)
	glutSpecialFunc(processSpecialKeys)
	
	#Mouse Function
	glutMouseFunc(mouse)
	glutMotionFunc(mouseMotion)

	#OpenGL init
	glEnable(GL_DEPTH_TEST)

	#enter GLUT event processing cycle
	glutMainLoop()
	
main()