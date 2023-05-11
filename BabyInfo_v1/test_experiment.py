import os
import pygaze
import psychopy
from pygaze import libscreen, libinput, eyetracker
from pygaze import plugins
from pygaze.plugins import aoi
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
				  'default': self.expName + '_001'},
			'2': {'name': 'eyetracker',
                   'prompt': '(yes / no)',
                   'options': ("yes", "no"),
                   'default': "yes",
                   'type': str}}

		optionsReceived = False
		fileOpened = False

		# open data files to save while checking to make sure that no data is overwritten
		while not fileOpened:
			[optionsReceived, self.subjVariables] = enterSubjInfo(self.expName, self.subjInfo)
			print(self.subjVariables)
			constants.LOGFILENAME = constants.LOGFILEPATH + self.subjVariables['subjCode']
			constants.LOGFILE = constants.LOGFILENAME[:]
			from pygaze import settings
			print(settings.LOGFILE)
			print("Tracker type: " + constants.TRACKERTYPE)
			if not optionsReceived:
				popupError(self.subjVariables)

			elif not os.path.isfile('data/' + 'training_data_' + self.subjVariables['subjCode'] + '.txt'):

				# if using an eyetracker
				if self.subjVariables['eyetracker'] == "yes":
					# import eyetracking package from pygaze
					from pygaze import eyetracker

					if not os.path.isfile(constants.LOGFILE + '_TOBII_output.tsv'):
						fileOpened = True
						self.activeTrainingOutputFile = open(
							'data/' + 'active_training_data_' + self.subjVariables['subjCode'] + '.txt', 'w')

						self.trainingOutputFile = open('data/' + 'training_data_' + self.subjVariables['subjCode'] + '.txt',
												   'w')
						self. activeOutputFile = open(
							'data/' + 'active_data_' + self.subjVariables['subjCode'] + '.txt',
							'w')

					else:
						fileOpened = False
						popupError(
							'That subject code for the eyetracking data already exists! The prompt will now close!')
						core.quit()
				else:
					fileOpened = True
					self.trainingOutputFile = open(
						'data/' + 'training_data_' + self.subjVariables['subjCode'] + '.txt', 'w')

			else:
				fileOpened = False
				popupError('That subject code already exists!')

		self.subjVariables['mainMonitor'] = 1
		self.disp = libscreen.Display(disptype='psychopy', fgc="black", bgc="black")
		self.win = pygaze.expdisplay

		# Stim Paths
		self.imagePath = self.path + '/stimuli/images/'
		self.soundPath = self.path + '/stimuli/sounds/Ordertest/'
		self.moviePath = self.path + '/stimuli/movies/Ordertest/'
		self.imageExt = ['jpg', 'png', 'gif', 'jpeg']

		# Inputs

		if self.subjVariables['eyetracker'] == 'yes':
			self.tracker = pygaze.eyetracker.EyeTracker(self.disp)

		print("Using keyboard...")
		self.inputDevice = "keyboard"
		self.validResponses = {'1': 'space', '2': 'left', '3': 'right', '4': 'z', '5': 'enter'}
		# create keyboard object
		self.input = libinput.Keyboard(keylist=['space', 'enter', 'left', 'right'], timeout=None)




