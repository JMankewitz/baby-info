import pygaze
from pygaze import libscreen, libinput, eyetracker
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
                   'type': str},
			'3': {'name': 'activeMode',
				  'prompt': 'input / gaze',
				  'options': ("input", "gaze"),
				  'default': "input",
				  'type': str},
			'4': {'name': 'responseDevice',
				  'prompt': 'keyboard / mouse',
				  'options': ("keyboard", "mouse"),
				  'default': 'keyboard'}
		}

		optionsReceived = False
		fileOpened = False

		# open data files to save while checking to make sure that no data is overwritten
		while not fileOpened:
			[optionsReceived, self.subjVariables] = enterSubjInfo(self.expName, self.subjInfo)
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

		# TODO: Psychopy no longer reads both keyboard and mouse for some reason, need one or the other
		# We will always use the keyboard to start the experiment, but it won't always be the main input
		self.nextinput = libinput.Keyboard(keylist=['space', 'enter', 'left', 'right'], timeout=None)
		if self.subjVariables['responseDevice'] == 'keyboard':
			print("Using keyboard...")
			self.inputDevice = "keyboard"
			self.validResponses = {'1': 'space', '2': 'left', '3': 'right', '4': 'z', '5': 'enter'}
		# create keyboard object
			self.input = libinput.Keyboard(keylist=['space', 'enter', 'left', 'right'], timeout=None)

		else:
			self.inputDevice = "mouse"
			print("using mouse...")
			self.input = libinput.Mouse(mousebuttonlist = [1], timeout = None)


