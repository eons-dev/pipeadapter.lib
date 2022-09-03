# Pipedream Adapter for eons

This library allows you to call "fittings" from your [Pipdream](https://pipedream.com) (or compatible) workflow.

## Fittings

The modules used by Pipeadapter are functors based on the [eons library](https://github.com/eons-dev/lib_eons).

Among other features, Fittings support:
```python
#All necessary args that *this cannot function without.
this.requiredKWArgs = []

#For optional args, supply the arg name as well as a default value.
this.optionalKWArgs = {}
```
Each of these "KWArgs" will become a member in the Fitting. For example `this.requiredKWArgs.append("my_arg")` sets `this.my_arg` to the value of `this.Fetch("my_arg")`. This system allows users to provide inputs in multiple ways while allowing developers to code in a standard format.

Developers also have access to all the [eons.UserFunctor utilities](https://github.com/eons-dev/lib_eons#user-functor).

### Example Fitting

```python
import os
import logging
from datetime import datetime
from pipeadapter import Fitting

class timestamp_to_date(Fitting):
    def __init__(this, name="Timestamp to Date"):
        super().__init__(name)

        this.requiredKWArgs.append("timestamp")

        this.optionalKWArgs["output_format"] = '%m/%d/%Y'

    # Required Fitting method. See that class for details.
    def Run(this):
        dt = datetime.fromtimestamp(this.timestamp)
        this.output["date"] = dt.strftime(this.output_format)
```