####################################
#LWL Example with Pygaze and Tobii #
####################################

#import constants for pygaze
import constants


#load pygaze libraries and custom pygaze libraries
import pygaze
from pygaze import libscreen
from pygaze import libtime
from pygaze import libinput
#from pygaze import eyetracker
# from pygaze import libgazecon
from stimPresPyGaze import *

#import basic python utility libraries
import random
import math
import time, os

#load psychopy and custom psychopy libraries
from psychopy import visual,event,core
from baseDefsPsychoPy import *
from stimPresPsychoPy import *
#print(prefs) #tell me about all current settings


#load pyo for audio
import pyo
import moviepy


class Exp:
    def __init__(self):
        self.expName = 'Genic3'
        #save current working directory for setting stimuli paths later
        self.path = os.getcwd()
        print(self.path)
        #dictionary to hold subject info to get at beginning of experiment
        self.subjInfo = {
                '1':  { 'name' : 'subjCode',
                        'prompt' : 'EXP_XXX',
                        'options': 'any',
                        'default':'101',
                        'type' : str},
                '2' : {	'name' : 'sex', 
			'prompt' : 'Subject Sex m/f: ', 
			'options' : ("m","f"),
			'default':'',
			'type' : str},
		'3' : {	'name' : 'age', 
			'prompt' : 'Subject Age: ', 
			'options' : 'any',
			'default':'',
			'type' : str},
		'4': {	'name' : 'Order', 
			'prompt' : 'Order (e.g., 1): ', 
			'options' : ("1","2"),
			'default':"1",
			'type' : str},
		'5': {	'name' : 'mainMonitor', 
			'prompt' : 'Screen Index (0,1,2,3): ', 
			'options' : (0,1,2,3),
			'default': 2,
			'type' : int},
		'6': {	'name' : 'sideMonitor', 
			'prompt' : 'Screen Index (0,1,2,3): ', 
			'options' : (0,1,2,3),
			'default': 3,
			'type' : int},
		'7' : {'name' : 'expInitials', 
			'prompt' : 'Experiment Initials: ', 
			'options' : 'any', 
			'default' : 'DB', 
			'type' : str}, 
		'8' : { 'name' : 'eyetracker', 
			'prompt' : '(yes / no)', 
			'options' : ("yes","no"), 
			'default' : "yes", 
			'type' : str},	
		'9' : { 'name' : 'pygazeVersion', 
			'prompt' : '(04 / 06)', 
			'options' : ("04","06"), 
			'default' : "06", 
			'type' : str},
		}

        optionsReceived = False
        fileOpened = False
        
        #open data files to save while checking to make sure that no data is overwritten
        while not fileOpened:
            [optionsReceived, self.subjVariables] = enterSubjInfo(self.expName, self.subjInfo)
            constants.LOGFILENAME=constants.LOGFILEPATH+self.expName+'_'+self.subjVariables['subjCode']
            constants.LOGFILE=constants.LOGFILENAME[:]
            if self.subjVariables['pygazeVersion'] == "06":
                from pygaze import display
                from pygaze import settings
                settings.LOGFILE = constants.LOGFILENAME[:]
                print "Settings Logfile Name"
                print settings.LOGFILE
            if not optionsReceived:
                popupError(self.subjVariables)
            elif not os.path.isfile('data/'+self.expName+'_data_'+self.subjVariables['subjCode']+'.txt'):
                
                #if using an eyetracker
                if self.subjVariables['eyetracker']=="yes":
                    #import eyetracking package from pygaze
                    print settings.LOGFILE
                    from pygaze import eyetracker
                    print settings.LOGFILE
                    if not os.path.isfile(constants.LOGFILE+'_TOBII_output.tsv'):
                        
                        settings.LOGFILE
                        fileOpened = True
                        self.testOutputFile= open('data/'+self.expName+'_data_'+self.subjVariables['subjCode']+'.txt','w')
                        
                    else:
                        fileOpened = False
                        popupError('That subject code for the eyetracking data already exists! The prompt will now close!')  
                        core.quit()
                else:
                    fileOpened = True
                    self.testOutputFile= open('data/'+self.expName+'_data_'+self.subjVariables['subjCode']+'.txt','w')
            else:
                fileOpened = False
                popupError('That subject code already exists!')        
                    
        # create display object
        #this is where screens are drawn to
        self.disp = libscreen.Display(disptype='psychopy',fgc="black",bgc="black",screennr=self.subjVariables['mainMonitor'])

        #main display parameters can be set through constants.py
        
        #create psychopy window based on Display() object 
        if self.subjVariables['pygazeVersion'] == "06":
            self.win = pygaze.expdisplay 
        else: 
            self.win = self.disp.expdisplay 
        
        #create psychopy window for tracking trials
        self.win2 = visual.Window(fullscr=True, color="black", allowGUI=True,
                                 monitor='infoMonitor', units='pix', winType='pyglet',screen=self.subjVariables['sideMonitor'])
        
        #if using the eyetracker
        if self.subjVariables['eyetracker']=="yes":
            # create eyetracker object
            self.tracker = eyetracker.EyeTracker(self.disp)
        
                
        #keyboard is response device
        #setting up some useful response variables
        print "Using keyboard..."
        self.inputDevice = "keyboard"
        self.validResponses = {'1':'space','2':'left', '3':'right', '4':'z', '5': 'enter'}
        # create keyboard object
        self.input = libinput.Keyboard(keylist=['space', 'enter', 'left', 'right'], timeout=None)
        
        #set up general variables for hold stimuli paths and image extension
        self.imagePath=self.path+'/stimuli/images/'
        self.soundPath=self.path+'/stimuli/sounds/'
        self.moviePath=self.path+'/stimuli/movies/'
        self.imageExt=['jpg','png','gif']

        
