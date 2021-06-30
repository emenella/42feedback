#! /Users/emenella/.brew/bin/python3

with open("login.txt", "r") as txt_file:
  new_data = list(set(txt_file))
  for p in new_data:
    print(p, end='')