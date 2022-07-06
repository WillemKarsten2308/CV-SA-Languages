import re
import argparse

parser = argparse.ArgumentParser(description='RemoveRegexParser')

parser.add_argument("-i", "--input", help="File to process", default="NO",required=False)
parser.add_argument("-o", "--output", help="File to write results to", default="removed_braces.txt")
parser.add_argument("-r", "--regex", help="The regular expression to remove", default="^\(.*?\)")

args = parser.parse_args()

string="(Bracket stuff) and other Stuff (more brackets) and some final stuff"

string=re.sub(args.regex, "", string)
print(string)

if args.input != "NO":
    myFile = open(args.input)
    myOut = open(args.output, "w")
    for line in myFile.readlines():
        line=re.sub(args.regex, "", line)
        myOut.write(line)

else:
    print("No file specified")
