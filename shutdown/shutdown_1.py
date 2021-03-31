
import os

n = input("shutdown your compurter? (y or n) : ")

if n == 'y':
    # os.system("shutdown /l") # log off
    os.system("shutdown /s /t 0")