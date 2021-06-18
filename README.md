# TERMINALFUNC, a python library with every terminal manuplation function you will ever need!
## Attributes:
- `stopSleep()`: stop idle sleep while current process exists. Only works on OSX
- `getPosition()`: get current cursor position. Position is returned in `{"row":row, "column":column}`  
  Note: it will clear stdin
- `getTerminalSize()`: get current terminal size. Size is returned in `{"columns":columns,"rows":lines}`
- `print(string,newline=False,stdout=True,flush=True,moveCursor=True,crIfRaw=True)`: function to print `string`.  
  - If `newline` is not changed to `True`, `string` will be printed without newlines after it.  
  - If `stdout` is not changed to `False`, it will use `sys.stdout.write()` to output `string`
  - If `flush` is not changed to `False`, it will do `sys.stdout.flush()` after outputting `string` with `sys.stdout.write()`
  - If `moveCursor` is changed to `False`, it will move cursor back to it's original position after outputting `string`.
  - If `crIfRaw` is not changed to `True`, it will use `\n\r` as `newline` when in `raw` mode
- `checkStdinForData()`: checks stdin for data. If there is data, it returns `True`, `False` otherwise
- `getLastChar(block=False,includeNewline=True)`: gets the last character in stdin.
  - If block is not changed to `True`, it will return `None` if there is no data in stdin. If it is changed to `True`, it will wait for data.
  - If `includeNewline` is changed to `False`, it will return `None` when it finds a newline, useful when getting stdin data from `cooked` mode, which needs an extra `\n` to push data to stdin.
- `echoKeys(enable=False,disable=False)`: change whether to echo key presses to stdout
  - If `enable` is changed to `True`, echoing keys will be enabled.
  - If `disable` is changed to `True`, echoing keys will be disabled.
  - If nothing is changed, it will return if echoing keys is enabled.
- `clear(screen=False,scrollback=False,line=False,fromCursor=False,toEnd=False,toStart=False)`: clear certain parts of the screen.
  - If `fromCursor` is changed to `True`:
    - If `toEnd` is changed to `True`:
      - If `line` is changed to `True`, it will clear from the cursor to the end of the line
      - If `screen` is changed to `True`, it will clear from the cursor to the end of the screen.
    - If `toStart` is changed to `True`:
      - If `line` is changed to `True`, it will clear from the cursor to the end of the line
      - If `screen` is changed to `True`, it will clear from the cursor to the end of the screen.
  - Else:
    - If `screen` is changed to `True`, it will clear the screen
    - If `scrollback` is changed to `True`, it will clear the scrollback
    - If `line` is changed to `True`, it will clear the line that the cursor is currently on
- `CursorSaver`: a class with cursor-saving and loading utils
  - initialising requires no args
  - `CursorSaver.save(id)`: save cursor with `id` as the id. `id` must be hashable
  - `CursorSaver.get(id)`: get the position with `id`. Returns with the same format as `getPosition()`
  - `CursorSaver.load(id)`: go to the position in `id`
- `raw(enable=False,disable=False)`: set raw mode.
  - If `enable` is changed to `True`, it will enable raw mode
  - If `disable` is changed to `True`, it will disable raw mode
  - If nothing is changed, it will return whether raw mode is activated
- `cursorVisibility(hide=False,show=False)`: set raw mode.
  - If `show` is changed to `True`, it will show the cursor
  - If `hide` is changed to `True`, it will hide the cursor
  - If nothing is changed, it will return whether cursor is visible
- `bell()`: makes the terminal ring
- `backspace()`: prints a backspace
- `fillWithSpaces(saveCursor=True)`: fill the screen with spaces, pushing everything above into scrollback and allowing the cursor to move everywhere
  - if `saveCursor` is `False`, it will not get the cursor position and therefore not clear stdin
- `fillRowWithSpaces()`: fill the current row with spaces
- `changeStyle(background=False,foreground=False,color8=False,color256=False,reset=False,bold=False,dim=False,italic=False,underline=False,blink=False,invert=False,invisible=False,strikethrough=False)`: change the current text style/color
  - If `reset` is changed to True, all text printed after changing style will be reset  
  - If `bold` is changed to True, all text printed after changing style will be bold  
  - If `dim` is changed to True, all text printed after changing style will be dim  
  - If `italic` is changed to True, all text printed after changing style will be italic  
  - If `underline` is changed to True, all text printed after changing style will be underline  
  - If `blink` is changed to True, all text printed after changing style will be blink  
  - If `invert` is changed to True, all text printed after changing style will be inverted
  - If `invisible` is changed to True, all text printed after changing style will be invisible  
  - If `strikethrough` is changed to True, all text printed after changing style will be strikethrough'd
  - If `background` is changed to True:
    - If `color8` is not `False`, and is one of these: 
      - `black`
      - `red`
      - `green`
      - `yellow`
      - `blue`
      - `magenta`
      - `cyan`
      - `white`
      , it will make the background of all text printed after changing style `color8` colored
    - If `color256` is not `False` and is a `int` from `0` to `256`, it will make the background of all text printed after changing style `color256` colored
  - If `foreground` is changed to True:
    - If `color8` is not `False`, and is one of these: `blue` `black` `red` `green` `yellow` `magenta` `cyan` `white`
      , it will make the foreground of all text printed after changing style `color8` colored
    - If `color256` is not `False` and is a `int` from `0` to `256`, it will make the foreground of all text printed after changing style `color256` colored
- `moveCursor(to=False,column=False,up=False,down=False,left=False,right=False,home=False)`: move the cursor
  - If `to` is not `False`, it will move the cursor to column `to["column"]` and row `to["row"]`
  - If `column` is not `False`, it will move the cursor to column `column`
  - If `up` is not `False`, it will move the cursor up `up` spaces
  - If `down` is not `False`, it will move the cursor down `down` spaces
  - If `left` is not `False`, it will move the cursor left `left` spaces
  - If `right` is not `False`, it will move the cursor right `right` spaces

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
