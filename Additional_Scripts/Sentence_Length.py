import argparse

parser = argparse.ArgumentParser(description='CountingWordsParser')

parser.add_argument("-i", "--input", help="Input file to analyze", required=True)
parser.add_argument("-o", "--output", help="File to write results to", default="Generated_Stats.txt")

args = parser.parse_args()

total = 0
numSent = 0
maxCount = 0

myFile = open(args.input)

for line in myFile.readlines():
    countOfWords = len(line.split())
    print(line, ": Number of Words: ", countOfWords)
    total = total + countOfWords
    numSent += 1

    if maxCount < countOfWords:
        maxCount = countOfWords

myFile.close()

aveWords = total/numSent
print("Total amount of Words:", total)
print("Total Number of Sentences: ", numSent)
print("Longest Sentence: ", maxCount)
print("Average number of words per sentence: ", aveWords)

myOut = open(args.output, "w")

myOut.write("Total amount of Words:" + str(total) + "\n")
myOut.write("Total Number of Sentences: " + str(numSent) + "\n")
myOut.write("Longest Sentence: " + str(maxCount) + "\n")
myOut.write("Average number of words per sentence: " + str(aveWords) + "\n")

myOut.close()
