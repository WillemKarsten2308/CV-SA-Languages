import argparse
import array

parser = argparse.ArgumentParser(description='CompareParser')

parser.add_argument("-c", "--compare", help="File name of LID Output", required=True)
parser.add_argument("-i", "--input", help="Input file to run against LID output", required=True)
parser.add_argument("-o", "--output", help="Output file after cleaning with LID", default="Clean_Output.txt")
parser.add_argument("-l", "--language", help="Correct language, all others will be discarded", required=True)

args = parser.parse_args()

i = 0
n = 0
u = 0
errWords = []
errors = array.array('L', [])

file = open(args.compare)

for lang in file.readlines():
    i += 1
    if args.language in lang:
        print(i, ": Correct")
    else:
        print(i, ": Error")
        errors.append(i)
   # print(i)

file.close()

errLen = errors.__len__()

with open(args.input, "r") as myFile:
    lines = myFile.readlines()
with open(args.output, "w") as myOut:
    for line in lines:
        n += 1
        # print("FLAG!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        if n != errors[u]:
            myOut.write(line)
        else:
            if u < errLen - 1:
                u += 1
print("Total Errors: ", errLen)