class ExpPresentation(Exp):
    def __init__(self,experiment):
        self.experiment = experiment
    
        
    def initializeExperiment(self):
        #This function initializes all of the important experiment parameters, pre-loads stimuli and pre-creates some experiment screens
        
        #screen that prints "Loading Files..." message to the screen while experiment initializes
        #i.e. trial lists and stimuli are loaded
        
        loadScreen = libscreen.Screen()
        loadScreen.draw_text(text="Loading Files...",colour="lightgray", fontsize=48)
        self.experiment.disp.fill(loadScreen)
        self.experiment.disp.show()
        self.experiment.disp.fill()
        
        ######EXPERIMENT PARAMETERS######
        #these may need to be edited from experiment to experiment
        
        #set trial lists to draw on
        #exposurePath = 'LWL_exposure.csv'
        #trialsPath = 'LWL_familiarization_List'+self.experiment.subjVariables["famList"]+'.csv'
        testPath='Genic3_Order_'+self.experiment.subjVariables["Order"]+'.csv'
        
        #print trialsPath
        
        #import trials based on trial list files
        #see baseDefsPsychoPy for details
        (self.testListMatrix, self.testFieldNames) = importTrials(testPath, method="sequential")
        
        #load sound files and image files (see baseDefsPsychoPy)
        self.pictureMatrix = loadFiles('stimuli/images', ['jpg','png','gif'], 'image', self.experiment.win)
        self.soundMatrix = loadFiles('stimuli/sounds',['wav'], 'sound')
        
        # load images and sounds for demo
        # self.statues = loadFiles('Demo/stimuli/statues/',['.jpg', 'png'],'image',self.experiment.win)
        # self.demoSounds = loadFiles('Demo/stimuli/sounds/',['.wav', 'aiff'],'sound',self.experiment.win)
        # self.demoLWL = loadFiles('Demo/stimuli/lwl/',['.jpg'], 'image',self.experiment.win)

        # self.statues['left'][0].size=[800,600]
        # self.statues['right'][0].size=[800,600]
        # self.demoLWL['Apple'][0].pos=(-585,-251)
        # self.demoLWL['Ball'][0].pos=(585,-251)

        
        # load images and sounds for end
        self.stars = loadFiles('Demo/stimuli/stars/',['.jpg', 'png'],'image',self.experiment.win)
        self.sounds = loadFiles('Demo/stimuli/sounds/',['.wav', 'aiff'],'sound',self.experiment.win)


        #initial experiment screen image to show
        self.initialImageName=self.experiment.imagePath+"bunnies.gif"
        
        ####POSITION PARAMETERS####
        #Set up dictionary controlling screen positions for stimuli
        # TV monitor is 1920 by 1080 & the positions specified below mark the center of the image
        self.pos={'bottomLeft': (-585,-251),'bottomRight':(585,-251), 'centerLeft': (-585,0), 'centerRight': (585,0), 'topLeft': (-585,251), 'topRight': (585,251), 'center': (0,0)}
        
        #####TIMING PARAMETERS#####
        #set duration of pauses between trial events
        
        #general ISI
        self.ISI=1000

        ############################
        #introductory image screens#
        ############################
        #this creates an initial image screen, waiting for keyboard response (space bar) to advance
        #create screen to draw to
        self.imageScreen=libscreen.Screen()
        #create initial image stim
        initialImage=visual.ImageStim(self.experiment.win, self.initialImageName,mask=None,interpolate=True) 
        initialImage.setPos(self.pos['center'])
        buildScreenPsychoPy(self.imageScreen,[initialImage])  

