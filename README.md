# TERMINALFUNC, a python library with every terminal manuplation function you will ever need!
## Attributes:
- `stopSleep()`: stop idle sleep while current process exists. Only works on OSX
- `getPosition()`: get current cursor position. Position is returned in `{"row":row, "column":column}`
- `getTerminalSize()`: get current terminal size. Size is returned in `{"columns":columns,"rows":lines}`
- `print(string,newline=False,stdout=True,flush=True,moveCursor=True,crIfRaw=True)`: function to print `string`.  
  > If `newline` is not changed to `True`, `string` will be printed without newlines after it.  
  > If `stdout` is not changed to `False`, it will use `sys.stdout.write()` to output `string`
  > If `flush` is not changed to `False`, it will do `sys.stdout.flush()` after outputting `string` with `sys.stdout.write()`
  > If `moveCursor` is changed to `False`, it will move cursor back to it's original position after outputting `string`.
  > If `crIfRaw` is not changed to `True`, it will use `\n\r` as `newline` when in `raw` mode
- `checkStdinForData()`: checks stdin for data. If there is data, it returns `True`, `False` otherwise
- `getLastChar(block=False,includeNewline=True)`: gets the last character in stdin.
  > If block is not changed to `True`, it will return `None` if there is no data in stdin. If it is changed to `True`, it will wait for data.
  > If `includeNewline` is changed to `False`, it will return `None` when it finds a newline, useful when getting stdin data from `cooked` mode, which needs an extra `\n` to push data to stdin.
- `echoKeys(enable=False,disable=False)`: change whether to echo key presses to stdout
  > If `enable` is changed to `True`, echoing keys will be enabled.
  > If `disable` is changed to `True`, echoing keys will be disabled.
  > If nothing is changed, it will return if echoing keys is enabled.
- `clear(screen=False,scrollback=False,line=False,fromCursor=False,toEnd=False,toStart=False)`: clear certain parts of the screen.
  > If `fromCursor` is changed to `True`:
    > If `toEnd` is changed to `True`:
      > If `line` is changed to `True`, it will clear from the cursor to the end of the line
      > If `screen` is changed to `True`, it will clear from the cursor to the end of the screen.
    > If `toStart` is changed to `True`:
      > If `line` is changed to `True`, it will clear from the cursor to the end of the line
      > If `screen` is changed to `True`, it will clear from the cursor to the end of the screen.
  > Else:
    > If `screen` is changed to `True`, it will clear the screen
    > If `scrollback` is changed to `True`, it will clear the scrollback
    > If `line` is changed to `True`, it will clear the line that the cursor is currently on
- `CursorSaver`: a class with cursor-saving and loading utils
  > Object needs to be initialised


---

**DISCLAIMERS**:
  - disclaimer

---
