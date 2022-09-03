import os
import logging
import eons as e
from .Exceptions import *

class Fitting(e.UserFunctor):
    def __init__(this, name=e.INVALID_NAME()):
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
    def DidUserFunctionSucceed(this):
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
    def UserFunction(this):
        this.PreRun()

        logging.debug(f"<---- Running {this.name} ---->")
        this.Run()
        logging.debug(f">---- Done running {this.name} ----<")

        this.PostRun()


    # Will try to get a value for the given varName from:
    #    first: this
    #    second: the input map provided
    #    third: the executor (args > config > environment)
    # RETURNS the value of the given variable or None.
    def Fetch(this,
        varName,
        default=None,
        enableThis=True,
        enableExecutor=True,
        enableArgs=True,
        enableExecutorConfig=True,
        enableEnvironment=True,
        enableInput=True):
            
        # Duplicate code from eons.UserFunctor in order to establish precedence.
        if (enableThis and hasattr(this, varName)):
            logging.debug("...got {varName} from self ({this.name}).")
            return getattr(this, varName)

        if (enableInput):
            for key, val in this.input.items():
                if (key == varName):
                    logging.debug(f"...got {varName} from input.")
                    return val

        return super().Fetch(varName, default, enableThis, enableExecutor, enableArgs, enableExecutorConfig, enableEnvironment)