#     def demoExperiment(self):
#         # wait for space bar to start
#         readyScreen=libscreen.Screen()
#         readyScreen.draw_text(text="Demo Ready!",colour="lightgray", fontsize=48)
#         self.experiment.disp.fill(readyScreen)
#         self.experiment.disp.show()
#         self.experiment.disp.fill()
#         self.experiment.input.get_key()
#         self.experiment.disp.show()
# 
#         # LWL Demo
#         demoScreen=libscreen.Screen()
#         buildScreenPsychoPy(demoScreen,[self.demoLWL['Apple'][0],self.demoLWL['Ball'][0]])
#         setAndPresentScreen(self.experiment.disp, demoScreen)
#         self.demoSounds['apple_cool'].play()
#         core.wait(6.7)
# 
#         # Statues 
#         demoScreen=libscreen.Screen()
#         buildScreenPsychoPy(demoScreen,[self.statues['left'][0]])
#         setAndPresentScreen(self.experiment.disp, demoScreen)
#         core.wait(2)
#         
#         for i in range(3):
#             buildScreenPsychoPy(demoScreen,[self.statues['right'][0]])
#             setAndPresentScreen(self.experiment.disp, demoScreen)
#             self.demoSounds['eye1'].play()
#             core.wait(.5)
#             buildScreenPsychoPy(demoScreen,[self.statues['left'][0]])
#             setAndPresentScreen(self.experiment.disp, demoScreen)
#             self.demoSounds['eye2'].play()
#             core.wait(1)   
# 
#          # wait for space bar
#         self.experiment.input.get_key()   
    
    def presentScreen(self,screen):
        # show precreated screen and wait for valid input from response device (e.g. space bar from the keyboard)
        setAndPresentScreen(self.experiment.disp,screen)
        self.experiment.input.get_key()
    
    def presentAGTrial(self,curTrial,getInput,duration):
        
        #flip screen
        self.experiment.disp.show()
        
        #pause for duration of ISI
        libtime.pause(self.ISI)
        
        if curTrial['AGType']=="image":
            #create picture
            curPic=self.pictureMatrix[curTrial['AGImage']][0]
            #position in center of screen
            curPic.pos=self.pos['center']
            #create screen
            agScreen=libscreen.Screen()
            #build screen
            buildScreenPsychoPy(agScreen, [curPic])

            #present screen
            #see stimPresPyGaze to see details on setAndPresentScreen
            #basically, it simply fills the display with the specified screen (setting) and then flips (shows) the screen (presenting)
            setAndPresentScreen(self.experiment.disp,agScreen)
            
            #play audio
            playAndWait(self.soundMatrix[curTrial['AGAudio']],waitFor=0)
            
            #display for rest of ag Time
            libtime.pause(duration)
            
            
        elif curTrial['AGType']=="movie":
            #load movie stim
            print(self.experiment.moviePath)
            print(curTrial['AGVideo'])
            mov = visual.MovieStim3(self.experiment.win, self.experiment.moviePath+curTrial['AGVideo'] )
            # while mov.status != visual.FINISHED:
            #     mov.draw()
            #     self.experiment.win.flip()

            if curTrial['AGAudio'] != "none":
                playAndWait(self.soundMatrix[curTrial['AGAudio']],waitFor=0)
            while mov.status != visual.FINISHED:
                mov.draw()
                self.experiment.win.flip()

            
        #if getInput=True, wait for keyboard press before advancing
        if getInput:
            self.experiment.input.get_key()
            
        self.experiment.disp.fill()
        
    def presentTrial(self, curTrial, curTestTrialIndex,trialStartSilence,trialEndSilence,trialAudioDur):

        #self.checkExit()
        
        self.experiment.disp.show()
        #libtime.pause(self.ISI+random.choice([0,100,200]))
        libtime.pause(self.ISI)
        
        #######start eye tracking##########
        if self.experiment.subjVariables['eyetracker']=="yes":
            self.experiment.tracker.start_recording()
            #logging data
            logData="Experiment %s subjCode %s Order %s TrialNumber %d" % (self.experiment.expName, self.experiment.subjVariables['subjCode'],self.experiment.subjVariables['Order'],curTestTrialIndex)
            #log data from list of trial variables
            for field in self.testFieldNames:
                logData+=" "+field + " "+str(curTrial[field])
            #log data on trial
            self.experiment.tracker.log(logData)
        
        ########build and present text screen for hand coding######
        trialInfo="\n\nExperiment: " + self.experiment.expName +"\n\n"
        trialInfo+="Sub.Num: " + self.experiment.subjVariables['subjCode'] +"\n\n"
        trialInfo+="Order: " + self.experiment.subjVariables['Order'] +"\n\n"
        #trialInfo+="TrialType: " + str(curTrial['trialType']) + "\n\n"
        #trialInfo+="Block: " + str(curTrial['BlockID']) + "\n\n"
        trialInfo+="Trial.Num: " + str(curTestTrialIndex) + "\n\n"

        trialInfoStim=visual.TextStim(self.experiment.win2,text=trialInfo,color="white",height=72,wrapWidth=1200)
        trialInfoStim.draw()
        self.experiment.win2.flip()
        
        ########present start screen########
        
        curTargetLocation=curTrial['TargetObjectPos']
        curTargetTrialCoordinates=self.pos[curTargetLocation]
        curDistracterLocation=curTrial['DistracterObjectPos']
        curDistracterTrialCoordinates=self.pos[curDistracterLocation]
        #create pictures
        curTargetPic=self.pictureMatrix[curTrial['TargetImage']][0] #psychopy image stimulus
        curDistracterPic=self.pictureMatrix[curTrial['DistracterImage']][0] #psychopy image stimulus
        #set position
        curTargetPic.pos=curTargetTrialCoordinates
        curDistracterPic.pos=curDistracterTrialCoordinates
        #create screen
        testScreen=libscreen.Screen()
        #build screen
        buildScreenPsychoPy(testScreen, [curTargetPic,curDistracterPic])
        
        #start trial timer
        trialTimerStart=libtime.get_time()
        
        #present screen
        setAndPresentScreen(self.experiment.disp, testScreen)
        
        if self.experiment.subjVariables['eyetracker']=="yes":
            #log event
            self.experiment.tracker.log("testScreen")
        
        #wait for duration of trial onset silence
        libtime.pause(trialStartSilence)
        
        ######play audio######
        #play audio
        playAndWait(self.soundMatrix[curTrial['Audio']],waitFor=0)
        if self.experiment.subjVariables['eyetracker']=="yes":
            #log event
            self.experiment.tracker.log("audioOnset")
        
        libtime.pause(trialAudioDur)
        
        #record audio offset
        if self.experiment.subjVariables['eyetracker']=="yes":
            #log event
            self.experiment.tracker.log("audioOffset")   
        #silence at end of trial        
        libtime.pause(trialEndSilence)
        
        ######Stop Eyetracking######
        
        #trialEndTime
        trialTimerEnd=libtime.get_time()
        #trial time
        trialTime=trialTimerEnd-trialTimerStart
        if self.experiment.subjVariables['eyetracker']=="yes":
            #stop eye tracking
            self.experiment.tracker.stop_recording()
        
        self.experiment.disp.fill()
        
        #######Save data#########

        fieldVars=[]
        for curField in self.testFieldNames:
            fieldVars.append(curTrial[curField])

           
        [header, curLine] = createRespNew(self.experiment.subjInfo, self.experiment.subjVariables, self.testFieldNames, fieldVars,
                                        a_curTrialIndex = curTestTrialIndex,
                                        b_trialStart=trialTimerStart,
                                        c_expTimer=trialTimerEnd,
                                        d_trialTime=trialTime)
        
        writeToFile(self.experiment.testOutputFile,curLine)
    
             
    def cycleThroughExperimentTrials(self, whichPart):
        
        if whichPart=="test":
            curTestTrialIndex =1
            for curTrial in self.testListMatrix.trialList:
                print("Trial "+str(curTestTrialIndex)+" of 26")
                self.presentTrial(curTrial, curTestTrialIndex,curTrial['trialStartSilence'],curTrial['trialEndSilence'],curTrial['trialAudioDuration'])
                if int(curTrial['AG'])==1:
                    self.presentAGTrial(curTrial,curTrial['AGgetInput'],curTrial['AGTime'])
                curTestTrialIndex += 1
                
            self.experiment.testOutputFile.close()  

    def EndDisp(self):
        # show the screen with no stars filled in
        #self.stars['0'][0].draw()
        #print(self.stars)
        #win.flip()
        
        curStar=self.stars['0'][0]
        #create screen
        endScreen=libscreen.Screen()
        #build screen
        buildScreenPsychoPy(endScreen, [curStar])
        
        #present screen
        setAndPresentScreen(self.experiment.disp, endScreen)
        
        
        core.wait(1)

        # iterate to fill in each star
        for i in range(1,6,1):
           # self.stars[str(i)][0].draw()
          #  win.flip()
          curStar=self.stars[str(i)][0]
          #build screen
          buildScreenPsychoPy(endScreen, [curStar])
          #present screen
          setAndPresentScreen(self.experiment.disp, endScreen)
        
          self.sounds['ding'].play()
          core.wait(.5)

        # have the stars jiggle
        self.sounds['applause'].play()
        self.sounds['done'].play()

        for i in range(4):
            #self.stars['5'][0].draw()
            #win.flip()
            curStar=self.stars['5'][0]
            #build screen
            buildScreenPsychoPy(endScreen, [curStar])
            #present screen
            setAndPresentScreen(self.experiment.disp, endScreen)
        
            core.wait(.5)
            #self.stars['5_left'][0].draw()   
            #win.flip()
            
            curStar=self.stars['5_left'][0]
            #build screen
            buildScreenPsychoPy(endScreen, [curStar])
            #present screen
            setAndPresentScreen(self.experiment.disp, endScreen)
            core.wait(.5)
            
            #self.stars['5'][0].draw()
            #win.flip()
            #core.wait(.5)
            #self.stars['5_right'][0].draw()   
            #win.flip()
            #core.wait(.5)
            
            curStar=self.stars['5'][0]
            #build screen
            buildScreenPsychoPy(endScreen, [curStar])
            #present screen
            setAndPresentScreen(self.experiment.disp, endScreen)
        
            core.wait(.5)
            #self.stars['5_left'][0].draw()   
            #win.flip()
            
            curStar=self.stars['5_right'][0]
            #build screen
            buildScreenPsychoPy(endScreen, [curStar])
            #present screen
            setAndPresentScreen(self.experiment.disp, endScreen)
            core.wait(.5)

        
################
#RUN EXPERIMENT#
################  

#Create the experiment object and run the individual phases   
#creat experiment object      
currentExp = Exp()
#load ExpPresentation class
currentPresentation = ExpPresentation(currentExp)
#initialize the experiment
currentPresentation.initializeExperiment()
# present demo
# currentPresentation.demoExperiment()
#present the starting screen and wait for button press
currentPresentation.presentScreen(currentPresentation.imageScreen)
#if currentExp.subjVariables['eyetracker']=="yes":
# create eyetracker object
#    currentExp.tracker.calibrate()
#test phase
currentPresentation.cycleThroughExperimentTrials("test")
if currentExp.subjVariables['eyetracker']=="yes":
    #close tracker
    currentExp.tracker.close()
# display stars at end
currentPresentation.EndDisp()
#close experiment and expend libtime
currentExp.win2.close()
currentExp.disp.close()
libtime.expend()