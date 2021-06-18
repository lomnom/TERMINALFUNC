import ESCAPES as e
import sys
import select
import FUNC as f
import time as t

isRaw=False
cursorVisible=True
isEchoKeys=True
noSleepProcess=None

def stopSleep():
	from os import getpid
	f.runBash("caffeinate -w "+str(getpid()),background=True)

def getPosition():  #get current cursor position
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
	# from stdin? As dirty work around, getpos() recurses and calls itself to try again
	try:
		matches = re.match(r"^\x1b\[(\d*);(\d*)R", buf)
		groups = matches.groups()
	except AttributeError:
		return getPosition() #any keypresses will make it attributeerror, so try again. will error if 1000th time fails

	return {"row":int(groups[0]), "column":int(groups[1])}

def getTerminalSize(): #get size of current terminal
	from os import get_terminal_size
	columns,lines=get_terminal_size()
	return {"columns":columns,"rows":lines}

def print(string,newline=False,stdout=True,flush=True,moveCursor=True,crIfRaw=True): #advanced print
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

def checkStdinForData(): #check if stdin has data
	import select
	return select.select([sys.stdin,],[],[],0.0)[0]

def getLastChar(block=False,includeNewline=True): #get previous char pressed
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

def getLastChars(includeNewline=True,mustEndWithNewline=False): #VERY buggy unblocked getchars function, NOT documenting.
	chars=""

	while True:
		char=getLastChar(includeNewline=includeNewline)
		if char==None:
			if mustEndWithNewline:
				if chars.endswith("\n"): #there is a bug that incomplete input is received
					#, and it always doesnt end with a \n
					break
			else:
				break
		else:
			chars+=char

	return chars

def echoKeys(enable=False,disable=False): #change whether to let keypresses be displayed on the terminal
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
	#clear the terminal in different ways
	if fromCursor:
		if line:
			if toEnd:
				print(
					e.Escapes.Erase.FromCursor.toEndOfLine
				)
			if toStart:
				print(
					e.Escapes.Erase.FromCursor.toStartOfLine
				)
		if screen:
			if toEnd:
				print(
					e.Escapes.Erase.FromCursor.toEndOfScreen
				)
			if toStart:
				print(
					e.Escapes.Erase.FromCursor.toStartOfScreen
				)
		return

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

class CursorSaver: #class to save and load cursor positions
	def __init__(self):
		self.saves={}

	def save(self,name):
		self.saves[name]=getPosition()

	def get(self,name):
		return self.saves[name]

	def load(self,name):
		print(e.Escapes.Cursor.moveEscape(self.saves[name]["row"],self.saves[name]["column"]))

def raw(enable=False,disable=False): 
	#enable and disable raw (unbuffered) mode. useful for getting last char without newline
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

def cursorVisibility(hide=False,show=False): #change cursor visibility
	global cursorVisible
	if show:
		print(e.Escapes.Cursor.makeVisible)
		cursorVisible=True
	elif hide:
		print(e.Escapes.Cursor.makeInvisible)
		cursorVisible=False
	else:
		print(cursorVisible)

def bell(): #make terminal make bell sound
	print(e.Escapes.bell)

def backspace(): #backspace
	print(e.Escapes.backspace)

def fillWithSpaces(crIfRaw=True,saveCursor=True): #fill screen with spaces
	cursor=CursorSaver()
	if saveCursor:
		cursor.save(0)

	size=getTerminalSize()
	for line in f.fromTo(2,size["rows"]):
		print(" "*size["columns"],crIfRaw=crIfRaw,newline=True)

	if saveCursor:
		cursor.load(0)

def fillRowWithSpaces():
	size=getTerminalSize()
	print(" "*size["columns"],moveCursor=False)

def style(background=None,foreground=None,color8=None,color256=None,
	reset=None,bold=None,dim=None,italic=None,underline=None,blink=None,
	invert=None,invisible=None,strikethrough=None):
	
	escapes=""

	color8s={"colorCodes":
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
			,"backgroundStarter":"4"
			}

	if not color8==None:
		if not background==None:
			escapes+=e.buildEscape("esc",color8s["backgroundStarter"]+color8s["colorCodes"][color8]+"m")
		if not foreground==None:
			escapes+=e.buildEscape("esc",color8s["foregroundStarter"]+color8s["colorCodes"][color8]+"m")
	elif not color256==None:
		if not background==None:
			escapes+=e.Escapes.Color256.Background.color(color256)
		if not foreground==None:
			escapes+=e.Escapes.Color256.Foreground.color(color256)

	if reset:
		escapes+=e.Escapes.Style.reset
	if bold:
		escapes+=e.Escapes.Style.bold
	if dim:
		escapes+=e.Escapes.Style.dim
	if italic:
		escapes+=e.Escapes.Style.italic
	if underline:
		escapes+=e.Escapes.Style.underline
	if blink:
		escapes+=e.Escapes.Style.blink
	if invert:
		escapes+=e.Escapes.Style.invert
	if invisible:
		escapes+=e.Escapes.Style.invisible
	if strikethrough:
		escapes+=e.Escapes.Style.strikethrough

	return escapes

