import ESCAPES as e
import sys
import select
import FUNC as f

isRaw=False
cursorVisible=True
isEchoKeys=True

def getPosition(): 
	#https://stackoverflow.com/questions/46651602/determine-the-terminal-cursor-position-with-an-ansi-sequence-in-python-3
	import os, re, sys, termios, tty

	buf = ""
	stdin = sys.stdin.fileno()
	tattr = termios.tcgetattr(stdin)

	try:
		tty.setcbreak(stdin, termios.TCSANOW)
		sys.stdout.write("\x1b[6n")
		sys.stdout.flush()

		while True:
			buf += sys.stdin.read(1)
			if buf[-1] == "R":
				break

	finally:
		termios.tcsetattr(stdin, termios.TCSANOW, tattr)

	# reading the actual values, but what if a keystroke appears while reading
	# from stdin? As dirty work around, getpos() returns if this fails: None
	try:
		matches = re.match(r"^\x1b\[(\d*);(\d*)R", buf)
		groups = matches.groups()
	except AttributeError:
		return None

	return {"row":int(groups[0]), "column":int(groups[1])}

def getTerminalSize():
	from os import get_terminal_size
	columns,lines=get_terminal_size()
	return {"columns":columns,"rows":lines}

def print(string,newline=False,stdout=True,flush=True,moveCursor=True,crIfRaw=True):
	#crIfRaw is to add carraige return if in raw mode
	global isRaw

	if not moveCursor:
		saver=CursorSaver()
		saver.save(0)

	if stdout:
		sys.stdout.write(string)
		if newline:
			if not isRaw:
				sys.stdout.write("\n")
			elif crIfRaw:
				sys.stdout.write("\r\n")
	else:
		e.newlinelessPrint(string)
		if newline:
			if not isRaw:
				e.newlinelessPrint("\n")
			elif crIfRaw:
				e.newlinelessPrint("\r\n")
	if flush:
		sys.stdout.flush()

	if not moveCursor:
		saver.load(0)

def checkStdinForData():
	import select
	return select.select([sys.stdin,],[],[],0.0)[0]

def getLastChar(block=False,includeNewline=True):
	sys.stdin.flush()
	if block: #blocked, so dint care if got data
		data=sys.stdin.read(1)
		if (not data=="\n") or (includeNewline): #check for 
			return data #return data if no newline

	elif select.select([sys.stdin,],[],[],0.0)[0]: #check if got data
		data=sys.stdin.read(1)
		if (not data=="\n") or (includeNewline): #dont care if is newline if newlines enabled
			return data

	return None #return nothing otherwise

def getLastChars(includeNewline=True,mustEndWithNewline=True):
	chars=""

	while True:
		char=getLastChar(includeNewline=includeNewline)
		if char==None:
			if chars.endswith("\n") and mustEndWithNewline: #there is a bug that incomplete input is received
				#, and it always doesnt end with a \n
				break
		else:
			chars+=char

	return chars

def echoKeys(enable=False,disable=False):
	global isEchoKeys
	if enable:
		f.runBash("stty echo")
		isEchoKeys=True
	elif disable:
		f.runBash("stty -echo")
		isEchoKeys=False
	else:
		return isEchoKeys

def clear(screen=False,scrollback=False,line=False,fromCursor=False,toEnd=False,toStart=False):
	if fromCursor:
		if line:
			if toEnd:
				print(
					e.Escapes.Erase.FromCursor.toEndOfLine
				)
			elif toStart:
				print(
					e.Escapes.Erase.FromCursor.toStartOfLine
				)
		if screen:
			if toEnd:
				print(
					e.Escapes.Erase.FromCursor.toEndOfScreen
				)
			elif toStart:
				print(
					e.Escapes.Erase.FromCursor.toStartOfScreen
				)

	if screen:
		print(
			e.Escapes.Cursor.home+
			e.Escapes.Erase.FromCursor.toEndOfScreen
		)
	if scrollback:
		print(
			e.Escapes.Erase.scrollback
		)
	if line:
		print(
			e.Escapes.Erase.entireLine
		) 

class CursorSaver:
	def __init__(self):
		self.saves={}

	def save(self,name):
		self.saves[name]=getPosition()

	def get(self,name):
		return self.saves[name]

	def load(self,name):
		print(e.Escapes.Cursor.moveEscape(self.saves[name]["row"],self.saves[name]["column"]))

def raw(enable=False,disable=False):
	global isRaw

	if enable:
		f.runBash("""
			stty raw
			""")
		isRaw=True
	elif disable:
		f.runBash("""
			stty -raw
			""")
		isRaw=False
	else:
		return isRaw

def cursorVisibility(hide=False,show=False):
	global cursorVisible
	if show:
		print(e.Escapes.Cursor.makeVisible)
		cursorVisible=True
	elif hide:
		print(e.Escapes.Cursor.makeInvisible)
		cursorVisible=False
	else:
		print(cursorVisible)

def bell():
	print(e.Escapes.bell)

def backspace():
	print(e.Escapes.backspace)

def fillWithSpaces(crIfRaw=True):
	size=getTerminalSize()
	for line in f.fromTo(1,size["rows"]):
		print(" "*size["columns"],crIfRaw=crIfRaw,newline=True)

def changeStyle(background=False,foreground=False,color8=False,color256=False,trueColor=False):
	color8={"colorCodes":
				{"black":"0",
				"red":"1",
				"green":"2",
				"yellow":"3",
				"blue":"4",
				"magenta":"5",
				"cyan":"6",
				"white":"7"
				}
			,"foregroundStarter":"3"
			,"backgroundStarter":"4"}
	if not color8==False:
		if not background==False:
			print()

