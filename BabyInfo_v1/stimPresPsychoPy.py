############################
#  Import various modules  #
############################
import numpy
import glob, os, random, sys, gc, time

try:
	import winsound

	winSoundLoaded = True
except ImportError:
	print("Warning: winsound can't be imported. Will try to use pyo")
	winSoundLoaded = False
from math import *

try:
	import pygame
	from pygame.locals import *
except ImportError:
	print("Warning: pygame not found; will be using pyglet for stim presentation")

from psychopy import visual, core, event, data, info, prefs


def pollMouse():
	pass


# (x,y) = pygame.mouse.get_pos()
# y = self.experiment.screen.size[1]-y # convert to OpenGL coords
# return [x,y]


def pollMouseCorrected():
	pass


# maxY = self.experiment.screen.size[1]
# (x,y) = pygame.mouse.get_pos()
# y = maxY-y # convert to OpenGL coords
# return [x,y]

def newTextureObject(win, image, position=[0, 0]):
	return visual.SimpleImageStim(win, image=image, units='', pos=position)


def newText(win, text, pos=[0, 0], color="gray", scale=1.0):
	if win.units == "pix":
		height = 30 * scale
		wrapWidth = int(win.size[0] * .8)
	else:  # assumes degree
		height = .7 * scale
		wrapWidth = 30
	return visual.TextStim(win, text=text, pos=pos, color=color, units=win.units, ori=0, height=height)


def randomButNot(arr, index):
	randIndex = index
	while randIndex == index:
		randIndex = random.randint(0, len(arr) - 1)
	return arr[randIndex]


def polarToRect(angleList, radius):
	coords = []
	for curAngle in angleList:
		radAngle = (float(curAngle) * 2.0 * pi) / 360.0
		xCoord = round(float(radius) * cos(radAngle), 0)
		yCoord = round(float(radius) * sin(radAngle), 0)
		coords.append([xCoord, yCoord])
	return coords


def calculateRectangularCoordinates(distanceX, distanceY, numCols, numRows):
	coord = [[0, 0]] * numCols * numRows
	curObj = 0
	for curCol in range(0, numCols):  # x-coord
		for curRow in range(0, numRows):  # y-coord
			coord[curObj] = (curCol * distanceX, curRow * distanceY)
			curObj = curObj + 1
	xCorrect = max(map(lambda x: x[0], coord)) / 2
	yCorrect = max(map(lambda x: x[1], coord)) / 2
	return map(lambda x: [x[0] - xCorrect, x[1] - yCorrect], coord)


def setAndPresentStimulus(win, stimuli, duration=0):
	"""Stimuli can be a list or a single draw-able stimulus"""
	if type(stimuli).__name__ == "list":
		for curStim in stimuli:
			curStim.draw()
	else:
		stimuli.draw()
	if duration == 0:  # single frame
		win.flip()
	else:
		win.flip()
		core.wait(duration)
	return


def setPresentAndWaitForEnter(win, stimuli, inputDevice='keyboard'):
	"""Stimuli can be a list or a single draw-able stimulus"""
	if type(stimuli).__name__ == "list":
		for curStim in stimuli:
			curStim.draw()
	else:
		stimuli.draw()
	win.flip()
	if inputDevice == "keyboard":
		global event
		event.waitKeys(keyList=['return', 'enter'])
	elif inputDevice == "gamepad" or inputDevice == "mouse":
		while True:
			for event in pygame.event.get():  # check responses
				if inputDevice == 'mouse':
					if event.type == pygame.MOUSEBUTTONDOWN:
						pygame.event.clear()
						return
				if event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN:
					pygame.event.clear()
					return


def moveMouseCursor(self, win, startX, startY):
	mouse1 = mouse2 = mouse3 = 0
	self.mouseCursor.setPos([startX, startY])
	while True:
		mouse1, mouse2, mouse3 = self.myMouse.getPressed()
		if (mouse1):
			moved = True
			self.mouseCursor.setPos(self.myMouse.getPos())
			mouse_dX, mouse_dY = self.myMouse.getPos()
			mouse_dX -= startX  # get position relative to the starting position
			mouse_dY -= startY
		self.targetRect.draw()
		self.mouseCursor.draw()
		win.flip()  # redraw the buffer


