# Helper for Maxi

All the Functions I could need multiple times

## Instructions

1. Install:

```
pip install helper-for-maxi
```

2. Import package:

```python
from helper import *
OR
import helper
helper.*
# You can replace * with what you need!
``` 

## Currently Implemented Classes / Functions

appendClipboard()
```python
import helper
helper.appendClipboard(text: str)

OR

from helper import appendClipboard
appendClipboard(text: str)

# copies text
#
# Copies / Appends the given text to the windows clipboard using the utf-8 encoding
#
# Parameters
# ----------
# text: str
#     The text that is copied / appended to the clipboard
```

betterColorInput()
```python
import helper
helper.betterColorInput(text: str, beforeColor: Optional[Terminal.color.foreground] = Terminal.color.RESET, delay: float = .01)

OR

from helper import betterColorInput
betterColorInput(text: str, beforeColor: Optional[Terminal.color.foreground] = Terminal.color.RESET, delay: float = .01)

# Gets an input
# 
# Prints the given text letter by letter using the specified delay and gets an input() in cyan after
# 
# Parameters
# ----------
# text: Optional[str]
#     The text that is printed letter by letter
#     DEFAULT: None
# 
# beforeColor: Optional[Terminal.color.foreground]
#     The color to change back to after getting the input
#     DEFAULT: None
# 
# delay: Optional[float]
#     Changes the time between each printed letter
#     DEFAULT: .01
```

betterInput()
```python
import helper
helper.betterInput(text: str = "", delay: float = .01)

OR

from helper import betterInput
betterInput(text: str = "", delay: float = .01)

# Gets an input
# 
# Prints the given text letter by letter using the specified delay and gets an input() after
# 
# Parameters
# ----------
# text: Optional[str]
#     The text that is printed letter by letter
#     DEFAULT: ""
# 
# delay: Optional[float]
#     Changes the time between each printed letter
#     DEFAULT: .01
```

betterPrint()
```python
import helper
helper.betterPrint(text: str, delay: float = .01)

OR

from helper import betterPrint
betterPrint(text: str, delay: float = .01)

# Prints text
# 
# Prints the given text letter by letter to the command line using the specified delay
# 
# Parameters
# ----------
# text: str
#     The text that is printed letter by letter
# 
# delay: Optional[float]
#     Changes the time between each printed letter
#     DEFAULT: .01
# 
# newLine: Optional[bool]
#     whether to add a new line at the end or not
#     DEFAULT: True
```

colorInput()
```python
import helper
helper.colorInput(text: str = "", beforeColor: Optional[Terminal.color.foreground] = Terminal.color.RESET)

OR

from helper import colorInput
colorInput(text: str = "", beforeColor: Optional[Terminal.color.foreground] = Terminal.color.RESET)

# Gets an input
# 
# executes the input() function in cyan and changes the color back to beforeColor if given
# 
# Parameters
# ----------
# text: Optional[str]
#     The text that is printed before getting the input
#     DEFAULT: None
# beforeColor: Optional[Terminal.color.foreground]
#     The color that was used before (if u want it to change back)
#     DEFAULT: None
```

outputStdout()
```python
import helper
helper.outputStdout(outputValue)

OR

from helper import outputStdout
outputStdout(outputValue)

# Outputs to stdout
# 
# Outputs the given outputValue to stdout and flushes the stream after
# 
# Parameters
# ----------
# outputValue: Any
#     The value that's written to stdout
```

Terminal
```python
import helper
helper.Terminal._  # _ = subclass

OR

from helper import Terminal
Terminal._         # _ = subclass

# Functions & Stuff for the Windows Terminal
# 
# Contains classes and Functions to use for/in the Windows Terminal
# 
# Subclasses
# ----------
# color:
#     returns escape sequences to manipulate the color of the Terminal when printed
```