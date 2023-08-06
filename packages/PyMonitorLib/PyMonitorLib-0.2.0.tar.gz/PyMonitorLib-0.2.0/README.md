# PyMonitorLib
Lightweight python library for collecting metrics and outputing to influx DB on an interval.

This library is designed for creating interval based monitoring applications quickly and easily. a Main function initializes the application and a Process function is called at the regular interval.

An example for all that is required:

```python
from monitor.lib import Execute, Result

def Main(config, logger, pipeline):
    return Result.SUCCESS

if __name__ == "__main__":
     Execute(Main, 'service')
```

The example will create an ArgumentParser for the necessary argument collect and spin up a process.

## Notes
This library currently only supports linux/posix based systems for use in process daemonization. Windows services are not currently supported. Basic functionality for building OS independent monitors should still function.
