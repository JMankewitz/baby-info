import psychopy.hardware.keyboard
import pygaze
from pygaze import libscreen, libinput, eyetracker
from pygaze.plugins import aoi
from baseDefsPsychoPy import *
from stimPresPyGaze import *
from stimPresPsychoPy import *
import constants
import tobii_research as tr

from psychopy import logging
logging.console.setLevel(logging.CRITICAL)

class Exp:
	def __init__(self):
		self.expName = "BabyInfo"
		self.path = os.getcwd()
		self.subjInfo = {
			'1': {'name': 'subjCode',
				  'prompt': 'EXP_XXX',
				  'options': 'any',
				  'default': self.expName + '_001'},
			'2': {'name': 'order',
                   'prompt': '(test / 1 / 2 / 3 / 4)',
                   'options': ("test", "1", "2", "3", "4"),
                   'default': "test",
                   'type': str},
			'3': {'name': 'eyetracker',
                   'prompt': '(yes / no)',
                   'options': ("yes", "no"),
                   'default': "yes",
                   'type': str},
			'4': {'name': 'activeMode',
				  'prompt': 'input / gaze',
				  'options': ("input", "gaze"),
				  'default': "input",
				  'type': str},
			'5': {'name': 'responseDevice',
				  'prompt': 'keyboard / mouse',
				  'options': ("keyboard", "mouse"),
				  'default': 'keyboard'}
		}

		optionsReceived = False
		fileOpened = False

		# open data files to save while checking to make sure that no data is overwritten
		while not fileOpened:
			[optionsReceived, self.subjVariables] = enterSubjInfo(self.expName, self.subjInfo)
			print(self.subjVariables)

			from pygaze import settings
			print(constants.LOGFILE)
			settings.LOGFILE = constants.LOGFILEPATH + self.subjVariables['subjCode']
			print("settings logfile: " + settings.LOGFILE)

			print("Tracker type: " + constants.TRACKERTYPE)
			if not optionsReceived:
				popupError(self.subjVariables)

			elif not os.path.isfile('data/' + 'training_data_' + self.subjVariables['subjCode'] + '.txt'):

				# if using an eyetracker
				if self.subjVariables['eyetracker'] == "yes":
					# import eyetracking package from pygaze
					from pygaze import eyetracker

					if not os.path.isfile(constants.LOGFILENAME + '_TOBII_output.tsv'):
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
		self.blackScreen = libscreen.Screen(fgc="black", bgc="black")
		self.win = pygaze.expdisplay
		# Stim Paths
		self.imagePath = self.path + '/stimuli/images/'
		#self.soundPath = self.path + '/stimuli/movies/Order' + self.subjVariables['order'] +'/'
		self.soundPath = self.path + '/stimuli/movies/OrderAll/'

		self.activeSoundPath = self.path + '/stimuli/sounds/sampleAudio/'
		#self.moviePath = self.path + '/stimuli/movies/Order' + self.subjVariables['order'] +'/'
		self.moviePath = self.path + '/stimuli/movies/OrderAll/'
		self.AGPath = self.path + '/stimuli/movies/AGStims/'
		self.imageExt = ['jpg', 'png', 'gif', 'jpeg']

		# Inputs

		if self.subjVariables['eyetracker'] == 'yes':


			self.eyetrackers = tr.find_all_eyetrackers()

			while len(self.eyetrackers) == 0:
				print("trying to find eyetracker...")
				self.eyetrackers = tr.find_all_eyetrackers()

			self.tracker = pygaze.eyetracker.EyeTracker(self.disp)
			print("Eyetracker connected? " + str(self.tracker.connected()))

		# We will always use the keyboard to start the experiment, but it won't always be the main input
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
		familiarizationTrialPath = 'orders/trialOrders/BabyInfo_Order' + self.experiment.subjVariables['order'] +".csv"
		activeTrainingTrialPath = 'orders/activeTrainingOrders/BabyInfo_ActiveTrainingOrdertest.csv'
		activeTestTrialPath = 'orders/activeOrders/BabyInfo_ActiveOrder' + self.experiment.subjVariables['order'] +".csv"

		(self.familTrialListMatrix, self.trialFieldNames) = importTrials(familiarizationTrialPath, method="sequential")
		(self.activeTrainingTrialsMatrix, self.activeTrainingTrialFieldNames) = importTrials(activeTrainingTrialPath, method="sequential")
		(self.activeTestTrialsMatrix, self.activeTrialFieldNames) = importTrials(activeTestTrialPath, method="sequential")

		self.movieMatrix = loadFilesMovie(self.experiment.moviePath, ['mp4'], 'movie', self.experiment.win)
		self.AGmovieMatrix = loadFilesMovie(self.experiment.AGPath, ['mp4'], 'movie', self.experiment.win)
		self.soundMatrix = loadFiles(self.experiment.soundPath, ['.mp3'], 'sound')
		self.AGsoundMatrix = loadFiles(self.experiment.AGPath, ['.mp3'], 'sound')
		self.activeSoundMatrix = loadFiles(self.experiment.activeSoundPath, ['.mp3'], 'sound')
		self.imageMatrix = loadFiles(self.experiment.imagePath, ['.png'], 'image', win = self.experiment.win)
		self.stars = loadFiles(self.experiment.AGPath, ['.jpg'], 'image', self.experiment.win)

		self.locations = ['left', 'right']

		# dimensions MATH ugh

		self.x_length = constants.DISPSIZE[0]
		self.y_length = constants.DISPSIZE[1]
		print(self.x_length, self.y_length)

		self.pos = {'bottomLeft': (-256, 0), 'bottomRight': (256, 0),
					'centerLeft': (-322, 0), 'centerRight': (322, 0),
					'topLeft': (-self.x_length/4, self.y_length/4),
					'topRight': (self.x_length/4, self.y_length/4),
					'center': (0, 0),
					'sampleStimLeft': (-322, -116),
					'sampleStimRight': (322, -116),
					'stimleft': (-256, -181),
					'stimright': (256, -181)
					}

		# Active sampling timing stuff
		self.timeoutTime = 10000
		self.aoiLeft = aoi.AOI('rectangle', pos = (0, 160), size = (355, 450))
		self.aoiRight = aoi.AOI('rectangle', pos= (668, 160), size=(355, 450))
		self.ISI = 1000
		self.startSilence = 0
		self.endSilence = 0

		#max seconds
		self.countMax = 20
		self.lookAwayPos = (-1,-1)
		self.labelTime = 1000
		self.famCountMax = 0

		# Build Screens for Image Based Displays (Initial Screen and Active Stuff)

		# INITIAL SCREEN #
		self.initialScreen = libscreen.Screen()
		self.initialImageName = self.experiment.imagePath + "bunnies.gif"
		initialImage = visual.ImageStim(self.experiment.win, self.initialImageName, mask=None, interpolate=True)
		initialImage.setPos(self.pos['center'])
		buildScreenPsychoPy(self.initialScreen, [initialImage])


		print("Files Loaded!")
	# Active Sampling Test Screen #

	def presentScreen(self, screen):
		setAndPresentScreen(self.experiment.disp, screen)
		self.experiment.input.get_key()
		self.experiment.disp.show()

	def cycleThroughTrials(self, whichPart):

		curFamilTrialIndex = 1

		if whichPart == "familiarizationPhase":
			for curTrial in self.familTrialListMatrix.trialList:
				print(curTrial)
				if curTrial['trialType'] == "training":
					self.presentTrial(curTrial, curFamilTrialIndex, stage = "familiarization", getInput = "no")

					self.experiment.win.flip()
				if curTrial['trialType'] == 'AG':
					self.presentAGTrial(curTrial, getInput = "no", duration = curTrial['AGTime'])
					self.experiment.win.flip()
				curFamilTrialIndex += 1

		elif whichPart == "sampleTraining":
			curActiveTrainingIndex = 1
			for curTrial in self.activeTrainingTrialsMatrix.trialList:
				print(curTrial)
				self.presentActiveTrial(curTrial, curActiveTrainingIndex, "training")
				curActiveTrainingIndex += 1

		elif whichPart == "sampleTest":
			curActiveTrainingIndex = 1
			for curTrial in self.activeTestTrialsMatrix.trialList:
				print(curTrial)
				self.presentActiveTrial(curTrial, curActiveTrainingIndex, "test")
				curActiveTrainingIndex += 1

	def presentAGTrial(self, curTrial, getInput, duration):

		# flip screen
		self.experiment.disp.fill(self.experiment.blackScreen)
		self.experiment.disp.show()

		# pause for duration of ISI
		libtime.pause(self.ISI)
		if self.experiment.subjVariables['eyetracker'] == "yes":
			self.experiment.tracker.start_recording()
			logData = "Experiment %s subjCode %s" % (
			self.experiment.expName, self.experiment.subjVariables['subjCode'])

			for field in self.trialFieldNames:
				logData += " "+field+" "+str(curTrial[field])
			#print("would have logged " + logData)
			self.experiment.tracker.log(logData)

		if curTrial['AGType'] == "image":
			# create picture
			curPic = self.pictureMatrix[curTrial['AGImage']][0]
			# position in center of screen
			curPic.pos = self.pos['center']
			# create screen
			agScreen = libscreen.Screen()
			# build screen
			buildScreenPsychoPy(agScreen, [curPic])

			# present screen
			# see stimPresPyGaze to see details on setAndPresentScreen
			# basically, it simply fills the display with the specified screen (setting) and then flips (shows) the screen (presenting)
			setAndPresentScreen(self.experiment.disp, agScreen)
			if self.experiment.subjVariables['eyetracker'] == "yes":
				# log event
				self.experiment.tracker.log("presentImage")

			if curTrial['AGAudio'] != "none":
				playAndWait(self.soundMatrix[curTrial['AGAudio']], waitFor=0)

				if self.experiment.subjVariables['eyetracker'] == "yes":
					# log event
					self.experiment.tracker.log("presentAudio")

			# display for rest of ag Time
			libtime.pause(duration)

		elif curTrial['AGType'] == "movie":
			# load movie stim
			# mov = visual.MovieStim3(self.experiment.win, self.experiment.moviePath+curTrial['AGVideo'] )
			mov = self.AGmovieMatrix[curTrial['AGVideo']]
			#mov.loadMovie(self.experiment.moviePath + curTrial['AGVideo'] + self.movieExt)
			mov.size = (1024, 560)

			if curTrial['AGAudio'] != "none":
				playAndWait(self.AGsoundMatrix[curTrial['AGAudio']], waitFor=0)
				if self.experiment.subjVariables['eyetracker'] == "yes":
					# log event
					self.experiment.tracker.log("presentAudio")

			if self.experiment.subjVariables['eyetracker'] == "yes":
				# log event
				self.experiment.tracker.log("presentMovie")

			while mov.status != visual.FINISHED:
				mov.draw()
				#mov.draw()
				self.experiment.win.flip()

		# if getInput=True, wait for keyboard press before advancing
		if getInput == "yes":
			self.experiment.input.get_key()

		if self.experiment.subjVariables['eyetracker'] == "yes":
			# stop eye tracking
			self.experiment.tracker.stop_recording()

		self.experiment.disp.fill(self.experiment.blackScreen)

	# self.experiment.win2.flip(clearBuffer=True)

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
			#print("would have logged " + logData)
			self.experiment.tracker.log(logData)

		#grab correct movie, sound, and images
		mov = self.movieMatrix[curTrial['video']]
		curSound = self.soundMatrix[curTrial['video']]
		left_image = self.imageMatrix[curTrial['leftImage']][0]
		left_image.pos = self.pos['stimleft']
		right_image = self.imageMatrix[curTrial['rightImage']][0]
		right_image.pos = self.pos['stimright']

		# set image sizes
		left_image.size = (200, 200)
		right_image.size = (200, 200)
		mov.size = (1024, 560)

		#load sound until window flip for latency

		mov.draw()
		mov.pause()
		left_image.draw()
		right_image.draw()
		self.experiment.win.flip()

		trialTimerStart = libtime.get_time()
		libtime.pause(self.startSilence)
		curSound.volume = 3
		curSound.play()
		mov.play()

		if self.experiment.subjVariables['eyetracker'] == "yes":
			# log event
			self.experiment.tracker.log("startScreen")

		while mov.status != visual.FINISHED:
			mov.draw()
			left_image.draw()
			right_image.draw()
			self.experiment.win.flip()

		if mov.status == visual.FINISHED:
			mov.pause()

		libtime.pause(self.endSilence)

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
		# Set up screens
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
		self.leftSpeakerGrayImage.size = (280, 400)

		self.leftSpeakerColorImage = self.imageMatrix[leftSpeakerImageColorName][0]
		self.leftSpeakerColorImage.setPos(self.pos['centerLeft'])
		self.leftSpeakerColorImage.size = (280, 400)
		# Right
		self.rightSpeakerGrayImage = self.imageMatrix[rightSpeakerImageGrayName][0]
		self.rightSpeakerGrayImage.setPos(self.pos['centerRight'])
		self.rightSpeakerGrayImage.size = (280, 400)

		self.rightSpeakerColorImage = self.imageMatrix[rightSpeakerImageColorName][0]
		self.rightSpeakerColorImage.setPos(self.pos['centerRight'])
		self.rightSpeakerColorImage.size = (280, 400)

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

		if stage == "test":

			# Load correct novel images
			leftNovelImageGrayName = curTrial['novelImage'] + '_left_grayscale'
			rightNovelImageGrayName = curTrial['novelImage'] + '_right_grayscale'
			leftNovelImageColorName = curTrial['novelImage'] + '_left_color'
			rightNovelImageColorName = curTrial['novelImage'] + '_right_color'

			# Find Psychopy Stim from image matrix
			# Left
			self.leftNovelGrayImage = self.imageMatrix[leftNovelImageGrayName][0]
			self.leftNovelGrayImage.setPos(self.pos['sampleStimLeft'])
			self.leftNovelGrayImage.size = (150, 130)

			self.leftNovelColorImage = self.imageMatrix[leftNovelImageColorName][0]
			self.leftNovelColorImage.setPos(self.pos['sampleStimLeft'])
			self.leftNovelColorImage.size = (150, 130)

			# Right
			self.rightNovelGrayImage = self.imageMatrix[rightNovelImageGrayName][0]
			self.rightNovelGrayImage.setPos(self.pos['sampleStimRight'])
			self.rightNovelGrayImage.size = (150, 130)

			self.rightNovelColorImage = self.imageMatrix[rightNovelImageColorName][0]
			self.rightNovelColorImage.setPos(self.pos['sampleStimRight'])
			self.rightNovelColorImage.size = (150, 130)

			# TODO: if this works append color images to active color screens
			self.activeGrayScreen.screen.append(self.rightNovelGrayImage)
			self.activeGrayScreen.screen.append(self.leftNovelGrayImage)

			self.activeLeftScreen.screen.append(self.leftNovelColorImage)
			self.activeLeftScreen.screen.append(self.rightNovelGrayImage)
			self.activeRightScreen.screen.append(self.rightNovelColorImage)
			self.activeRightScreen.screen.append(self.leftNovelGrayImage)

			self.activeColorScreen.screen.append(self.leftNovelColorImage)
			self.activeColorScreen.screen.append(self.rightNovelColorImage)

		# Initialize eyetracker

		libtime.pause(self.ISI)

		if self.experiment.subjVariables['eyetracker'] == 'yes':
			self.experiment.tracker.start_recording()
			self.experiment.tracker.log(
				"Experiment %s subjCode %s TrialNumber %d TrialType %s" % (
					self.experiment.expName,
					self.experiment.subjVariables['subjCode'],
					curActiveTrialIndex, stage))

		trialTimerStart = libtime.get_time()

		setAndPresentScreen(self.experiment.disp, self.activeColorScreen)

		if self.experiment.subjVariables['eyetracker'] == "yes":
			# log event
			self.experiment.tracker.log("startScreen")
		# pause for non-contingent color display
		libtime.pause(1000)

		#start contingent
		setAndPresentScreen(self.experiment.disp, self.activeGrayScreen)

		if self.experiment.subjVariables['eyetracker'] == "yes":
			# log event
			self.experiment.tracker.log("startContingent")

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
				####smoothing eyetracking sample###

				# get current gaze position
				curGazePos = self.experiment.tracker.sample()

				# add cur gaze position to the list
				last150ms.append(curGazePos)

				# if the length of the list exceeds 150 ms/16.6667==9, then delete the earliest item in the list:
				if len(last150ms) > 9:
					del (last150ms[0])

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

			elif self.experiment.subjVariables['activeMode'] == "input":
				if self.experiment.inputDevice == 'keyboard':
					response = self.experiment.input.get_key(keyList=[self.experiment.validResponses['2'],
																	  self.experiment.validResponses['3']],
															 clear=True)
					print(response)
					if response != None:
						if response == '2':
							response = 'left'
						elif response == '3':
							response = 'right'

					if response == 'left':
						gazepos = (256, 384)
					elif response == 'right':
						gazepos = (768, 384)
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

			if eventTriggered == 1:
				firstTrigger = 0
			elif eventTriggered == 0:
				if countLeft > self.countMax:
					selectionNum += 1
					eventTriggered = 1
					if firstTrigger == 0:
						firstTrigger = 1

					eventTriggerTime = libtime.get_time()
					eventStartTime_list.append(eventTriggerTime)
					rt = eventTriggerTime - t0
					rt_list.append(rt)

					# log event
					if self.experiment.subjVariables['eyetracker'] == 'yes':
						self.experiment.tracker.log("selection" + str(selectionNum))
					selectionTime = libtime.get_time()
					gazeCon = True
					contingent = True
					response = "left"
					response_list.append(response)
				elif countRight > self.countMax:
					selectionNum += 1
					eventTriggered = 1
					if firstTrigger == 0:
						firstTrigger = 1

					eventTriggerTime = libtime.get_time()
					eventStartTime_list.append(eventTriggerTime)
					rt = eventTriggerTime - t0
					rt_list.append(rt)

					# log event
					if self.experiment.subjVariables['eyetracker'] == 'yes':
						self.experiment.tracker.log("selection" + str(selectionNum))
					selectionTime = libtime.get_time()
					gazeCon = True
					contingent = True
					response = "right"
					response_list.append(response)

			if firstTrigger == 1:
				chosenImage = curTrial[response + "Image"]
				chosenAudio = curTrial[response + 'Audio']
				chosenImage_list.append(chosenImage)
				chosenAudio_list.append(chosenAudio)
				if response == "left":
					setAndPresentScreen(self.experiment.disp, self.activeLeftScreen)
				if response == "right":
					setAndPresentScreen(self.experiment.disp, self.activeRightScreen)

				# Start audio

				self.activeSoundMatrix[chosenAudio].setLoops(-1)
				print(self.activeSoundMatrix[chosenAudio].loops)
				playAndWait(self.activeSoundMatrix[chosenAudio], waitFor=0)
				audioTime = libtime.get_time()
				audioStartTime_list.append(audioTime)
				if self.experiment.subjVariables['eyetracker'] == "yes":
					# log audio event
					self.experiment.tracker.log("audio" + str(selectionNum))

			if eventTriggered == 1:
				# check if the infant has switched
				if curLook != response and libtime.get_time() - audioTime > self.labelTime:
					countLeft = 0
					countRight = 0
					gazeCon = False
					contingent = False
					eventTriggered = 0
					firstTrigger = 0
					# stop sound
					self.activeSoundMatrix[chosenAudio].stop()
					audioStopTime = libtime.get_time()
					audioPlayTime_list.append(audioStopTime - audioTime)
					audioStopTime_list.append(audioStopTime)

					# reset screen
					setAndPresentScreen(self.experiment.disp, self.activeGrayScreen)
					if self.experiment.subjVariables['eyetracker'] == "yes":
						# log audio event end
						self.experiment.tracker.log(
							"audioEnd" + str(selectionNum))
		if eventTriggered == 1:
			# stop sound
			self.activeSoundMatrix[chosenAudio].stop()
			audioStopTime = libtime.get_time()
			audioPlayTime_list.append(audioStopTime - audioTime)
			audioStopTime_list.append(audioStopTime)

		self.experiment.disp.fill()
		self.experiment.disp.show()

		trialTimerEnd = libtime.get_time()
		# trial time
		trialTime = trialTimerEnd - trialTimerStart
		if self.experiment.subjVariables['eyetracker'] == "yes":
			# stop eye tracking
			self.experiment.tracker.stop_recording()


	def EndDisp(self):
		# show the screen with no stars filled in
		# self.stars['0'][0].draw()
		# print(self.stars)
		# win.flip()

		curStar = self.stars['0'][0]
		curStar.size = (self.x_length, self.y_length)
		# create screen
		endScreen = libscreen.Screen()
		# build screen
		buildScreenPsychoPy(endScreen, [curStar])

		# present screen
		setAndPresentScreen(self.experiment.disp, endScreen)

		core.wait(1)

		# iterate to fill in each star
		for i in range(1, 6, 1):
			# self.stars[str(i)][0].draw()
			#  win.flip()
			curStar = self.stars[str(i)][0]
			curStar.size = (self.x_length, self.y_length)
			# build screen
			buildScreenPsychoPy(endScreen, [curStar])
			# present screen
			setAndPresentScreen(self.experiment.disp, endScreen)

			self.AGsoundMatrix['ding'].play()
			core.wait(.75)
			self.AGsoundMatrix['ding'].stop()

		# have the stars jiggle
		self.AGsoundMatrix['applause'].play()
		self.AGsoundMatrix['done'].play()

		for i in range(4):
			# self.stars['5'][0].draw()
			# win.flip()
			curStar = self.stars['5'][0]
			curStar.size = (self.x_length, self.y_length)
			# build screen
			buildScreenPsychoPy(endScreen, [curStar])
			# present screen
			setAndPresentScreen(self.experiment.disp, endScreen)

			core.wait(.5)
			# self.stars['5_left'][0].draw()
			# win.flip()

			curStar = self.stars['5_left'][0]
			curStar.size = (self.x_length, self.y_length)
			# build screen
			buildScreenPsychoPy(endScreen, [curStar])
			# present screen
			setAndPresentScreen(self.experiment.disp, endScreen)
			core.wait(.5)

			# self.stars['5'][0].draw()
			# win.flip()
			# core.wait(.5)
			# self.stars['5_right'][0].draw()
			# win.flip()
			# core.wait(.5)

			curStar = self.stars['5'][0]
			curStar.size = (self.x_length, self.y_length)
			# build screen
			buildScreenPsychoPy(endScreen, [curStar])
			# present screen
			setAndPresentScreen(self.experiment.disp, endScreen)

			core.wait(.5)
			# self.stars['5_left'][0].draw()
			# win.flip()

			curStar = self.stars['5_right'][0]
			curStar.size = (self.x_length, self.y_length)
			# build screen
			buildScreenPsychoPy(endScreen, [curStar])
			# present screen
			setAndPresentScreen(self.experiment.disp, endScreen)
			core.wait(.5)


currentExp = Exp()

currentPresentation = ExpPresentation(currentExp)

currentPresentation.initializeExperiment()
currentPresentation.presentScreen(currentPresentation.initialScreen)
currentPresentation.cycleThroughTrials(whichPart = "sampleTraining")
currentPresentation.cycleThroughTrials(whichPart = "familiarizationPhase")
currentPresentation.cycleThroughTrials(whichPart = "sampleTest")
currentPresentation.EndDisp()