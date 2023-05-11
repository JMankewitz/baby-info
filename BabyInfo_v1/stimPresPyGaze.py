"""These are pygaze specific functions and rely on pygaze modules and presentation systems"""
from pygaze import libscreen
from pygaze import libtime


def buildScreenPsychoPy(screen, stimuli):
	"""Adds psychopy stimuli to a screen"""
	"""Stimuli can be a list or a single draw-able stimulus"""
	if type(stimuli).__name__ == "list":
		for curStim in stimuli:
			screen.screen.append(curStim)
	else:
		screen.screen.append
	return


def setAndPresentScreen(display, screen, duration=0):
	"""Sets display with a given screen and displays that screen"""
	"""duration can be set to a specific time to display screen for"""
	"""otherwise, the function returns immediately (duration=0)"""
	display.fill(screen)
	if duration == 0:  # single frame
		display.show()
	else:
		display.show()
		# relies on pygaze's libtime module
		libtime.pause(duration)
