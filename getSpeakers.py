################################################################
# A quick python script to extract information about the various
# speakers in the SSPNet Corpus
# Input: Labels.txt file containing the instances of nonvocal communication
# Output: speakers.csv, csv file containing the speaker information
###################################################################




def main():
##    labels_file = open("labels.txt","r")
##    speakers = {}
##    line = labels_file.readline()
##    line = line.rstrip()
##    while(len(line) > 1):
##        lineTokens = line.split(",")
##        speaker = lineTokens[1]
##        gender = lineTokens[2]
##        role = speaker[-1]
##        infoArray = [speaker,gender,role]
##        if speaker not in speakers.keys():
##            speakers[speaker] = infoArray
##        line = labels_file.readline()
##        line = line.rstrip()
##    labels_file.close()
##    generateOutputFile(speakers)
##
    speakers = getSpeakersList("labels.txt")
    samples = getSpeakersSamples(speakers, "labels.txt")
    for speaker in speakers:
        print speaker, ",", samples[speaker]
    
def getSpeakersList(location):
    speakers = []
    f = open(location, 'r')
    line = f.readline()
    line = f.readline()
    line = line.rstrip()
    while len(line) > 1:
        lineTokens = line.split(",")
        speaker = lineTokens[1]
        if speaker not in speakers:
            speakers.append(speaker)
        line = f.readline()
        line = line.rstrip()
    f.close()
    return speakers
    
def getSpeakersSamples(speakers, location):
    speakerSamples= {}
    f = open(location, 'r')
    lines = f.readlines()
    for speaker in speakers:
        samples = []
        for line in lines:
            #print line
            line = line.rstrip()
            tokens = line.split(",")
            if tokens[1] == speaker and "laughter" in line:
             #   print line
                samples.append(tokens[0])
        speakerSamples[speaker] = samples
    f.close()
    return speakerSamples

        

def generateSpeakersFile(speakers):
    speakerCodes = speakers.keys()
    output = open("speakers.csv","w")
    for speaker in speakerCodes:
        line = ""
        line = line + speaker+","
        for item in speakers[speaker]:
            line = line + item + ","
        line = line + "\n"
        output.write(line)
    output.close()


if __name__ == "__main__":
    main()
