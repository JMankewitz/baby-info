
Broad Experiment Steps:

- Load all packages
- Preload videos and stimuli images
- Set AOIs and stimuli locations
- Read trial info
- For each training trial
	- Find correct speaker video
	- Find correct stimuli and side
	- Pause until speaker start - total time
	- Play video until end of video, pause until silence variable - end silence
	- Track gaze to AOIs
- For each test trial
	- Find correct speaker images
	- Place speaker images
	- Wait until gaze in AOI
	- Change image to color
	- Loop sound for max of 20 seconds

05/10 Goals:
Get video(s) to play in /some/ order, ignoring eyetracking requirements

DONE!

mp4 -> .mp3 conversion 

1) for each video file, convert to mp3

for vid in *.mp4; do ffmpeg -i "$vid" -vn -c:a libmp3lame "${vid%.mp4}.mp3"; done

2) for each mp3, convert to 44100HZ

for i in *.mp3; do ffmpeg -i "$i" -ar 44100 -ac 1 "${i%.mp3}-encoded.mp3"; done  

Tomorrow: Attention getters and basic eye tracking

Friday: gaze contingent trials 

Bonus: fade in and out


Dolphin screen size: (1024,768)
Size of images: (452, 646)


4 Trial Types 

1) Attention grabber (start, after active training, middle of familiarization, between active test?

2) activeTraining (gaze contingent phase with just speakers going "hi baby!") 

3) familiarizationTrials (speaker familiarization)

4) activeTest (gaze contingent with novel object)


Eyetracker should log:

"Experiment %s subjCode %s Phase %sTrialNumber %d"


