![image logo][logo]

dott is a simple scheduling package written in Python 3.7.

## Install

With pip;
```bash
> pip install dott
```

With git;
```bash
> pip install git+https://github.com/alexmacniven/dott.git#egg=dott
```

## Usage

Use dott in your code to schedule invoking a function at a given time(s) or
periodically.

dott has just two functions; `hourly` and `daily`.

Here's some examples:

```python
import dott


def say_hello():
    """Displays 'hello world'."""
    print("hello world")

# Invoke `say_hello` every 2 hours.
dott.hourly(say_hello, 2)

# Invoke 'say_hello` daily at 14:00 and 21:00.
dott.daily(say_hello, ["14:00", "21:00"])
```

[logo]: ./docs/assets/logo.png
