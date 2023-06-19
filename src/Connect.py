import os
import logging
import eons
from pathlib import Path
from .Exceptions import *

#Interface method for use in other python code.
def connect(fitting, input={}, **kwargs):
	connector = Connector()
	return connector(fitting, input, **kwargs)

class Connector(eons.Executor):

	def __init__(this):
		super().__init__(name="Pipe Adapter", descriptionStr="An eons adapter for Pipedream")

		#Spoof args, since we won't be using this on the command line.
		this.args = eons.util.DotDict({
			'no_repo': False,
			'verbose': 1,
			'quiet': 0,
			'config': None
		})

		#Outputs are consolidated from Fitting.
		this.output = {}


	#Configure class defaults.
	#Override of eons.Executor method. See that class for details
	def Configure(this):
		super().Configure()
		this.defaultRepoDirectory = str(Path("/tmp/fittings").resolve())

	#Override eons.UserFunctor Call method to add arguments when called by other python functions.
	def __call__(this, fitting, input={}, **kwargs) :
		this.fittingName = fitting
		this.input = input
		super().__call__(**kwargs)
		return this.output #set in UserFunction()

	#Disable argument parsing, since this will not be called from the command line.
	def ParseArgs(this):
		pass

	#Override of eons.Executor method. See that class for details
	def Function(this):
		super().Function()
		fitting = this.GetRegistered(this.fittingName, "fitting")
		fitting(executor=this, input=this.input, **this.kwargs)
		this.output = fitting.output
