
window=300
ms_per_frame=(1000/60)
# Convert window duration (ms) into the number of frames, rounded down.
frames_in_window <- floor(window /ms_per_frame)


# Simple container for the information we care about when interpolating a gap
Gap <- function(start, end, na_size) {
  structure(list(
    start = start, end = end, na_size = na_size,
    seq = seq(start, end), na_seq = seq(start + 1, end - 1)),
    class = c("Gap", "list"))
}


# Interpolate a single gap
fill_gap <- function(trial, gap,AOIs) {
  trial$LookAOI[gap$na_seq]=AOIs[gap$start]
  trial$numInterpolatedPoints[gap$na_seq]=gap$na_size
  trial$isInterpolatedFrame[gap$na_seq]=1
  trial
}

# sub='559'
# trial = c(32,33)

# trial=d[d$subjCode==sub & d$TrialNumber==trial,]
# trial$Accuracy[trial$trialID==32 & trial$TimeBin==432] = 1
# trial$Accuracy[trial$trialID==33 & trial$TimeBin==3] = 1
# 
# trial$numInterpolatedAOIPoints=0
# trial$isInterpolatedAOIFrame=0


# trial[2672:2676,]
# accuracies[2672:2676]
# AOIs[2672:2676]

# For each trial

# Tidyverse this
InterpolateMissingAOI = function(trial) {
  trial$LookAOI[trial$LookAOI=='off']=NA
  trial$numInterpolatedPoints=0
  trial$isInterpolatedFrame=0
  trial$isTracked = 'yes'
  trial$isTracked[is.na(trial$LookAOI)]= NA
  # Extract the gazes from the trial. Record how many missing frames there are.
  accuracies = trial$LookAOI # was 1 or 0 for target or distractor, need to generalize to >2 AOIs
  AOIs = trial$LookAOI
  trialnums = trial$trial_type_id
  gazes <- trial$isTracked
  missing <- sum(is.na(AOIs))
  # Grab all the non-NA gaze frames.
  tracked <- which(!is.na(AOIs))
  # The lag in frame numbers of non-NA gazes tells us how many NA frames were
  # skipped when we extracted all the non-NA gazes. Include the 0 at front
  # because diff(1:n) returns n-1 values
  differences <- diff(c(0, tracked))
  ## Find starts and ends of each NA gap
  # Locations from `which` are not accurate because they don't take into account
  # earlier missing frames. Use the cumulative sum of missing frames to correct
  # these start locations.
  gap_start <- which(1 < differences)
  gap_size <- differences[gap_start] - 1
  total_gap_sizes <- cumsum(gap_size)
  # First gap doesn't need to be offset
  start_offsets <- c(0, total_gap_sizes[-length(total_gap_sizes)])
  gap_start <- gap_start + start_offsets - 1
  gap_end <- gap_start + gap_size + 1
  # Enforce valid windows! Margins need to be non-NA and next to an NA value
  stopifnot(is.na(AOIs[c(gap_start + 1, gap_end - 1)]),
            !is.na(AOIs[c(gap_start, gap_end)]))
  # Make a set of Gap objects from these start/end/size descriptions
  gaps <- Map(Gap, gap_start, gap_end, gap_size)
  # Only fill gaps no bigger than the interpolation window, gaps that don't
  # involve first frame and gaps with the gaze location on both sides of window
  has_legal_length <- function(gap) gap$na_size <= frames_in_window
  is_not_first_frame <- function(gap) gap$start != 0
  is_fillable <- function(gap) AOIs[gap$start] == AOIs[gap$end] # start and end of gap are same AOI
  is_same_trial <- function(gap) trialnums[gap$start] == trialnums[gap$end] # within the same trial
  gaps <- Filter(has_legal_length, gaps)
  gaps <- Filter(is_not_first_frame, gaps)
  gaps <- Filter(is_fillable, gaps)
  gaps <- Filter(is_same_trial,gaps)
  # Fill each gap
  for (gap in gaps) {
    trial <- fill_gap(trial, gap,AOIs)
  }
  trial
}



