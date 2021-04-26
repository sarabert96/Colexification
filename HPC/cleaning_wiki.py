import re
import sys

wiki_name = sys.argv[1] # taking argument from bash

name = "clear_" + wiki_name
text_mod = open(name,'a')
with open(wiki_name, 'r') as fileinput:
  consider = True
  for line in fileinput:
    line = line.lower()
    if consider: # to skip one line after <doc> tag
      if "<doc" in line:
        consider = False
        continue
      if "</doc>" in line or line=="\n":
        continue # do nothing but continue for loop
      else:
        line = re.sub(r'http.*\/\/.+\/*','', line) # website
        line = re.sub(r'www.*','', line) # website
        line = re.sub(' +', ' ', line) # multiple spaces
        line = re.sub(r'[^\w\s]','', line) # punctuation
        text_mod.write(line)
    else:
      consider = True
text_mod.close()