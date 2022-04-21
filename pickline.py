#! /Users/emenella/.brew/bin/python3
import random
import sys
import os
  
# Open the file in read mode
with open(sys.argv[1], "r") as file:
    allText = file.read()
    words = list(map(str, allText.split('\n')))
  
    # print random string
    print(random.choice(words))