class ExpPresentation(Exp):
	def __init__(self, experiment):
		self.experiment = experiment

	def initializeExperiment(self):
		loadScreen = libscreen.Screen()
		loadScreen.draw_text(text = "Loading Files...", color = "white", fontsize = 48)
		self.experiment.disp.fill(loadScreen)
		self.experiment.disp.show()

		# Load Trials
		trainingTrialPath = 'orders/trialOrders/BabyInfo_Ordertest.csv'
		activeTrainingTrialPath = 'orders/activeTrainingOrders/BabyInfo_ActiveTrainingOrdertest.csv'
		activeTrialPath = 'orders/activeOrders/BabyInfo_ActiveOrdertest.csv'
		(self.trialListMatrix, self.trialFieldNames) = importTrials(trainingTrialPath, method="sequential")
		(self.activeTrainingTrialsMatrix, self.activeTrainingTrialFieldNames) = importTrials(activeTrainingTrialPath,
																							 method="sequential")
		(self.activeTrialsMatrix, self.activeTrialFieldNames) = importTrials(activeTrialPath, method="sequential")

		print(self.trialListMatrix)

		self.movieMatrix = loadFilesMovie(self.experiment.moviePath, ['mp4'], 'movie', self.experiment.win)

		self.soundMatrix = loadFiles(self.experiment.moviePath, ['.mp3'], 'sound')
		self.imageMatrix = loadFiles(self.experiment.imagePath, ['.png'], 'image',win = self.experiment.win)

		self.pos = {'bottomLeft': (-585, -251), 'bottomRight': (585, -251), 'centerLeft': (-256, 0),
					'centerRight': (256, 0), 'topLeft': (-585, 251), 'topRight': (585, 251), 'center': (0, 0),
					'left': (-256, -251), 'right': (256, -251)}

		# Active sampling timing stuff
		self.timeoutTime = 20000
		self.aoiLeft = aoi.AOI('rectangle', pos = (-256, 0), size = (452, 646))
		self.aoiRight = aoi.AOI('rectangle', pos= (256, 0), size=(452, 646))

		#max seconds
		self.countMax = 10
		self.lookAwayPos = (-1024,-768)
		self.labelTime = 1000
		self.famCountMax = 0

		# Build screens

		# INITIAL SCREEN #
		self.initialScreen = libscreen.Screen()
		self.initialImageName = self.experiment.imagePath + "bunnies.gif"
		initialImage = visual.ImageStim(self.experiment.win, self.initialImageName, mask=None, interpolate=True)
		initialImage.setPos(self.pos['center'])
		buildScreenPsychoPy(self.initialScreen, [initialImage])

		# Active Screen(s) #
		self.activeGrayScreenPrompt = libscreen.Screen(disptype='psychopy')
		self.activeRightScreenPrompt = libscreen.Screen(
			disptype='psychopy')
		self.activeLeftScreenPrompt = libscreen.Screen(
			disptype='psychopy')

		# picture paths
		self.leftSpeakerImageGrayName = self.experiment.imagePath + \
										 self.activeTrainingTrialsMatrix.trialList[0]['leftImage'] + \
										 '_grayscale.png'



		self.activeTrainingScreen = libscreen.Screen(disptype='psychopy')
		self.leftSpeakerImageColorName = self.experiment.imagePath + \
									self.activeTrainingTrialsMatrix.trialList[0]['leftImage'] + \
									'_color.png'
		self.leftSpeakerImageColorName = self.experiment.imagePath + \
									self.activeTrainingTrialsMatrix.trialList[0]['rightImage'] + \
									'_color.png'
		# psychopy stim
		leftSpeakerColorImage = visual.ImageStim(self.experiment.win, self.leftSpeakerImageColorName, mask=None, interpolate=True)
		rightSpeakerColorImage = visual.ImageStim(self.experiment.win, self.leftSpeakerImageColorName, mask=None, interpolate=True)
		leftSpeakerColorImage.setPos(self.pos['centerLeft'])
		rightSpeakerColorImage.setPos(self.pos['centerRight'])
		self.leftAudioIntroduction = self.activeTrainingTrialsMatrix.trialList[0]['leftAudio']
		self.rightAudioIntroduction = self.activeTrainingTrialsMatrix.trialList[0]['rightAudio']

		buildScreenPsychoPy(self.activeTrainingScreen, [leftSpeakerColorImage, rightSpeakerColorImage])

	# Active Sampling Test Screen #

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
		target_image.size = (250, 250)
		distractor_image.size = (250, 250)
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

	def presentActiveTrial(self, curTrial):


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
#currentPresentation.cycleThroughTrials()