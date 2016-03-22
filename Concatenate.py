import wave
import sys
import glob
import os
###############################################################################
## Author: Thomas Toussaint                                                  ##
## A Python module to collect all laughter instances in the corpus           ##
## And output them as one single wav file                                    ##
## This is largely done by 3 functions:                                      ##
## The first reads the label file and returns the file and the timestamps    ##
## where laughter is present                                                 ##
## The second splices the audio file where indicated by the first file       ##
## The third takes all the splices and concatenates them                     ##
###############################################################################


def main():
    
    #Get the list of all instances of laughter from the txt file
    labels_file = open("labels.txt", "r") #Hard coded for now, make it something more flexible in the future
    line = labels_file.readline()
    line = line.rstrip()
    instances = list()
    while(len(line) > 1):
        instance = laughterFinder(line)
        if instance is not None:
            instances.append(instance)
        line = labels_file.readline()
        line = line.rstrip()
    labels_file.close()

    #Get all the instances of laughter in a folder
    os.mkdir("Spliced")
    for instance in instances:
        wav_Location = "data\\"+instance[0]+".wav" #Hard coded for now
        for i in xrange(1, len(instance),2):
            new_Location = "Spliced\\"+instance[0]+"_instance_{0}.wav".format(i)
            wavSplicer(wav_Location, instance[i], instance[i+1], new_Location)

    #Now to concatenate all the splices
    toMerge = glob.glob("Spliced\\*.wav")
    wavAppender(toMerge, "joined.wav")

    
            
                
            

def laughterFinder(line):
    """Given a line from the labels reader, returns an array containing file name, and all instances of laughter indicated in that file"""

    lineTokens = line.split(",")
    AudioFileName = lineTokens[0]
    laughterInstances = list()
    laughterInstances.append(AudioFileName)

    for i in xrange(0, len(lineTokens)):
        if lineTokens[i] == "laughter":
            laughterInstances.append(float(lineTokens[i+1]))
            laughterInstances.append(float(lineTokens[i+2]))
            
    if len(laughterInstances) > 1:
        return laughterInstances
    else:
        return None

def wavSplicer(wav_Location, start, end, newName):
    """Given the location of a wave file, creates a splice of the file from start to end specified"""

    try :
        waveReader = wave.open(wav_Location, 'r')
        waveWriter = wave.open(newName, 'w')
    except:
        print "error opening file in waveSplicer",sys.exc_info()[0]
        raise
    
    waveWriter.setnchannels(waveReader.getnchannels())
    waveWriter.setsampwidth(waveReader.getsampwidth())
    waveWriter.setframerate(waveReader.getframerate())
    #Not using setparams because of the nframes field not matching

    startSample = int(start * waveReader.getframerate())
    endSample = int(end * waveReader.getframerate())
    waveReader.readframes(startSample*waveReader.getnchannels()) # get to right position
    toSplice = waveReader.readframes(endSample - startSample * waveReader.getnchannels())
    waveWriter.writeframes(toSplice) #This may be one of the most expensive operations in this script
    waveReader.close()
    waveWriter.close()

#With help from StackOverflow
def wavAppender(filesToMerge, newFileName):

    data = []
    
    for fileToMerge in filesToMerge:
        w = wave.open(fileToMerge, 'r')
        data.append( [w.getparams(), w.readframes(w.getnframes())])
        w.close()

    output = wave.open(newFileName, 'w')
    output.setparams(data[0][0])
    #print data[0][0]
    
    for i in xrange(0, len(data)):
        output.writeframes(data[i][1])
        #add 2 seconds of silence
        numFrames = data[0][0][2] * 2
        output.writeframes(chr(0) * numFrames)
        
    output.close()
    

if __name__ == "__main__" :
    main()
