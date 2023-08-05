#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from cl1.classes.config import *
from cl1.classes.exceptions import *
import datetime 

# argument functions.
def argument_present(arguments):
	if isinstance(arguments, str):
		if arguments in sys.argv: return True
		else: return False
	elif isinstance(arguments, list):
		for argument in arguments:
			if argument in sys.argv: return True
		return False
	else: raise ValueError("Invalid usage, arguments must either be a list or string.")
def arguments_present(arguments):
	if isinstance(arguments, str): return argument_present(argument)
	else:
		for argument in arguments:
			if argument_present(argument):
				return True
		return False
def get_argument(argument, required=True, index=1, empty=None):

	# check presence.
	if argument not in sys.argv:
		if required:
			raise ValueError(f"Define parameter [{argument}].")
		else: return empty

	# retrieve.
	y = 0
	for x in sys.argv:
		try:
			if x == argument: return sys.argv[y+index]
		except IndexError:
			if required:
				raise ValueError(f"Define parameter [{argument}].")
			else: return empty
		y += 1

	# should not happen.
	return empty
def __str_representable__(dict):
	str = json.dumps(dict, indent=4, ensure_ascii=False)[:-2][2:].replace('    "', '    ').replace('": "', " : ")
	s, c, max = "", 0, len(str.split('\n'))
	for i in str.split('\n'):
		if i not in ["", " "]:
			if c < max-1:
				s += i[:-2]+"\n"
			else:
				s += i[:-1]+"\n"
		c += 1
	return s[:-1].replace(": : \n"," :\n").replace(" : \n",":\n")

# a default cli object
class CLI(object):
	def __init__(self, alias=None, modes={}, options={}, notes={}, executable=__file__, author="Daan van den Bergh"):

		# arguments.
		self.alias = alias
		self.modes = modes
		self.options = options
		self.notes = notes
		self.author = author
		self.executable = executable
		self.documentation = self.__create_docs__()
		self.arguments = self.Arguments(executable=self.executable, docs=self.docs, stop=self.stop)
		self.arguments.documentation = self.documentation

		#
	class Arguments(object):
		def __init__(self, executable=None, docs=None, stop=None,):
			self.docs = docs
			self.stop = stop
			self.executable = executable
		def present(self, argument):
			if isinstance(argument, str):
				return argument_present(argument)
			else:
				return arguments_present(argument)
		def get(self, argument, required=True, index=1, empty=None):
			if isinstance(argument, str):
				return get_argument(argument, required=required, index=index,empty=empty)
			else:
				arguments = []
				for i in argument: 
					arguments.append(get_argument(i, required=required, index=index,empty=empty))
				return arguments	
		def check(self, json=False):
			lexecutable = self.executable
			while True:
				if len(lexecutable) > 0 and lexecutable[len(lexecutable)-1] == "/": lexecutable = lexecutable[:-1]
				elif "//" in lexecutable: lexecutable = lexecutable.replace("//","/")
				else: break
			for i in sys.argv:
				if i not in ["", lexecutable] and not os.path.exists(i):
					if f" {i}: " not in self.modes_str and f" {i}: " not in self.options_str:
						error = f"Argument [{i}] is not a valid mode nor option."
						if json:
							response.log(error=error, json=True)
							sys.exit(1)
						else: 
							self.docs(stop=False)
							sys.tracebacklimit = -1
							sys.traceback_limit = -1
							raise UnkownArgumentError(error)
	def stop(self,
		# success exit.
		success=True,
		# optional order 1 success message (overwrites success to response.success).
		response=None,
		# optional order 2 success message (overwrites success to True).
		message=None,
		# optional order 3 message.
		error=None,
		# json format.
		json=False,
	):
		if response != None:
			if response["success"] in [True, "True", "true", "TRUE"]:
				success = True
				message = response["message"]
			else:
				success = False
				error = response["error"]
		if message != None: 
			success = True
			r3sponse.log(message=message, json=json)
		elif error != None: 
			success = False
			r3sponse.log(error=error, json=json)
		if success: sys.exit(0)
		else: sys.exit(1)
	def docs(self, 
		# the chapter (optional).
		chapter=None,
		# the mode (optional).
		mode=None,
		# success exit.
		success=True,
		# optional order 1 success message (overwrites success to response.success).
		response=None,
		# optional order 2 success message (overwrites success to True).
		message=None,
		# optional order 3 message.
		error=None,
		# json format.
		json=False,
		# stop after show.
		stop=True,
	):
		if not json:
			docs = self.documentation
			if chapter != None:
				s = self.documentation.split("\nModes:\n")
				before = s[0]+"\nModes:\n"
				s = s[1].split("\nAuthor:")
				after = "\nAuthor:"+s[1]
				new, include, indent, indent_str = "", False, 0, ""
				for line in s[0].split("\n"):
					if f" {chapter.lower()}: " in line.lower():
						indent = len(line.split(f"{mode}:")[0])
						indent_str = ""
						for _ in range(indent): indent_str += " "
						include = True
					elif include:
						s = ""
						for i in line:
							if i != " ": break
							s += i
						if s == indent_str and ":" in line:
							l = line[indent:].split(":")[0]
							if not(len(l) > 0 and len[0] == "-"):
								include = False
					if include: new += line+"\n"
				if mode != None and f" {mode}: " in new:
					s = new.split(f" {mode}: ")
					before = s[0]+f" {mode}: "
					_new_, include, indent = "", False, None
					for line in new.split("\n"):
						if f" {mode}: " in new:
							indent = len(line.split(f"{mode}:")[0])
							include = True
						elif indent != None and ":" in line:
							l = line[indent:].split(":")[0]
							if " " not in l and len(l) > 0 and l[0] == "-":
								include = False
						if include: _new_ += line+"\n"
					docs = before + _new_ + after
				else:
					docs = before + new + after
			elif mode != None:
				s = docs.split(f" {mode}: ")
				before = s[0]+f" {mode}: "
				_new_, include, indent = "", False, None
				for line in docs.split("\n"):
					if f" {mode}: " in docs:
						indent = len(line.split(f"{mode}:")[0])
						include = True
					elif indent != None and ":" in line:
						l = line[indent:].split(":")[0]
						if " " not in l and len(l) > 0 and l[0] == "-":
							include = False
					if include: _new_ += line+"\n"
				docs = before + _new_ + after
			print(docs)
		if stop:
			self.stop(
				success=success, 
				response=response, 
				message=message, 
				error=error, 
				json=json)
	def invalid(self, error="Selected an invalid mode.", chapter=None, mode=None, json=False):
		if not json:
			self.docs(
				chapter=chapter,
				mode=mode, 
				stop=False,)
		self.stop(error=error, json=json)
		#
	# system functions.
	def __create_docs__(self):
		self.modes_str  = self.arguments.modes_str = m = __str_representable__(self.modes)
		self.options_str = self.arguments.options_str = o = __str_representable__(self.options)
		n = __str_representable__(self.notes)
		c = f"\nAuthor: {self.author}. \nCopyright: © {self.author} {datetime.datetime.today().strftime('%Y')}. All rights reserved."
		doc = "Usage: "+self.alias+" <mode> <options> \nModes:\n"+m
		if o != "": doc += "\nOptions:\n"+o
		if n != "": doc += "\nNotes:\n"+n
		doc += c
		return doc


#