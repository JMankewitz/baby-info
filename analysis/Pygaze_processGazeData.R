##############################################
#Functions for processing gaze data output of
#pygaze experiment (.tsv file)
#############################################

#The .tsv file output in pygaze contains gaze data info as well event data logged during the experiment.
#These functions help in integrating the logged event and the gaze data after the experiment.
#functions overview:
#integrateEventData: integrates logged event data, puts all of the data together
#processGazeData: replace missing values with NA, compute means of left and right eye coordinates
#createTimeBins: adds unified time bins in addition to "noisy" timestamp column
#mergeTrialList: merge each trial with its trial info from a trial list

#necessary packages
require(gtools)


# gazedatafileName = "YumME_105_TOBII_output.tsv"
# skipNum=11

integrateEventData=function(gazedatafileName,skipNum=11) {
  #gazedatafile: .tsv file of gazedata
  #skipNum: number of lines to skip (header lines)
  d=read.csv(gazedatafileName,sep="\t", skip=skipNum)
  #pygaze prints the columns names prior to each trial start
  rowNumTrialStart=as.numeric(rownames(d[grepl("TimeStamp",d$TimeStamp),]))
  #columns as numeric values, not factors
  d$TimeStamp=suppressWarnings(as.numeric(as.character(d$TimeStamp)))
  #may throw a warning message: NAs introduced by coercion
  #This is nothing to worry about.
  #that's why warning is suppressed
  #Convert other eyetracking columns to numeric values
  d$GazePointXLeft=suppressWarnings(as.numeric(as.character(d$GazePointXLeft)))
  d$GazePointYLeft=suppressWarnings(as.numeric(as.character(d$GazePointYLeft)))
  d$ValidityLeft=suppressWarnings(as.numeric(as.character(d$ValidityLeft)))
  d$GazePointXRight=suppressWarnings(as.numeric(as.character(d$GazePointXRight)))
  d$GazePointYRight=suppressWarnings(as.numeric(as.character(d$GazePointYRight)))
  d$ValidityRight=suppressWarnings(as.numeric(as.character(d$ValidityRight)))
  d$GazePointX=suppressWarnings(as.numeric(as.character(d$GazePointX)))
  d$GazePointY=suppressWarnings(as.numeric(as.character(d$GazePointY)))
  
  #event as character column
  d$Event=as.character(d$Event)
  
  ########create new columns containing the trial info#######
  #get trial info for each trial number
  #the first event logged for each trial is info about experiment, trial number, trial type and subject code
  #Example:"experiment ALC subjCode p101 TrialNumber 1 TrialType active"
  trialInfo=strsplit(as.character(d[rownames(d[grepl("TrialNumber",d$Event),]),"Event"]), split=" ")
  #the output is a list of lists
  #the first level of the list will be the trial number
  #for each trial number, there is a vector containing trial info and its corresponding value
  trialNum=length(trialInfo)
  
  #tag columns as being logging events or actual eyetracking events
  d$LoggingEvent=ifelse(d$GazePointX=="GazePointX",NA,
                        ifelse(d$GazePointX=="",1,0))
  
  #adds a column for each kind of trial info stored and adds info to the appropriate row
  eventColumnList=c()
  for (j in 1:trialNum) {
    for (i in 1:(length(trialInfo[[j]])/2)) {
      if (!(trialInfo[[j]][2*i-1] %in% eventColumnList)) {
        eventColumnList=c(eventColumnList,trialInfo[[j]][2*i-1])
      }
    }
  }
  
  for (column in 1:length(eventColumnList)) {
    d[,eventColumnList[column]]=0
    for (tNum in (1:trialNum)) {
      #add OverallTrialNum column (used later to fill in Event column appropriately)
      if (tNum==1) {
        
        d[as.numeric(rownames(d))<rowNumTrialStart[tNum],"OverallTrialNum"]=tNum
      } else {
        d[as.numeric(rownames(d))>rowNumTrialStart[tNum-1],"OverallTrialNum"]=tNum
      }
      
      if (eventColumnList[column] %in% trialInfo[[tNum]]) {
        if (tNum==1) {
          d[as.numeric(rownames(d))<rowNumTrialStart[tNum],eventColumnList[column]]=as.character(trialInfo[[tNum]][match(eventColumnList[column],trialInfo[[tNum]])+1])
        } else {
          d[as.numeric(rownames(d))>rowNumTrialStart[tNum-1],eventColumnList[column]]=as.character(trialInfo[[tNum]][match(eventColumnList[column],trialInfo[[tNum]])+1])
        } 
      } else {
          if (tNum==1) {
            d[as.numeric(rownames(d))<rowNumTrialStart[tNum],eventColumnList[column]]=NA
          } else {
            d[as.numeric(rownames(d))>rowNumTrialStart[tNum-1],eventColumnList[column]]=NA
          }
        }
      }
  }
  
  ####add event data####
  #subset the data to just the event info (without the trial info)
  #including TimeStamp, Event, TrialNumber & TrialType
  events=subset(d,Event!=""&Event!="Event"&!grepl("TrialNumber",Event), select=c("TimeStamp", "Event", "TrialNumber", "trialType","OverallTrialNum"))
  #remove columns from dataframe with recorded events
  d=d[d$LoggingEvent==0&!is.na(d$LoggingEvent),]
  # RP: changed 1 to 17
  # for (i in 17:trialNum) {
  for (i in unique(events$OverallTrialNum)) {
    for (j in 1:length(subset(events, OverallTrialNum==i)$TimeStamp)) {
      d[d$OverallTrialNum==i,as.character(subset(events, OverallTrialNum==i)$Event[j])]=subset(events, OverallTrialNum==i)$TimeStamp[j]
      d$Event[d$TimeStamp>subset(events, OverallTrialNum==i)$TimeStamp[j]&d$OverallTrialNum==i]=as.character(subset(events, OverallTrialNum==i)$Event[j])
    }
  }
  
  #convert Block and Trial Number to numeric vectors
  # d$Block=suppressWarnings(as.numeric(as.character(d$Block)))
  d$TrialNumber=suppressWarnings(as.numeric(as.character(d$TrialNumber)))
  
  
  return(d)
}



