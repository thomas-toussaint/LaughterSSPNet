#Praat script to extract GeMAPS features from all files in a directory

#Choose folder
 form Files
	 sentence inputDir C:\Users\Thomas\Desktop\Project\InPython\all\
	 sentence outputFile C:\Users\Thomas\Desktop\Project\InPython\all\halfresults.txt
 endform

 Create Strings as file list... list 'inputDir$'*.wav

numberOfFiles = Get number of strings
titleline$ = "Filename Pitch Jitter F1 F2 F3 F1_Bandwidth Shimmer Intensity HNR 'newline$'"
fileappend "'outputFile$'" 'titleline$'

for ifile to numberOfFiles

	select Strings list
	fileName$ = Get string... ifile
	Read from file... 'inputDir$''fileName$'
	soundname$ = selected$ ("Sound", 1)
	
	#Get formant information
	To Formant (burg)... 0 5 5500 0.025 50
	f1 = Get mean... 1 0 0 Hertz
	f2 = Get mean... 2 0 0 Hertz
	f3 = Get mean... 3 0 0 Hertz
	f1b = Get quantile of bandwidth... 1 0 0 "Hertz" 0.5
	
	selectObject: "Sound 'soundname$'"
	To Spectrum: "yes"
	spectral_slope = Get band energy difference: 0, 500, 500, 1500
	
	#Get voiced related information
	selectObject: "Sound 'soundname$'"
	soundlength = Get total duration
	i = Get intensity (dB)
	View & Edit
	editor: "Sound 'soundname$'"
		Select: 0, soundlength
		minPitch = Get minimum pitch
		pceiling = Get maximum pitch
	endeditor
	
	
	pceiling = pceiling * 1.5
	if minPitch <> undefined
		selectObject: "Sound 'soundname$'"
		To Pitch... 0 minPitch pceiling
		voiced = Count voiced frames
		if voiced > 0 
		
		#Check range of pitch
			if minPitch > 75
				minPitch = 75
			else
				minPitch = minPitch/2
				if minPitch <2.6
					minPitch = 2.6
				endif
			endif
		

			f0 = Get mean... 0 0 Hertz
			selectObject: "Sound 'soundname$'"
			To Harmonicity (cc): 0.01, minPitch, 0.1, 1
			hnr = Get mean... 0 0
			selectObject: "Sound 'soundname$'"
			plusObject: "Pitch 'soundname$'"
			To PointProcess (cc)
			plusObject: "Pitch 'soundname$'"
			plusObject: "Sound 'soundname$'"
	
		
			voiceReport$ = Voice report: 0, 0, minPitch, pceiling, 1.3, 1.6, 0.03, 0.45
			shimmer = extractNumber (voiceReport$, "Shimmer (local): ")
			jitter = extractNumber (voiceReport$, "Jitter (local): ")
		else 
			f0 = 0
			hnr = 0
			jitter = 0
			shimmer = 0
		
		endif
		else 
			f0 = 0
			hnr = 0
			jitter = 0
			shimmer = 0
		
	endif
	selectObject: "Sound 'soundname$'"
	
	#Get spectrum information
	
	appendLine$ = "'soundname$','f0','jitter','f1','f2','f3','f1b','shimmer','i','hnr','newline$'"
	fileappend "'outputFile$'" 'appendLine$'
	select all
	minus Strings list
	#minus Sound fileName$
	Remove
endfor
select all
Remove