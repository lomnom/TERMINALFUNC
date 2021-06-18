# TERMINALFUNC, a python library with every terminal manuplation function you will ever need!
## Attributes:
- ***func*** `stopSleep()`: stop idle sleep while current process exists. Only works on OSX
- ***func*** `getPosition()`: get current cursor position. Position is returned in `{"row":row, "column":column}`  
  Note: it will clear stdin
- ***func*** `getTerminalSize()`: get current terminal size. Size is returned in `{"columns":columns,"rows":lines}`
- ***func*** `print(string,newline=False,stdout=True,flush=True,moveCursor=True,crIfRaw=True)`: function to print `string`.  
  - ***kwarg*** If `newline` is not changed to `True`, `string` will be printed without newlines after it.  
  - ***kwarg*** If `stdout` is not changed to `False`, it will use `sys.stdout.write()` to output `string`
  - ***kwarg*** If `flush` is not changed to `False`, it will do `sys.stdout.flush()` after outputting `string` with `sys.stdout.write()`
  - ***kwarg*** If `moveCursor` is changed to `False`, it will move cursor back to it's original position after outputting `string`.
  - ***kwarg*** If `crIfRaw` is not changed to `True`, it will use `\n\r` as `newline` when in `raw` mode
- ***func*** `checkStdinForData()`: checks stdin for data. If there is data, it returns `True`, `False` otherwise
- ***func*** `getLastChar(block=False,includeNewline=True)`: gets the last character in stdin.
  - ***kwarg*** If block is not changed to `True`, it will return `None` if there is no data in stdin. If it is changed to `True`, it will wait for data.
  - ***kwarg*** If `includeNewline` is changed to `False`, it will return `None` when it finds a newline, useful when getting stdin data from `cooked` mode, which needs an extra `\n` to push data to stdin.
- ***func*** `echoKeys(enable=False,disable=False)`: change whether to echo key presses to stdout
  - ***kwarg*** If `enable` is changed to `True`, echoing keys will be enabled.
  - ***kwarg*** If `disable` is changed to `True`, echoing keys will be disabled.
  - ***kwarg*** If nothing is changed, it will return if echoing keys is enabled.
- ***func*** `clear(screen=False,scrollback=False,line=False,fromCursor=False,toEnd=False,toStart=False)`: clear certain parts of the screen.
  - ***kwarg*** If `fromCursor` is changed to `True`:
    - ***kwarg*** If `toEnd` is changed to `True`:
      - ***kwarg*** If `line` is changed to `True`, it will clear from the cursor to the end of the line
      - ***kwarg*** If `screen` is changed to `True`, it will clear from the cursor to the end of the screen.
    - ***kwarg*** If `toStart` is changed to `True`:
      - ***kwarg*** If `line` is changed to `True`, it will clear from the cursor to the end of the line
      - ***kwarg*** If `screen` is changed to `True`, it will clear from the cursor to the end of the screen.
  - Else:
    - ***kwarg*** If `screen` is changed to `True`, it will clear the screen
    - ***kwarg*** If `scrollback` is changed to `True`, it will clear the scrollback
    - ***kwarg*** If `line` is changed to `True`, it will clear the line that the cursor is currently on
- ***obj*** `CursorSaver()`: a object with cursor-saving and loading utils
  it uses `getPosition()`, causing it to clear stdin
  - ***func*** `self.save(id)`: save cursor with `id` as the id. `id` must be hashable
  - ***func*** `self.get(id)`: get the position with `id`. Returns with the same format as `getPosition()`
  - ***func*** `self.load(id)`: go to the position in `id`
- ***func*** `raw(enable=False,disable=False)`: set raw mode.
  - ***kwarg*** If `enable` is changed to `True`, it will enable raw mode
  - ***kwarg*** If `disable` is changed to `True`, it will disable raw mode
  - ***kwarg*** If nothing is changed, it will return whether raw mode is activated
- ***func*** `cursorVisibility(hide=False,show=False)`: set raw mode.
  - ***kwarg*** If `show` is changed to `True`, it will show the cursor
  - ***kwarg*** If `hide` is changed to `True`, it will hide the cursor
  - ***kwarg*** If nothing is changed, it will return whether cursor is visible
- ***func*** `bell()`: makes the terminal ring
- ***func*** `backspace()`: prints a backspace
- ***func*** `fillWithSpaces(saveCursor=True)`: fill the screen with spaces, pushing everything above into scrollback and allowing the cursor to move everywhere
  - ***kwarg*** if `saveCursor` is `False`, it will not get the cursor position and therefore not clear stdin
