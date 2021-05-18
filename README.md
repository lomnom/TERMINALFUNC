# TERMINALFUNC, a python library with every terminal manuplation function you will ever need!
## Attributes:
- `stopSleep()`: function to stop idle sleep while current process exists. Only works on OSX
- `getPosition()`: function to get current cursor position. Position is returned in `{"row":row, "column":column}`
- `getTerminalSize()`: function to get current terminal size. Size is returned in `{"columns":columns,"rows":lines}`
- `print(string,newline=False,stdout=True,flush=True,moveCursor=True,crIfRaw=True)`: function to print `string`.  
  > If `newline` is not changed to `True`, `string` will be printed without newlines after it.  
  > If `stdout` is not changed to `False`, it will use `sys.stdout.write()` to output `string`
  > If `flush` is not changed to `False`, it will do `sys.stdout.flush()` after outputting `string` with `sys.stdout.write()`
  > If `moveCursor` is changed to `False`, it will move cursor back to it's original position after outputting `string`.
  > If `crIfRaw` is not changed to `True`, it will use `\n\r` as `newline` when in `raw` mode


---

**DISCLAIMERS**:
  - disclaimer

---
