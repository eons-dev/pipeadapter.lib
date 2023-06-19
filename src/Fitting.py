import os
import logging
import eons
from .Exceptions import *

class Fitting(eons.Functor):
	def __init__(this, name=eons.INVALID_NAME()):
		super().__init__(name)

		this.enableRollback = False

		# Populate this with anything you want to return.
		this.output = {}


	# Run inputs through *this fitting!
	# i.e. do work.
	# Override this or die.
	def Run(this):
		pass


	# Override this to perform whatever success checks are necessary.
	def DidRunSucceed(this):
		return True


	# API compatibility shim
	def DidFunctionSucceed(this):
		return this.DidRunSucceed()


	# Hook for any pre-run configuration
	def PreRun(this):
		pass


	# Hook for any post-run configuration
	def PostRun(this):
		pass


	# Override of eons.UserFunctor method. See that class for details.
	def ParseInitialArgs(this):
		super().ParseInitialArgs()
		this.input = this.kwargs.pop('input')


	# Override of eons.Functor method. See that class for details
	def Function(this):
		this.PreRun()

		logging.debug(f"<---- Running {this.name} ---->")
		this.Run()
		logging.debug(f">---- Done running {this.name} ----<")

		this.PostRun()

	def fetch_location_input(this, varName, default, fetchFrom, attempted):
		if (varName in this.input.keys()):
			return this.input[varName], True
		return default, False