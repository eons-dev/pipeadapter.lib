import os
import logging
import eons as e
from dotdict import dotdict
from pathlib import Path
from .Exceptions import *

#Interface method for use in other python code.
def connect(fitting, input={}, **kwargs):
    connector = Connector()
    return connector(fitting, input, **kwargs)

class Connector(e.Executor):

    def __init__(this):
        super().__init__(name="Pipe Adapter", descriptionStr="An eons adapter for Pipedream")

        #Spoof args, since we won't be using this on the command line.
        this.args = dotdict({
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
    def UserFunction(this):
        super().UserFunction()
        fitting = this.GetRegistered(this.fittingName, "fitting")
        fitting(executor=this, input=this.input, **this.kwargs)
        this.output = fitting.output

    # Will try to get a value for the given varName from:
    #    first: this.
    #    second: extra arguments provided to *this.
    #    third: the config file, if provided.
    #    fourth: the environment (if enabled).
    # RETURNS the value of the given variable or default.
    def Fetch(this, varName, default=None, enableThis=True, enableArgs=True, enableConfig=True, enableEnvironment=True):
        logging.debug(f"Fetching {varName}...")

        if (enableThis and hasattr(this, varName)):
            logging.debug(f"...got {varName} from {this.name}.")
            return getattr(this, varName)

        if (enableArgs):
            for key, val in this.kwargs.items():
                if (key == varName):
                    logging.debug(f"...got {varName} from argument.")
                    return val

        if (enableConfig and this.config is not None):
            for key, val in this.config.items():
                if (key == varName):
                    logging.debug(f"...got {varName} from config.")
                    return val

        if (enableEnvironment):
            envVar = os.getenv(varName)
            if (envVar is not None):
                logging.debug(f"...got {varName} from environment")
                return envVar

        logging.debug(f"...could not find {varName}; using default ({default})")
        return default