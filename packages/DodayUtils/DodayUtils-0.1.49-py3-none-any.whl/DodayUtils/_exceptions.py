import os
import sys
import logging
import traceback

# Advanced Info on Error
def error_description():
	"""
	This function gets the file path and error line number 
	when a system exception occurs
	"""
	_, _, exc_tb = sys.exc_info()
	fobj = traceback.extract_tb(exc_tb)[-1]
	fname = fobj.filename
	line_no = fobj.lineno
	return fname, line_no, ''.join(traceback.format_tb(exc_tb))

def construct_error_message(header, bounds, description, filename, line_number, tb):
	"""
	This function constructs the error debug message by breaking line
	"""
	file_message = 'Occured in file: {} \n'.format(filename)
	line_number_message = 'At line: {} \n'.format(line_number)
	error_message = tb+header + '\n' + description + '\n' + file_message + line_number_message + bounds + '\n'
	return error_message

# define Python user-defined exceptions
class DodayUtilError(Exception):
	"""
	Base class for other exceptions
	filename: The file where the exception happens
	line_number: Line number where the exception occurs
	"""
	def __init__(self, description, fn=None, lineno=None, tb=None):
		super().__init__()
		self.description = description
		self.json_response = {"indicator":False, "message":description}
		self.bounds = "************************************************\n"
		self.fname, self.line_number, self.tb = fn, lineno, tb
		
	def __str__(self):
		self.header = super().__str__()
		if self.fname == None or self.line_number == None or self.tb == None:
			self.fname, self.line_number, self.tb = error_description()
		error_message = construct_error_message(self.header,self.bounds,self.description,self.fname,self.line_number, self.tb)
		logging.error(error_message)
		return error_message

	@classmethod
	def buildfromexc(cls, desc, fname, lineno, tb):
		"""
		This is the class method to return
		an instance based on existing exception
		"""
		return cls(desc, fname, lineno, tb)
