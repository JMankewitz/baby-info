

# Load libraries ----------------------------------------------------------

setwd("~/Documents/Wisconsin-Madison/01 Lab/Studies/Context/Pilot/Data Processing/libraries")

source("Pygaze_processGazeData.R")
source("Pygaze_addAOIHits.R")
source("Pygaze_InterpolateAOIHits.R")

setwd("~/Documents/Wisconsin-Madison/01 Lab/Studies/Context/Pilot/Data Processing/tobii")

library(tidyverse)


# load and process raw data -----------------------------------------------

# get all of the names of files in the current directory and put them in a vector
gazeDataNames=list.files(pattern=".tsv")

# create an empty dataframe
gazeDataComplete=c()

for (i in 1:length(gazeDataNames)) {
  # print(paste('Starting...',gazeDataNames[i]))
  gaze=integrateEventData(gazeDataNames[i])  #load gazedata and clean appropriately (function from Pygaze_processGazeData.R)
  gaze=processGazeData(gaze)   #additional function to clean gaze coordinates (function from Pygaze_processGazeData.R)
  gaze=createTimeBins(gaze)  #create unified time bins
  gaze=addAOI(gaze)   #add AOI columns
  gaze=InterpolateMissingAOI(gaze)  #interpolate missing frames
  if (i==1) {gazeDataComplete=gaze} else {gazeDataComplete=smartbind(gazeDataComplete,gaze)}
  print(paste(i,'out of',length(gazeDataNames),'complete:',gazeDataNames[i]))
}

system("say complete!")

colsToKeep = c('subjCode','famList','TimeBin','TimeBinMs','OverallTrialNum','TrialNumber','trialType','BlockID','Condition','Audio','TargetImage','TargetObjectPos','DistracterImage','DistracterObjectPos','Accuracy','GazePointXMean','GazePointYMean','LookAOI','isInterpolatedFrame','numInterpolatedPoints')
gazeDataComplete = gazeDataComplete %>% select(colsToKeep)


# fix missing information -------------------------------------------------


## filter out non-test trials ##
gazeDataComplete <- gazeDataComplete %>% filter(trialType == "test")


## center time ##
# test trials: 1500 (silence) + 800 (carrier) + 100ms (python lag) = 2400
gazeDataComplete$TimeC = gazeDataComplete$TimeBinMs
gazeDataComplete$TimeC[gazeDataComplete$trialType=='test']=gazeDataComplete$TimeC[gazeDataComplete$trialType=='test']-2400



# adjust time for teaching trials, because the eyetracker began recording 500 ms before the actual onset of the trial
# because of the 500ms lag in loading the video (make this match the actual time lag)
# gazeDataComplete$TimeBinMs[gazeDataComplete$trialType=='teaching'] = gazeDataComplete$TimeBinMs[gazeDataComplete$trialType=='teaching']-500


## fix condition ##
# gazeDataComplete$Condition[gazeDataComplete$trialType=='test' & gazeDataComplete$famList==1 & gazeDataComplete$BlockID==1]='Gaze'
# gazeDataComplete$Condition[gazeDataComplete$trialType=='test' & gazeDataComplete$famList==1 & gazeDataComplete$BlockID==2]='ME'
# gazeDataComplete$Condition[gazeDataComplete$trialType=='test' & gazeDataComplete$famList==1 & gazeDataComplete$BlockID==3]='GazeME'

# gazeDataComplete$Condition[gazeDataComplete$trialType=='test' & gazeDataComplete$TrialNumber%in%c(1,9,17)]='Familiar'
# gazeDataComplete$Condition[gazeDataComplete$trialType=='test' & gazeDataComplete$TrialNumber%in%c(8,16,24)]='Filler'

## fix block ID
# gazeDataComplete$BlockID[gazeDataComplete$trialType=='teaching' & gazeDataComplete$TrialNumber <= 5]=1
# gazeDataComplete$BlockID[gazeDataComplete$trialType=='teaching' & gazeDataComplete$TrialNumber >= 6 & gazeDataComplete$TrialNumber <= 10]=2
# gazeDataComplete$BlockID[gazeDataComplete$trialType=='teaching' & gazeDataComplete$TrialNumber >= 11]=3


# gazeDataComplete = gazeDataComplete %>% filter(Condition !='Filler')


# d.raw = d


## subset & rename variables ##
gazeDataComplete = gazeDataComplete %>% select(subjCode,famList,OverallTrialNum,BlockID,trialType,Condition,Audio,TargetImage,TargetObjectPos,DistracterImage,TimeBin,TimeBinMs,TimeC,GazePointXMean,GazePointYMean,Accuracy,LookAOI)

# rename column headers
colnames(gazeDataComplete) <- c('Sub.Num','Order','Tr.Num',"Block","Phase",'Condition',"Audio",'Target','Target.Side','Distractor','TimeBin','Time','TimeC','GazePointXMean','GazePointYMean','Accuracy','AOI')


# save gaze data as txt file ----------------------------------------------

write.csv(gazeDataComplete, file='Context_Pilot_TobiiData.csv')




