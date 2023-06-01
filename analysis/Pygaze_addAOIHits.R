

# LWL ---------------------------------------------------------------------

## AOI look locations ##

# face
#aoiFaceMinY=350
#aoiFaceMaxY=740
#aoiFaceMinX=880
#aoiFaceMaxX=1130
 
# objects
#aoiObjMinY=680
#aoiObjMaxY=1080

#aoiLeftMinX=350
#aoiLeftMaxX=790
#aoiRightMinX=1310
#aoiRightMaxX=1750


# View(gazedata[gazedata$TimeStamp==0,])


addAOI=function(gazedata) {
  
  original_dir = getwd()
  
  gazedata$Accuracy=NA
  

  # Add target object location for video trials
  
  #setwd("~/Box Sync/Dissertation/Experiment/Stimuli/Video/")
  #targetLocations=read.csv('Video Target Locations.csv')

  #gazedata$TargetObjectPos[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$TargetLocation=='L']] = 'Left'
  #gazedata$TargetObjectPos[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$TargetLocation=='R']] = 'Right'
  
  #gazedata$DistracterObjectPos[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$TargetLocation=='L']] = 'Right'
  #gazedata$DistracterObjectPos[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$TargetLocation=='R']] = 'Left'
  
  
  # And Images
  #gazedata$TargetImage[grepl('Tever',gazedata$ExposureVideo)] = 'Novel1'
  #gazedata$TargetImage[grepl('Juff',gazedata$ExposureVideo)] = 'Novel2'
  #gazedata$TargetImage[grepl('Rel',gazedata$ExposureVideo)] = 'Novel3'
  #gazedata$TargetImage[grepl('Blicket',gazedata$ExposureVideo)] = 'Novel4'
  #gazedata$TargetImage[grepl('Manu',gazedata$ExposureVideo)] = 'Novel5'
  #gazedata$TargetImage[grepl('Gip',gazedata$ExposureVideo)] = 'Novel6'
  #gazedata$TargetImage[grepl('Flower',gazedata$ExposureVideo)] = 'Flower'
  #gazedata$TargetImage[grepl('Book',gazedata$ExposureVideo)] = 'Book'
  #gazedata$TargetImage[grepl('Juice',gazedata$ExposureVideo)] = 'Juice'
  
  
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Apple']] = 'Apple'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Ball']] = 'Ball'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Bear']] = 'Bear'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Cake']] = 'Cake'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Cheese']] = 'Cheese'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Cookie']] = 'Cookie'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Duck']] = 'Duck'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Novel1']] = 'Novel1'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Novel2']] = 'Novel2'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Novel3']] = 'Novel3'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Novel4']] = 'Novel4'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Novel5']] = 'Novel5'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Novel6']] = 'Novel6'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Novel7']] = 'Novel7'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Novel8']] = 'Novel8'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Novel9']] = 'Novel9'
  #gazedata$DistracterImage[gazedata$ExposureVideo %in% targetLocations$Video[targetLocations$DistracterObject=='Truck']] = 'Truck'
  
  
  # And Audio
  #gazedata$Audio[grepl('Tever',gazedata$ExposureVideo)] = 'Tever' 
  #gazedata$Audio[grepl('Juff',gazedata$ExposureVideo)] = 'Juff'
  #gazedata$Audio[grepl('Rel',gazedata$ExposureVideo)] = 'Rel'
  #gazedata$Audio[grepl('Blicket',gazedata$ExposureVideo)] = 'Blicket'
  #gazedata$Audio[grepl('Manu',gazedata$ExposureVideo)] = 'Manu'
  #gazedata$Audio[grepl('Gip',gazedata$ExposureVideo)] = 'Gip'
  #gazedata$Audio[grepl('Tever',gazedata$ExposureVideo)] = 'Tever'
  #gazedata$Audio[grepl('Book',gazedata$ExposureVideo)] = 'Book'
  #gazedata$Audio[grepl('Flower',gazedata$ExposureVideo)] = 'Flower'
  #gazedata$Audio[grepl('Juice',gazedata$ExposureVideo)] = 'Juice'
  
  
  # And look AOI
  
  # if y coordinate of gaze is within the appropriate range: goodY=TRUE, otherwise goodY=FALSE
  #gazedata$goodY=NA
  #gazedata$goodY = ifelse((gazedata$GazePointYMean<=aoiObjMaxY)&(gazedata$GazePointYMean>=aoiObjMinY)&(!is.na(gazedata$GazePointYMean)),TRUE,FALSE)
  #gazedata$goodFaceY=ifelse((gazedata$GazePointYMean<=aoiFaceMaxY)&(gazedata$GazePointYMean>=aoiFaceMinY)&(!is.na(gazedata$GazePointYMean)),TRUE,FALSE)
      
  # if goodY & if the x coordinate of gaze is within the range of the left or right image: set LookAOI to 'bottomLeft' or 'bottomRight', else 'away'
  #gazedata$LookAOI=ifelse(!is.na(gazedata$GazePointXMean) & gazedata$goodY & gazedata$GazePointXMean >= aoiLeftMinX & gazedata$GazePointXMean <= aoiLeftMaxX, "Left",
                          #ifelse(!is.na(gazedata$GazePointXMean) & gazedata$goodY & gazedata$GazePointXMean >= aoiRightMinX & gazedata$GazePointXMean <= aoiRightMaxX, "Right",
                                # ifelse(!is.na(gazedata$GazePointXMean) & gazedata$goodFaceY & gazedata$GazePointXMean >= aoiFaceMinX & gazedata$GazePointXMean <= aoiFaceMaxX,"Face","away")))
  
  #gazedata$goodY[is.na(gazedata$ExposureVideo)]=NA
  #gazedata$goodFaceY[is.na(gazedata$ExposureVideo)]=NA
  #gazedata$LookAOI[is.na(gazedata$ExposureVideo)]=NA
  
  
  # Add look AOI for test trials
  # aoiMinY=78 (542)
  # aoiMaxY=578 (1042)
  # aoiLeftMinX=125
  # aoiLeftMaxX=625
  # aoiRightMinX=1295
  # aoiRightMaxX=1795
  gazedata$LookAOI[gazedata$trialType=='test' & gazedata$GazePointYMean>=542 & gazedata$GazePointYMean<=1042 & gazedata$GazePointXMean>=125 & gazedata$GazePointXMean<=625 ]= 'Left'
  gazedata$LookAOI[gazedata$trialType=='test' & gazedata$GazePointYMean>=542 & gazedata$GazePointYMean<=1042 & gazedata$GazePointXMean>=1295 & gazedata$GazePointXMean<=1795 ]= 'Right'
  
  gazedata$TargetObjectPos[gazedata$TargetObjectPos =='bottomLeft'] = 'Left'
  gazedata$TargetObjectPos[gazedata$TargetObjectPos =='bottomRight'] = 'Right'
  
  gazedata$DistracterObjectPos[gazedata$DistracterObjectPos =='bottomLeft'] = 'Left'
  gazedata$DistracterObjectPos[gazedata$DistracterObjectPos =='bottomRight'] = 'Right'
  
  
  
  # if LookAOI matches the position of the target image: Accuracy=1, if LookAOI matches the position of the distractor image: Accuracy=0, else NA
  gazedata$Accuracy=ifelse(gazedata$LookAOI == gazedata$TargetObjectPos,1,
                           ifelse(gazedata$LookAOI == gazedata$DistracterObjectPos,0,NA))
  

  # gazedata$TargetAcc=0
  # gazedata$TargetAcc[gazedata$LookAOI==gazedata$TargetObjectPos]=1
  # gazedata$TargetAcc[is.na(gazedata$LookAOI)]=NA
  # 
  # gazedata$DistracterAcc=0
  # gazedata$DistracterAcc[gazedata$LookAOI==gazedata$DistracterObjectPos]=1
  # gazedata$DistracterAcc[is.na(gazedata$LookAOI)]=NA
  # 
  # gazedata$FaceAcc=0
  # gazedata$FaceAcc[gazedata$LookAOI=='Face']=1
  # gazedata$FaceAcc[is.na(gazedata$LookAOI)]=NA
  
  setwd(original_dir)
  remove(targetLocations)
  
  # return the gazedata frame
  gazedata
}