class ExpPresentation(Exp):
	def __init__(self, experiment):
		self.experiment = experiment

	def initializeExperiment(self):
		
		# Loading Files Screen
		loadScreen = libscreen.Screen()
		loadScreen.draw_text(text = "Loading Files...", color = "white", fontsize = 48)
		self.experiment.disp.fill(loadScreen)
		self.experiment.disp.show()

		# Load Trials
		familiarizationTrialPath = 'orders/trialOrders/BabyInfo_Ordertest.csv'
		activeTrainingTrialPath = 'orders/activeTrainingOrders/BabyInfo_ActiveTrainingOrdertest.csv'
		activeTestTrialPath = 'orders/activeOrders/BabyInfo_ActiveOrdertest.csv'

		(self.familTrialListMatrix, self.trialFieldNames) = importTrials(familiarizationTrialPath, method="sequential")
		(self.activeTrainingTrialsMatrix, self.activeTrainingTrialFieldNames) = importTrials(activeTrainingTrialPath, method="sequential")
		(self.activeTestTrialsMatrix, self.activeTrialFieldNames) = importTrials(activeTestTrialPath, method="sequential")

		self.movieMatrix = loadFilesMovie(self.experiment.moviePath, ['mp4'], 'movie', self.experiment.win)
		self.soundMatrix = loadFiles(self.experiment.moviePath, ['.mp3'], 'sound')
		self.imageMatrix = loadFiles(self.experiment.imagePath, ['.png'], 'image',win = self.experiment.win)

		self.locations = ['left', 'right']

		# dimensions MATH ugh

		self.x_length = constants.DISPSIZE[0]
		self.y_length = constants.DISPSIZE[1]
		print(self.x_length, self.y_length)

		self.pos = {'bottomLeft': (-self.x_length/4, -self.y_length/4), 'bottomRight': (self.x_length/4, -self.y_length/4),
					'centerLeft': (-256, 0), 'centerRight': (256, 0),
					'topLeft': (-self.x_length/4, self.y_length/4), 'topRight': (self.x_length/4, self.y_length/4),
					'center': (0, 0),
					'stimleft': (-self.x_length/4, -self.y_length/3), 'stimright': (self.x_length/4, -self.y_length/3),
					}

		# Active sampling timing stuff
		self.timeoutTime = 10000
		#TODO: Starting without a buffer
		self.aoiLeft = aoi.AOI('rectangle', pos = (81, 134), size = (350, 500))
		self.aoiRight = aoi.AOI('rectangle', pos= (593, 134), size=(350, 500))
		self.ISI = 1000

		#max seconds
		self.countMax = 10
		self.lookAwayPos = (-1024,-768)
		self.labelTime = 1000
		self.famCountMax = 0

		# Build Screens for Image Based Displays (Initial Screen and Active Stuff)

		# INITIAL SCREEN #
		self.initialScreen = libscreen.Screen()
		self.initialImageName = self.experiment.imagePath + "bunnies.gif"
		initialImage = visual.ImageStim(self.experiment.win, self.initialImageName, mask=None, interpolate=True)
		initialImage.setPos(self.pos['center'])
		buildScreenPsychoPy(self.initialScreen, [initialImage])

		# Active Screen(s) #
		# Picture Names (should match name in left/right image column
		# Left speaker
		leftSpeakerImageGrayName = self.activeTrainingTrialsMatrix.trialList[0]['leftImage'] + '_grayscale'
		leftSpeakerImageColorName = self.activeTrainingTrialsMatrix.trialList[0]['leftImage'] + '_color'
		# Right speaker
		rightSpeakerImageGrayName = self.activeTrainingTrialsMatrix.trialList[0]['rightImage'] + '_grayscale'
		rightSpeakerImageColorName = self.activeTrainingTrialsMatrix.trialList[0]['rightImage'] + '_color'

		# Find Psychopy Stim from image matrix
		# Left
		self.leftSpeakerGrayImage = self.imageMatrix[leftSpeakerImageGrayName][0]
		self.leftSpeakerGrayImage.setPos(self.pos['centerLeft'])
		self.leftSpeakerColorImage = self.imageMatrix[leftSpeakerImageColorName][0]
		self.leftSpeakerColorImage.setPos(self.pos['centerLeft'])
		# Right
		self.rightSpeakerGrayImage = self.imageMatrix[rightSpeakerImageGrayName][0]
		self.rightSpeakerGrayImage.setPos(self.pos['centerRight'])
		self.rightSpeakerColorImage = self.imageMatrix[rightSpeakerImageColorName][0]
		self.rightSpeakerColorImage.setPos(self.pos['centerRight'])

		self.leftAudioIntroduction = self.activeTrainingTrialsMatrix.trialList[0]['leftAudio']
		self.rightAudioIntroduction = self.activeTrainingTrialsMatrix.trialList[0]['rightAudio']

		self.leftAudioNovel = self.activeTestTrialsMatrix.trialList[0]['leftAudio']
		self.rightAudioNovel = self.activeTestTrialsMatrix.trialList[0]['rightAudio']

		# Initialize Screens
		self.activeGrayScreen = libscreen.Screen(disptype='psychopy')
		self.activeColorScreen = libscreen.Screen(disptype='psychopy')

		# activated screens
		self.activeLeftScreen = libscreen.Screen(disptype='psychopy')
		self.activeRightScreen = libscreen.Screen(disptype='psychopy')

		#Active Gray
		buildScreenPsychoPy(self.activeGrayScreen, [self.leftSpeakerGrayImage, self.rightSpeakerGrayImage])
		buildScreenPsychoPy(self.activeColorScreen, [self.leftSpeakerColorImage, self.rightSpeakerColorImage])
		buildScreenPsychoPy(self.activeLeftScreen, [self.leftSpeakerColorImage, self.rightSpeakerGrayImage])
		buildScreenPsychoPy(self.activeRightScreen, [self.leftSpeakerGrayImage, self.rightSpeakerColorImage])

		print("Files Loaded!")
	# Active Sampling Test Screen #

	def presentScreen(self, screen):
		setAndPresentScreen(self.experiment.disp, screen)
		self.experiment.nextinput.get_key()
		self.experiment.disp.show()
	def cycleThroughTrials(self, whichPart):

		curActiveTrainingIndex = 1
		curFamilTrialIndex = 1

		if whichPart == "familiarizationPhase":
			for curTrial in self.familTrialListMatrix.trialList:
				print(curTrial)

				self.presentTrial(curTrial, curFamilTrialIndex, stage = "familiarization", getInput = "no")

				self.experiment.win.flip()

				# black screen for n seconds

				trial_spacing = 0
				# TODO: Fade instead of black screen? Is black screen too flashy?
				libtime.pause(trial_spacing)

				curFamilTrialIndex += 1

		elif whichPart == "sampleTraining":
			for curTrial in self.activeTrainingTrialsMatrix.trialList:
				print(curTrial)
				self.presentActiveTrial(curTrial, curActiveTrainingIndex, "training")
				curActiveTrainingIndex += 1

		elif whichPart == "sampleTest":
			print("This part would be the active sampling Test")

	def presentTrial(self, curTrial, curTrialIndex, stage, getInput):

		self.experiment.disp.show()
		libtime.pause(self.ISI)

		# start eyetracking
		if self.experiment.subjVariables['eyetracker'] == "yes":
			self.experiment.tracker.start_recording()
			logData = "Experiment %s subjCode %s Phase %s TrialNumber %d" % (
			self.experiment.expName, self.experiment.subjVariables['subjCode'], stage,
			curTrialIndex)

			for field in self.trialFieldNames:
				logData += " "+field+" "+str(curTrial[field])
			print("would have logged " + logData)
			self.experiment.tracker.log(logData)


		#grab correct movie, sound, and images
		mov = self.movieMatrix[curTrial['video']]
		curSound = self.soundMatrix[curTrial['video']]
		target_image = self.imageMatrix[curTrial['TargetImage']][0]
		distractor_image = self.imageMatrix[curTrial['DistractorImage']][0]

		# set image locations
		target_location = curTrial['TargetObjectPos']
		distractor_location = curTrial['DistractorObjectPos']
		target_image.pos = self.pos["stim"+target_location]
		distractor_image.pos = self.pos["stim"+distractor_location]

		# set image sizes
		target_image.size = (250, 250)
		distractor_image.size = (250, 250)
		mov.size = (self.x_length, self.y_length)
		#pause the movie and sound on first frame
		mov.pause()
		curSound.pause()

		#load sound until window flip for latency
		nextFlip = self.experiment.win.getFutureFlipTime(clock='ptb')
		curSound.play(when = nextFlip)
		playAndWait(self.soundMatrix[curTrial['video']], waitFor=0)
		trialTimerStart = libtime.get_time()

		if self.experiment.subjVariables['eyetracker'] == "yes":
			# log event
			self.experiment.tracker.log("startScreen")

		while mov.status != visual.FINISHED:
			mov.draw()
			target_image.draw()
			distractor_image.draw()
			self.experiment.win.flip()

		if mov.status == visual.FINISHED:
			mov.pause()

		#TODO: Code this depending on video length

		end_time = 1
		libtime.pause(1000)

		######Stop Eyetracking######

		# trialEndTime
		trialTimerEnd = libtime.get_time()
		# trial time
		trialTime = trialTimerEnd - trialTimerStart
		if self.experiment.subjVariables['eyetracker'] == "yes":
			# stop eye tracking
			self.experiment.tracker.stop_recording()

		self.experiment.disp.fill()

		fieldVars = []
		for curField in self.trialFieldNames:
			fieldVars.append(curTrial[curField])

		[header, curLine] = createRespNew(self.experiment.subjInfo, self.experiment.subjVariables, self.trialFieldNames,
										  fieldVars,
										  a_curTrialIndex=curTrialIndex,
										  b_trialStart=trialTimerStart,
										  c_expTimer=trialTimerEnd,
										  d_trialTime=trialTime)

		writeToFile(self.experiment.trainingOutputFile, curLine)

	def presentActiveTrial(self, curTrial, curActiveTrialIndex, stage):
		# First code up with keyboard
		if stage == "training": #training doesn't have objects
			trialType = "activeTraining"
			if self.experiment.subjVariables['eyetracker'] == "yes":
				self.experiment.tracker.start_recording()
				# log data on trial
				self.experiment.tracker.log(
					"Experiment %s subjCode %s TrialNumber %d TrialType %s" % (
						self.experiment.expName,
						self.experiment.subjVariables['subjCode'],
						curActiveTrialIndex, trialType))
			# start trial timer
			trialTimerStart = libtime.get_time()

			setAndPresentScreen(self.experiment.disp, self.activeGrayScreen)
			startScreenTime = libtime.get_time()
			if self.experiment.subjVariables['eyetracker'] == "yes":
				# log event
				self.experiment.tracker.log("startScreen")

			#### Contingent Start #
			t0 = libtime.get_time()
			selectionNum = 0
			countLeft = 0
			countRight = 0
			gazeCon = False
			contingent = False
			eventTriggered = 0
			firstTrigger = 0
			last150ms = []

			# list of events
			rt_list = []
			response_list = []
			chosenImage_list = []
			chosenLabel_list = []
			chosenAudio_list = []
			chosenRole_list = []
			audioPlayTime_list = []
			audioStartTime_list = []
			audioStopTime_list = []
			eventStartTime_list = []

			while libtime.get_time() - t0 < self.timeoutTime:
				if self.experiment.subjVariables['activeMode'] == 'gaze':
					libtime.pause(10)
					# get gaze position
					curGazePos = self.experiment.tracker.sample()

					####smoothing eyetracking sample###

					# get current gaze position
					curGazePos = self.experiment.tracker.sample()

					# add cur gaze position to the list
					last150ms.append(curGazePos)

					# if the length of the list exceeds 150 ms/16.6667==9, then delete the earliest item in the list:
					if len(last150ms) > 9:
						del(last150ms[0])

					# Now, remove the (no looking data) tuples
					last150msClean = [e for e in last150ms if e != self.lookAwayPos]
					# Now calculate the mean
					if len(last150msClean) > 0:
						# calculate mean
						# looks a bit tricky, but that's jsut because I think the gaze positions are stored as tuples, which is a bit of an odd data structure.
						gazepos = tuple(
							map(lambda y: sum(y) / float(len(y)), zip(*last150msClean)))
					else:
						gazepos = self.lookAwayPos

					if self.aoiLeft.contains(gazepos):
						countLeft += 1
						curLook = "left"
					elif self.aoiRight.contains(gazepos):
						countRight += 1
						curLook = "right"
					else:
						curLook = "none"
					print(curLook)

				elif self.experiment.subjVariables['activeMode'] == "input":
					if self.experiment.inputDevice == 'keyboard':
						while libtime.get_time() - t0 < self.timeoutTime:
							(response, presstime) = self.experiment.input.get_key(keylist = [self.experiment.validResponses['2'],
																							 self.experiment.validResponses['3']],
																				  timeout=self.timeoutTime)
							if response != None:
								print(response)
								if response == '2':
									response = 'left'
								elif response == '3':
									response = 'right'

							if response == 'left':
								setAndPresentScreen(self.experiment.disp, self.activeLeftScreen)
							elif response == 'right':
								setAndPresentScreen(self.experiment.disp, self.activeRightScreen)

							print(response)


		elif stage == "test":
			print("this is where the test stuff would be")


currentExp = Exp()


currentPresentation = ExpPresentation(currentExp)


currentPresentation.initializeExperiment()
currentPresentation.presentScreen(currentPresentation.initialScreen)
currentPresentation.cycleThroughTrials(whichPart = "sampleTraining")
currentPresentation.cycleThroughTrials(whichPart = "familiarizationPhase")