- ***func*** `fillRowWithSpaces()`: fill the current row with spaces
- ***func*** `changeStyle(background=False,foreground=False,color8=False,color256=False,reset=False,bold=False,dim=False,italic=False,underline=False,blink=False,invert=False,invisible=False,strikethrough=False)`: change the current text style/color
  - ***kwarg*** If `reset` is changed to True, all text printed after changing style will be reset  
  - ***kwarg*** If `bold` is changed to True, all text printed after changing style will be bold  
  - ***kwarg*** If `dim` is changed to True, all text printed after changing style will be dim  
  - ***kwarg*** If `italic` is changed to True, all text printed after changing style will be italic  
  - ***kwarg*** If `underline` is changed to True, all text printed after changing style will be underline  
  - ***kwarg*** If `blink` is changed to True, all text printed after changing style will be blink  
  - ***kwarg*** If `invert` is changed to True, all text printed after changing style will be inverted
  - ***kwarg*** If `invisible` is changed to True, all text printed after changing style will be invisible  
  - ***kwarg*** If `strikethrough` is changed to True, all text printed after changing style will be strikethrough'd
  - ***kwarg*** If `background` is changed to True:
    - ***kwarg*** If `color8` is not `False`, and is one of these: 
      - `black`
      - `red`
      - `green`
      - `yellow`
      - `blue`
      - `magenta`
      - `cyan`
      - `white`
      , it will make the background of all text printed after changing style `color8` colored
    - ***kwarg*** If `color256` is not `False` and is a `int` from `0` to `256`, it will make the background of all text printed after changing style `color256` colored
  - ***kwarg*** If `foreground` is changed to True:
    - ***kwarg*** If `color8` is not `False`, and is one of these: `blue` `black` `red` `green` `yellow` `magenta` `cyan` `white`
      , it will make the foreground of all text printed after changing style `color8` colored
    - ***kwarg*** If `color256` is not `False` and is a `int` from `0` to `256`, it will make the foreground of all text printed after changing style `color256` colored
- ***func*** `moveCursor(to=False,column=False,up=False,down=False,left=False,right=False,home=False)`: move the cursor
  - ***kwarg*** If `to` is not `False`, it will move the cursor to column `to["column"]` and row `to["row"]`
  - ***kwarg*** If `column` is not `False`, it will move the cursor to column `column`
  - ***kwarg*** If `up` is not `False`, it will move the cursor up `up` spaces
  - ***kwarg*** If `down` is not `False`, it will move the cursor down `down` spaces
  - ***kwarg*** If `left` is not `False`, it will move the cursor left `left` spaces
  - ***kwarg*** If `right` is not `False`, it will move the cursor right `right` spaces
- ***obj*** `KeyLogger()`: logs keys  
  it adds logged keys to `self.keys` list in the format of {`time.time()`output:key}  
  it is accurate to about 1/100th of a second
  - ***func*** `self.keyHandler()`: logs keys
  - ***func*** `self.start()`: starts `keyHandler()` in another thread
  - ***func*** `self.halt(wait=True)` stops the keyHandler in the other thread (if it is running, or it errors)
    - ***kwarg*** If `wait` is `True`, it will wait untill the other thread is stopped before continuing
  - ***bool*** `self.stop`: cause the keyHandler to end if it is set to `True`
- ***obj*** `KeyHandler(functions)`: calls a function when a key is pressed  
  functions are passed in the following format:  
  `{key1:[func1,(arg1,arg2)],key2:[func2,(arg1,arg2)],...,"default":defaultFunc}`
  the `default` func is not needed but is called when there isnt a mapping for the key already in the dictionary  
  the key is passed to the `default` function
  - ***func*** `self.keyHandler()`: handles keys
  - ***func*** `self.start()`: starts `keyHandler()` in another thread
  - ***func*** `self.halt(wait=True)` stops the keyHandler in the other thread (if it is running, or it errors)
    - ***kwarg*** If `wait` is `True`, it will wait untill the other thread is stopped before continuing
  - ***bool*** `self.stop`: cause the keyHandler to end if it is set to `True`
  - ***dict*** `self.actions`: the key-to-function mappings, from the time of initiation. You can change this directly.
- ***obj*** `FramerateLimiter(fps)`: limits framerate accurately
  ***arg*** `fps` is the fps to limit at  
  ***func*** `startFrame()`: start a frame  
  ***func*** `endFrame()`: end a frame, making a frame  
  ***func*** `delayTillNextFrame()`: delays till the end of the previous frame  
- ***obj*** `FramerateTracker()`: tracks framerate accurately  
  ***func*** `startFrame()`: start a frame  
  ***func*** `endFrame()`: end a frame, making a frame  
  ***func*** `calculateAverageFrameTime()`: get the average time taken to make a frame  
  ***func*** `calculateAverageFPS()`: calculate the average FPS  
  ***func*** `resetFrameMeasurements()`: reset the frame time measurements  
  ***func*** `calculateCurrentFPS()`: calculate the fps based on the previous frame  

## Installation:
### Macos/Linux:

1. [install ESCAPES](https://github.com/lomnom/ESCAPES/blob/main/README.md)
3. Run this:
```
echo "import os;print(os.__file__.replace('os.py',''))" - aahifbsab.py
PYPATH=$(python3 aahifbsab.py)
rm aahifbsab.py
curl https://raw.githubusercontent.com/lomnom/TERMINALFUNC/main/TERMINALFUNC.py - kashdfj.py
mv kashdfj.py "$PYPATH"TERMINALFUNC.py
```

## Uninstallation:
### macos/linux:
1. [uninstall ESCAPES](https://github.com/lomnom/ESCAPES/blob/main/README.md)
2. Run this:
```
echo "import os;print(os.__file__.replace('os.py',''))" - aahifbsab.py
PYPATH=$(python3 aahifbsab.py)
rm aahifbsab.py
rm "$PYPATH"TERMINALFUNC.py
```

---

Example: https://github.com/lomnom/PI

---
