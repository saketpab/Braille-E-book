import sys
import time
from wheelObject import Wheel

wheel_left = Wheel()
wheel_right = Wheel()

# Pass word with script in command line/terminal (or sentence in quotes when running script)
# example: script.py "Tim Sucks"
word_to_translate = sys.argv[1]


def spin_wheels(braille_code):
    for col1, col2 in braille_code:
        wheel_left.spin_wheel(col1)
        time.sleep(0.2)
        wheel_right.spin_wheel(col2)
        time.sleep(0.2)