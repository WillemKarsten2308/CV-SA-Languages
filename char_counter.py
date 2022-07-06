import argparse

parser = argparse.ArgumentParser(description='AverageChars')

parser.add_argument("-l", "--langPath", help="Language file to analyze", required=True)

args = parser.parse_args()

with open(args.langPath, 'r') as myFile:
    lines = myFile.readlines()

    print(sum(len(line) for line in lines)/len(lines))

myFile.close()
