#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from cl1.v1.classes.config import *
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
	return s[:-1].replace(" : \n",":\n")

# a default cli object
class CLI(object):
	def __init__(self, alias=None, modes={}, options={}, notes={}, executable=__file__, author="Daan van den Bergh"):

		# arguments.
		self.alias = alias
		self.modes = modes
		self.options = options
		self.author = author
		self.documentation = self.__create_docs__()

		#
	def argument_present(self, argument):
		return argument_present(argument)
	def arguments_present(self, arguments):
		return arguments_present(arguments)
	def get_argument(self, argument, required=True, index=1, empty=None):
		return get_argument(argument, required=required, index=index,empty=empty)
	def check_alias(self):
		alias = self.alias
		executable = self.executable
		if '__main__.py' in executable: executable = executable.replace("__main__.py", "")
		path = f"/usr/local/bin/{alias}"
		if not os.path.exists(path):
			file = f"""package={executable}\nargs=""\nfor var in "$@" ; do\n   	if [ "$args" == "" ] ; then\n   		args=$var\n   	else\n   		args=$args" "$var\n   	fi\ndone\npython3 $package $args\n"""
			os.system(f"sudo touch {path}")
			os.system(f"sudo chmod 755 {path}")
			if OS in ["osx"]:
				os.system(f"sudo chown {os.environ.get('USER')}:wheel {path}")
			elif OS in ["linux"]:
				os.system(f"sudo chown {os.environ.get('USER')}:root {path}")
			utils.__save_file__(f"{path}", file)
			os.system(f"sudo chmod 755 {path}")
			if '--silent' not in sys.argv:
				print(f'Successfully created alias: {alias}.')
				print(f"Check out the docs for more info $: {alias} -h")
	# system functions.
	def __create_docs__(self):
		m = __str_representable__(self.modes)
		o = __str_representable__(self.options)
		n = __str_representable__(self.notes)
		c = f"\nAuthor: {self.author}. \nCopyright: © {self.author} {datetime.datetime.today().strftime('%Y')}. All rights reserved."
		doc = "Usage: "+self.alias+" <mode> <options> \nModes:\n"+m
		if o != "": doc += "\nOptions:\n"+o
		if n != "": doc += "\nNotes:\n"+n
		doc += c
		return doc


#