def newRect(win, size=[0, 0], pos=[0, 0], color="gray"):
	return visual.PatchStim(win, tex='None', texRes=1024, mask='None', color=color, size=size, pos=pos)


def playAndWait(sound, soundPath='', winSound=False, waitFor=-1):
	"""Sound (other than winSound) runs on a separate thread. Waitfor controls how long to pause before resuming. -1 for length of sound"""
	print("Audiolib:", prefs.hardware['audioLib'])

	if not winSoundLoaded:
		winSound = False
	if prefs.hardware['audioLib'] == ['pygame']:
		# default to using winsound
		winSound = True
	if winSound:
		print('using winsound to play sound')
		if waitFor != 0:
			winsound.PlaySound(sound, winsound.SND_MEMORY)
		else:  # playing asynchronously - need to load the path.
			if soundPath:
				winsound.PlaySound(soundPath, winsound.SND_FILENAME | winsound.SND_ASYNC)
			else:
				sys.exit("sound path not provided to playAndWait")
		return
	else:
		if waitFor < 0:
			waitDurationInSecs = sound.getDuration()
		elif waitFor > 0:
			waitDurationInSecs = waitFor
		else:
			waitDurationInSecs = 0

		if waitDurationInSecs > 0:
			sound.play()
			core.wait(waitDurationInSecs)
			sound.stop()
			return
		else:
			sound.play()
			# print('returning right away'
			return


def showText(win, textToShow, color=[-1, -1, -1], waitForKey=True, acceptOnly=0, inputDevice="keyboard", mouse=False,
			 pos=[0, 0], scale=1):
	global event
	# event.clearEvents() #clear all events just in case
	win.flip()
	if win.units == "pix":
		height = 30 * scale
		wrapWidth = int(win.size[0] * .8)
	elif win.units == "deg":
		height = .7 * scale
		wrapWidth = 30
	else:
		wrapWidth = None
	textStim = visual.TextStim(win, pos=pos, wrapWidth=wrapWidth, color=color, height=height, text=textToShow)
	textStim.draw()
	win.flip()
	if mouse:
		while any(mouse.getPressed()):
			core.wait(.1)  # waits for the user to release the mouse
		while not any(mouse.getPressed()):
			pass
		return
	elif inputDevice == "keyboard":
		if waitForKey:
			if acceptOnly == 0:
				event.waitKeys()
			else:
				# event.waitKeys(keyList=list(str(acceptOnly)))
				event.waitKeys(keyList=[acceptOnly])
			return
		else:
			# event.clearEvents(eventType='keyboard')
			return
	elif inputDevice == "gamepad":  # also uses mouse if mouse is not false
		while True:
			for event in pygame.event.get():  # check responses
				if mouse:
					if event.type == pygame.MOUSEBUTTONDOWN:
						pygame.event.clear()
						return
				if event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN:
					pygame.event.clear()
					return


def waitingAnimation(win, size=20, distanceBetweenElements=3, numElements=8, delay=1.0):
	totalWidth = numElements * (size + distanceBetweenElements)
	positions = range(totalWidth / -2, totalWidth / 2, (size + distanceBetweenElements))
	for curFrame in range(numElements, -1, -1):
		for curElement in range(curFrame):
			visual.PatchStim(win, color='white', size=size, tex='None', mask='circle',
							 pos=[positions[curElement], 0]).draw()
		win.flip()
		core.wait(delay)


def playWinSound(soundPath):
	winsound.PlaySound(soundPath, winsound.SND_FILENAME | winsound.SND_ASYNC)


def giveFeedback(isRight):
	if isRight == 1:
		playWinSound('bleep')
	else:
		playWinSound('buzz')