def changeStyle(background=None,foreground=None,color8=None,color256=None,
	reset=None,bold=None,dim=None,italic=None,underline=None,blink=None,
	invert=None,invisible=None,strikethrough=None):

	print(style(background=background,foreground=foreground,color8=color8,
		color256=color256,reset=reset,bold=bold,dim=dim,italic=italic,
		underline=underline,blink=blink,invert=invert,invisible=invisible,
		strikethrough=strikethrough))

def moveCursor(to=False,column=False,up=False,down=False,left=False,right=False,home=False): #move cursor
	if not to==False:
		print(e.Escapes.Cursor.moveEscape(to["row"],to["column"]))

	if not up==False:
		print(e.Escapes.Cursor.upEscape(up))

	if not down==False:
		print(e.Escapes.Cursor.downEscape(down))

	if not left==False:
		print(e.Escapes.Cursor.leftEscape(left))

	if not right==False:
		print(e.Escapes.Cursor.rightEscape(right))

	if not home==False:
		print(e.Escapes.Cursor.home)

	if not column==False:
		print(moveToColumn(column)) 

def saveScreen():
	print(e.Escapes.saveScreen)

def loadScreen():
	print(e.Escapes.load)

class KeyLogger:
	def __init__(self):
		self.keys=[]

	def start(self):
		self.proccess=f.runInParallel([[self.keyHandler,()]])

	def keyHandler(self):
		self.stop=False
		while not self.stop:
			t.sleep(0.01)
			char=getLastChar()
			if not char==None:
				self.keys+=[{t.time():char}]

	def halt(self,wait=True):
		self.stop=True
		if wait:
			self.proccess[0].join()

class KeyHandler:
	def __init__(self,actions): #actions are {key:[function,args],...}
		self.actions=actions
		self.actionProcecces=[]

	def start(self):
		self.proccess=f.runInParallel([[self.keyHandler,()]])

	def keyHandler(self):
		self.stop=False
		while not self.stop:
			t.sleep(0.01)
			char=getLastChar()
			if not char==None:
				try:
					f.runInParallel([self.actions[char]])
				except KeyError:
					try:
						f.runInParallel([[self.actions["default"],(char)]])
					except KeyError:
						pass

	def halt(self,wait=True):
		self.stop=True
		if wait:
			self.proccess[0].join()

def asciiBlock(topLeft=False,topRight=False,bottomLeft=False,bottomRight=False,
			   shade=None):
	if topLeft or topRight or bottomLeft or bottomRight:
		blocks={ #topLeft,topRight,bottomLeft,bottomRight
			"False,False,True,False":"▖",
			"False,False,False,True":"▗",
			"True,False,False,False":"▘",
			"False,True,False,False":"▝",
			"True,False,True,True":"▙",
			"True,False,False,True":"▚",
			"True,True,True,False":"▛",
			"True,True,False,True":"▜",
			"False,True,True,False":"▞",
			"False,True,True,True":"▟",
			"True,True,False,False":"▀",
			"False,False,True,True":"▄",
			"True,False,True,False":"▌",
			"False,True,False,True":"▐",
			"True,True,True,True":"█",
			"False,False,False,False":" "
		}
		return blocks[",".join([str(topLeft),str(topRight),str(bottomLeft),str(bottomRight)])]
	elif not shade==None:
		shades=[" ","░","▒","▓","█"]
		return shades[shade]

class FramerateLimiter:
	def __init__(self,fps):
		if fps==None:
			try:
				self.minimumFrameDelta=(1/fps)*1000000000
			except ZeroDivisionError:
				self.minimumFrameDelta=float("inf")
		else:
			self.minimumFrameDelta=0
		self.frameTimes=0
		self.frames=0
	def startFrame(self):
		self.frameStart=t.perf_counter_ns()
	def endFrame(self):
		self.frameTime=t.perf_counter_ns()-self.frameStart
		self.frameTimes+=self.frameTime
		self.frames+=1
	def delayTillNextFrame(self):
		if self.minimumFrameDelta-self.frameTime>0:
			t.sleep((self.minimumFrameDelta-self.frameTime)/1000000000)

class FramerateTracker:
	def __init__(self):
		self.frameTimes=0
		self.frames=0
		self.frameTime=0
	def startFrame(self):
		self.frameStart=t.perf_counter_ns()
		
	def endFrame(self):
		self.frameTime=t.perf_counter_ns()-self.frameStart
		self.frameTimes+=self.frameTime
		self.frames+=1

	def calculateAverageFrameTime(self):
		try:
			return ((self.frameTimes)/1000000000)/self.frames
		except ZeroDivisionError:
			return 0

	def calculateAverageFPS(self):
		try:
			return 1/self.calculateAverageFrameTime()
		except ZeroDivisionError:
			return 0

	def resetFrameMeasurements(self):
		self.frameTimes=0
		self.frames=0

	def calculateCurrentFPS(self):
		try:
			return 1/(self.frameTime/1000000000)
		except ZeroDivisionError:
			return 0