# testing function
# temp <- addBinaryLookLocationTargetAOI(gazeDataComplete)
# head(temp[temp$goodY==FALSE,])
# head(temp[temp$subjCode==904 & temp$TrialNumber==2 & temp$TimeStamp >2050 & temp$TimeStamp<3850,])
# temp$LookLocationTargetAOI[temp$subjCode==i & temp$TrialNumber==j] = tolower(strsplit(toString(temp$TargetObjectPos[temp$subjCode==i & temp$TrialNumber==j][1]),"bottom")[[1]][2])



# split screen vertically -------------------------------------------------

# Screen split just based on X coordinates
# leftXLocation=350
# rightXLocation=1570
# XLenience=50
# imageSize=500

## apply appropriate screen location columns

# addBinaryLookLocationX=function(gazedata) {
#   extentLength=imageSize/2+XLenience
#   leftBoundary1=leftXLocation-extentLength
#   leftBoundary2=leftXLocation+extentLength
#   rightBoundary1=rightXLocation-extentLength
#   rightBoundary2=rightXLocation+extentLength
#   gazedata$LookLocationX=ifelse(gazedata$GazePointXMean>=leftBoundary1&gazedata$GazePointXMean<=leftBoundary2,"left",
#                                 ifelse(gazedata$GazePointXMean>leftBoundary2&gazedata$GazePointXMean<rightBoundary1,"middle",
#                                        ifelse(gazedata$GazePointXMean>=rightBoundary1&gazedata$GazePointXMean<=rightBoundary2,"right","off")))
#   gazedata
# }



