import os
import pygaze
import psychopy
from pygaze import libscreen
from pygaze import libinput

from baseDefsPsychoPy import *
from stimPresPyGaze import *
from stimPresPsychoPy import *
import constants

class Exp:
	def __init__(self):
		self.expName = "TestExp"
		self.path = os.getcwd()
		self.subjInfo = {
			'1': {'name': 'subjCode',
				  'prompt': 'EXP_XXX',
				  'options': 'any',
				  'default': self.expName + '_001'}}

		[optionsReceived, self.subjVariables] = enterSubjInfo(self.expName, self.subjInfo)

		#TODO add variables to subInfo GUI instead of hard coding
		self.subjVariables['mainMonitor'] = 1
		self.disp = libscreen.Display(disptype='psychopy', fgc="black", bgc="black")
		self.win = pygaze.expdisplay

		# Inputs

		print("Using keyboard...")
		self.inputDevice = "keyboard"
		self.validResponses = {'1': 'space', '2': 'left', '3': 'right', '4': 'z', '5': 'enter'}
		# create keyboard object
		self.input = libinput.Keyboard(keylist=['space', 'enter', 'left', 'right'], timeout=None)

		self.imagePath = self.path + '/stimuli/images/'
		self.soundPath = self.path + '/stimuli/sounds/Ordertest/'
		self.moviePath = self.path + '/stimuli/movies/Ordertest/'
		self.imageExt = ['jpg', 'png', 'gif', 'jpeg']

class ExpPresentation(Exp):
	def __init__(self, experiment):
		self.experiment = experiment

	def initializeExperiment(self):
		loadScreen = libscreen.Screen()
		loadScreen.draw_text(text = "Loading Files...", color = "white", fontsize = 48)
		self.experiment.disp.fill(loadScreen)
		self.experiment.disp.show()

		# Load Trials
		trialPath = 'trialOrders/BabyInfo_Ordertest.csv'
		(self.trialListMatrix, self.trialFieldNames) = importTrials(trialPath, method="sequential")

		print(self.trialListMatrix)

		self.movieMatrix = loadFilesMovie(self.experiment.moviePath, ['mp4'], 'movie', self.experiment.win)
		#print(self.movieMatrix)

		self.soundMatrix = loadFiles(self.experiment.moviePath, ['.mp3'], 'sound')
		self.imageMatrix = loadFiles(self.experiment.imagePath, ['.png'], 'image',win = self.experiment.win)
		print(self.imageMatrix)
		#print(self.soundMatrix)

		self.pos = {'bottomLeft': (-585, -251), 'bottomRight': (585, -251), 'centerLeft': (-585, 0),
					'centerRight': (585, 0), 'topLeft': (-585, 251), 'topRight': (585, 251), 'center': (0, 0),
					'left': (-250, -251), 'right': (250, -251)}

		self.initialScreen = libscreen.Screen()
		self.initialImageName = self.experiment.imagePath + "bunnies.gif"
		initialImage = visual.ImageStim(self.experiment.win, self.initialImageName, mask=None, interpolate=True)
		initialImage.setPos(self.pos['center'])
		buildScreenPsychoPy(self.initialScreen, [initialImage])

	def presentScreen(self, screen):
		setAndPresentScreen(self.experiment.disp, screen)
		self.experiment.input.get_key()
		self.experiment.disp.show()

	def presentTrial(self, curTrial, curTrialIndex, getInput):
		self.experiment.disp.show()

		#grab correct movie, sound, and images
		mov = self.movieMatrix[curTrial['video']]
		sound = self.soundMatrix[curTrial['video']]
		target_image = self.imageMatrix[curTrial['TargetImage']][0]
		distractor_image = self.imageMatrix[curTrial['DistractorImage']][0]

		# set image locations
		target_location = curTrial['TargetObjectPos']
		distractor_location = curTrial['DistractorObjectPos']
		target_image.pos = self.pos[target_location]
		distractor_image.pos = self.pos[distractor_location]
		x_size = target_image.size[0]
		y_size = target_image.size[1]
		size_adjust = .5
		# set image sizes
		target_image.size = (x_size*size_adjust, y_size*size_adjust)
		distractor_image.size = (x_size*size_adjust, y_size*size_adjust)
		mov.size = (1024,768)
		#mov.size = (mov.size[0]*.6, mov.size[1]*.6)
		#pause the movie and sound on first frame
		mov.pause()
		sound.pause()

		#load sound until window flip for latency
		nextFlip = self.experiment.win.getFutureFlipTime(clock='ptb')
		sound.play(when = nextFlip)
		playAndWait(self.soundMatrix[curTrial['video']], waitFor=0)

		while mov.status != visual.FINISHED:
			mov.draw()
			target_image.draw()
			distractor_image.draw()
			self.experiment.win.flip()

		if mov.status == visual.FINISHED:
			mov.pause()

		# wait for n seconds
		wait_time = 1
		core.wait(wait_time)
	def cycleThroughTrials(self):

		curTrialIndex = 1

		for curTrial in self.trialListMatrix.trialList:
			print(curTrial)

			self.presentTrial(curTrial, curTrialIndex, getInput= "no")

			self.experiment.win.flip()

			#black screen for n seconds

			trial_spacing = 0
			#TODO: Fade instead of black screen? Is black screen too flashy?
			core.wait(trial_spacing)

			curTrialIndex += 1
currentExp = Exp()

currentPresentation = ExpPresentation(currentExp)

currentPresentation.initializeExperiment()
currentPresentation.presentScreen(currentPresentation.initialScreen)
currentPresentation.cycleThroughTrials()