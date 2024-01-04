# encode_icon.py
# Add 'pyperclip==1.8.2' to requirements.txt *only* if you need to change the bundled icons
# Usage:- 'python encode_icon.py icon-16.png'

from base64 import b64encode
import sys
import pyperclip

filename = sys.argv[1]
with open(filename, "rb") as f:
    pyperclip.copy(b64encode(f.read()).decode("ascii"))
    print("Copied to clipboard.")
