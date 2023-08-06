# OpenPS
Open source plugin system.

# Install

Windows
```
pip install OpenPS
```

Linux
```
pip3 install OpenPS
```

# Built-in events

IMPORTANT: These events will not called automatically. You need to define when need to call.

- OnProgramStart
- OnProgramExit
- OnProgramInit

# How to use

If you have a project and want to add a plugin system then you just need to follow these instructions.
First you need to make the project folder.

```
.
├── main_program.py
└── plugins
    └── hello.py
```

You need to add a `plugin.py` file.
```
.
├── main_program.py
├── plugin.py
└── plugins
    └── hello.py
```
Write the following code to the `plugin.py`


```py
# plugin.py
import OpenPS

event = OpenPS.Event("./plugins/")

call = lambda name: event.call(name)
register = lambda name: event.register(name)

event.init()
```

If you want to add your own events then add this line in the code **above the `event.init()` line**.

```py
# plugin.py
import OpenPS

event = OpenPS.Event("./plugins/")

call = lambda name: event.call(name)
register = lambda name: event.register(name)

event.create("OnProgramFoo") # Create event.

event.init()
```

```py
# main_program.py
import plugin

def main():
  plugin.call("OnProgramFoo")
  print("hello world!")

main()
```

```py
# /plugins/hello.py
import plugin

@plugin.register("OnProgramFoo")
def function():
  print("hello from the plugin!")
```

When you run the `main_program.py` the output should be looks like this
```
hello from the plugin!
hello world!
```

# Adding custom plugin load order

The default loading order is `None`. That means loads in alphabetical order.

If you want to add your own order then make a new function in the `plugin.py`.
The function required minimum 1 parameter. The return value must be a list otherwise will not working.
```py
# plugin.py
import OpenPS

def reverse(lst) -> list:
  lst.sort(reverse=True)
  return lst

event = OpenPS.Event("./plugins/", reverse)

call = lambda name: event.call(name)
register = lambda name: event.register(name)

event.init()
```
