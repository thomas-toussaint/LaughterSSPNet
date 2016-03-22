import math
import matplotlib.pyplot as plt

def main():
    voicedCount = getCount("C:\\Users\\Thomas\\Desktop\\Project\\InPython\\Query Results\\speakersVoiced.csv")
    unvoicedCount = getCount("C:\\Users\\Thomas\\Desktop\\Project\\InPython\\Query Results\\speakersUnvoiced.txt")
    totalCount = getCount("C:\\Users\\Thomas\\Desktop\\Project\\InPython\\Query Results\\count.csv")
    entropies = []
    normed = []
    for speaker in totalCount.keys():
        total = totalCount[speaker]
        if total > 1:
            if speaker in voicedCount.keys():
                voiced = voicedCount[speaker]
            else:
                voiced = 0
            entropy = calculateEntropy(voiced, total)
            entropies.append(entropy)
            norm = calculateHnorm(entropy, total)
            normed.append(norm)
    print normed
    print getMean(normed)
    # get only entropy above 0:
    nonZero = []
    for instance in entropies:
        if instance != 0:
            nonZero.append(instance)
    print getMean(entropies)
    print getMean(nonZero)
    #generateHistogram(entropies, "Entropy measure for each speaker", "H", "Count")

def getCount(location):
    count = {}
    f = open(location, 'r')
    f.readline()
    line = f.readline()
    line = line.rstrip()
    while len(line) > 1:
        tokens = line.split(";")
        count[tokens[0]] = int(tokens[1])
        line = f.readline().rstrip()
    f.close()
    return count

def calculateEntropy(voicedCount,totalCount):
    p_voiced = float(voicedCount)/totalCount
    p_unvoiced = 1 - p_voiced
    if p_unvoiced != 0 and p_voiced != 0 :
        h = -p_voiced * math.log(p_voiced)- p_unvoiced * math.log(p_unvoiced)
    else:
        h = 0
    return h

def calculateHnorm(entropy, totalCount):
    normed = entropy/(-totalCount * math.log(totalCount))
    return normed

def generateHistogram(data, title,xAxis,yAxis):
    plt.figure()
    plt.title(title)
    plt.hist(data)
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.show()

def getMean(data):
    length = len(data)
    total = 0.0
    for datum in data:
        total += datum
    return total/length


if __name__ == "__main__":
    main()