processGazeData=function(gazedata,output_file=NULL) {
  
  #Transform all values marked as -1 (missing data) to NA
  # Replace all values of gazedata that fall outside of [0, 1] with NA.
  CorrectInvalidGazes = function(gaze) {
    gaze[(gaze < 0)] <- NA
    gaze
  }
  
  gazedata <- within(gazedata, {
    GazePointXLeft <- CorrectInvalidGazes(GazePointXLeft)
    GazePointXRight <- CorrectInvalidGazes(GazePointXLeft)
    GazePointYLeft <- CorrectInvalidGazes(GazePointYLeft)
    GazePointYRight <- CorrectInvalidGazes(GazePointYRight)
    GazePointX <- CorrectInvalidGazes(GazePointX)
    GazePointY <- CorrectInvalidGazes(GazePointY)
  })
  
  ####Computing mean gaze locations####
  #1. correct error in pygaze libtobii.py
  #GazePointX and GazePointY are the averages of the left and right gaze coordinates
  #in proportion of screen size. However, libtobii fails to divide them by 2.
  #2. compute averages for X and Y coordinates that are adjusted to display size
  #GazePointXLeft, GazePointXRight, GazePointYLeft, GazePointYRight
  # Compute the mean gaze values.
  ComputePairMeans <- function(x1, x2) rowMeans(cbind(x1, x2), na.rm = TRUE)
  gazedata <- within(gazedata, {
    GazePointX <- GazePointX/2
    GazePointY <- GazePointY/2
    GazePointXMean <- ComputePairMeans(GazePointXLeft, GazePointXRight)
    GazePointYMean <- ComputePairMeans(GazePointYLeft, GazePointYRight)
  })
  
  #add column that tracks whether a full look (X and Y coordinate) was tracked
  gazedata$isLook=ifelse(is.na(gazedata$GazePointXMean)|is.na(gazedata$GazePointYMean),NA,1)
  
  # Optionally write out the gazedata data frame.
  if (!is.null(output_file)) {
    write.table(gazedata, file = output_file, sep = ',',
                quote = FALSE, row.names = FALSE)
  }
  
  gazedata
}

createTimeBins=function(gazedata,ms_per_frame=1000/60) {
  #Bin TimeStamps with slight ms level variations on different trials into time bins
  gazedata$TimeBin=round(gazedata$TimeStamp/ms_per_frame,0)
  
  #Create ms equivalents of time bins
  gazedata$TimeBinMs=gazedata$TimeBin*ms_per_frame
  
  gazedata
}