# radius & rectangle AOIs -------------------------------------------------

#Active AOIs
# aoiCenterLeft=c(350,600)
# aoiCenterRight=c(1570,600)
# aoiCenterSize=500
# aoiCenterLenience=50
# aoiCenterType="rectangle"

# YumME AOIs
# aoiCenterLeft=c(375,791)
# aoiCenterRight=c(1545,791)
# aoiCenterWidth=650
# aoiCenterHeight=528
# aoiCenterLenience=0
# aoiCenterType="rectangle"


# contains=function(x,y,xradius,yradius,centerPointX,centerPointY,type="rectangle") {
#   if (type=="rectangle") {
#     xwithin=ifelse((x<=centerPointX+xradius)&(x>=centerPointX-xradius),TRUE,FALSE)
#     ywithin=ifelse((y<=centerPointY+yradius)&(x>=centerPointY-yradius),TRUE,FALSE)
#     output=ifelse(xwithin&ywithin,TRUE,FALSE)
#   } else if (type=="circle") {
#     radius=xradius
#     output=ifelse(sqrt((x-centerPointX)^2+(y-centerPointY)^2)<=radius,TRUE,FALSE)
#   }
#   output
# }

# addBinaryLookLocationTargetAOI=function(gazedata,aoiType=aoiCenterType) {
#   extentLength=aoiCenterSize/2+aoiCenterLenience
#   gazedata$LookLocationTargetAOI=NA
#   for (i in 1:length(gazedata$GazePointXMean)) {
#     gazedata$LookLocationAOI[i]=ifelse(contains(gazedata$GazePointXMean[i],gazedata$GazePointYMean[i],extentLength,extentLength,aoiCenterLeft[1],aoiCenterLeft[2],type=aoiType),"left",
#                                     ifelse(contains(gazedata$GazePointXMean[i],gazedata$GazePointYMean[i],extentLength,extentLength,aoiCenterRight[1],aoiCenterRight[2],type=aoiType),"right",NA))
#   }
#   gazedata
# }  


# NOTE !!! this function is broken - it marks fixations to the bottomLeft picture as NA...unable to determine why (RP)

# addBinaryLookLocationTargetAOI=function(gazedata,aoiType=aoiCenterType) {
#   # extentLength=aoiCenterSize/2+aoiCenterLenience
#   extentWidth=aoiCenterWidth/2+aoiCenterLenience
#   extentHeight=aoiCenterHeight/2+aoiCenterLenience
#   gazedata$LookLocationTargetAOI=NA
#   gazedata$Accuracy=NA
#   for (i in 1:length(gazedata$GazePointXMean)) {
#     gazedata$LookLocationAOI[i]=ifelse(contains(gazedata$GazePointXMean[i],gazedata$GazePointYMean[i],extentWidth,extentHeight,aoiCenterLeft[1],aoiCenterLeft[2],type=aoiType),"left",
#                                        ifelse(contains(gazedata$GazePointXMean[i],gazedata$GazePointYMean[i],extentWidth,extentHeight,aoiCenterRight[1],aoiCenterRight[2],type=aoiType),"right",NA))
#     
#     targetSide = tolower(strsplit(toString(gazedata$TargetObjectPos[i]),"bottom")[[1]][2])
#     if (!is.na(gazedata$LookLocationAOI[i])) {
#       if (gazedata$LookLocationAOI[i] == targetSide) {
#         gazedata$Accuracy[i]=1
#       } else {
#         gazedata$Accuracy[i]=0
#       }
#     }
#   }
#   gazedata
# }


