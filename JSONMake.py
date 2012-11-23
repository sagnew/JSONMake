'''
Python script to parse JSON makefiles. I'll add good doc strings later

@author: Sam Agnew
'''
import sys
import json
import subprocess

#A class containing various methods to help me deal with files effectively
#Should I take this class out because it only has one method? Does it just obfuscate my code?
class FileUtilities:
    
    def __init__(self):
        return
    
	#Opens a file, ignoring case for the file name.
	#Eventually I plan to allow the user to input a file name(perhaps even a path to the JSONMakefile in another directory?
    def openIgnoreCase(self, file_name):
		#store the results of ls in this variable
		process = subprocess.Popen('ls', stdout=subprocess.PIPE)
		files = process.stdout.read()
		for file in files.split():
			if file.lower() == file_name.lower():
				return open(file)
		#If the loop is exited, then this file is not in the directory.
		print "Error! no JSONMakefile in this directory!"
		sys.exit()

#A class that deals with makefile functionality. Could probably have chosen a better name?
class Builder:
	
	def __init__(self, json_object):
		self.__json_object = json_object
		return

	#Takes an input string that represents a variable(will usually have a preceding $ char to denote that it is a variable, but this should be dealt with before calling this method.) and replaces it with it's corresponding value
	def replaceVar(self, string):
		return self.__json_object['Variables'][string]

	#Attempts to build from a rule with the input string as a name of the rule
	def build(self, rule):

		#This makes the rest of my code easier to read
		thisRule = self.__json_object['Rules'][rule]

		if 'depends' in thisRule:
			self.build(thisRule['depends'])
		
		#This is the string with the commands in this JSON object
		commands = thisRule['commands']
		
		#Go through every command and run each one separately
		for command in commands:
			
			#Replace all variables in the commands string
			for word in command.split():
				if word[0] == '$':
					#send in the word without the preceding '$'
					word = replaceVar(word[1:])
			
			#Actually execute the commands		
			self.execute_command(command.split)
	
	#Executes the command given. The command argument should be in list form.
	def execute_command(self, command):
		try:
			return subprocess.check_call(command.split())
		except subprocess.CalledProcessError as e:
			print e.output
			return e.returncode


utilities = FileUtilities() #object to deal with files

try:
    with utilities.openIgnoreCase('JSONMakefile') as f:
        makeFile = json.load(f)
except EnvironmentError:
    print "JSON MakeFile not found!"
    sys.exit()
except ValueError:
	print "Invalid JSON object!"
	sys.exit()

builder = Builder(makeFile)

#Just to check if there is a rule to build for 'all' There is probably a better, and more pythonic, way to do this
try:
	makeFile['Rules']['all']
except KeyError:
	print "No rule for 'all'!"
	sys.exit()

#Crashes right now because I am not finished.
builder.build('all')
