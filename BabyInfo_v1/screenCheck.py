#!/usr/bin/env python

#script for testing screen locations

from psychopy import visual, event, core, gui


win0 = visual.Window(fullscr=True, color="black", allowGUI=True,
                                 monitor='infoMonitor0', units='pix', winType='pyglet',screen=0)
win1 = visual.Window(fullscr=True, color="black", allowGUI=True,
                                 monitor='infoMonitor1', units='pix', winType='pyglet',screen=1)
win2 = visual.Window(fullscr=True, color="black", allowGUI=True,
                                 monitor='infoMonitor2', units='pix', winType='pyglet',screen=2)
win3 = visual.Window(fullscr=True, color="black", allowGUI=True,
                                 monitor='infoMonitor3', units='pix', winType='pyglet',screen=3)
                                 
                                 
text0 = visual.TextStim(win0, "SCREEN INDEX 0", height=60, pos=[0,0], color="white")
text1 = visual.TextStim(win1, "SCREEN INDEX 1", height=60, pos=[0,0], color="white")
text2 = visual.TextStim(win2, "SCREEN INDEX 2", height=60, pos=[0,0], color="white")
text3 = visual.TextStim(win3, "SCREEN INDEX 3", height=60, pos=[0,0], color="white")

text0.draw()
text1.draw()
text2.draw()
text3.draw()

win0.flip()
win1.flip()
win2.flip()
win3.flip()

core.wait(5.0)

win0.close()
win1.close()
win2.close()
win3.close()

core.quit()