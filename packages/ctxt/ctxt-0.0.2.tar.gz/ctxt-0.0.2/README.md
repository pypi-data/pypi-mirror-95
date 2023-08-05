# context

Python debugging with context helper

Don't want complicated debugger but the `print("here")` isn't enough to help you catch mistakes ? Then you should try this module !

## Installation

```
pip install ctxt
```

## Usage

This example was generated using the notebook in the `demo` folder.

```python
from context import here, ctxt
"""
here: minimalist debugging
ctxt: complete debugging

Want an intermediate debugging? Instantiate your own Context object :-)
"""

sep = "\n" + 70 * "=" + "\n"

here()
```

    [<ipython-input-1-79eead714f34>:11] in <module>



```python
x = here(5 + 10)
print("x =", x)

print(sep)

y = ctxt(5 + 10)
print("y =", y)

print(sep)

z = ctxt(5, 6, a=10)
print("z =", z)
```

    [<ipython-input-2-db88b4f95185>:1] in <module>
    x = 15
    
    ======================================================================
    
    [<ipython-input-2-db88b4f95185>:6] in <module>:
    > 15
    y = 15
    
    ======================================================================
    
    [<ipython-input-2-db88b4f95185>:11] in <module>:
    > 5
    > 6
    > a = 10
    z = ((5, 6), dict_items([('a', 10)]))



```python
# Handle call inside a function
def my_square(x):
    y = x ** 2
    here()
    return y

s = my_square(5)
print("s =", s)

print(sep)


# Can also wrap a function call
s = here(my_square(10))
print("s =", s)
```

    [<ipython-input-3-323904d716c7>:4] in my_square
    s = 25
    
    ======================================================================
    
    [<ipython-input-3-323904d716c7>:4] in my_square
    [<ipython-input-3-323904d716c7>:14] in <module>
    s = 100



```python
# Can also be a function wrapper
@here  # binds to here.wrap
def my_sqrt(x):
    return pow(x, 0.5)

r = my_sqrt(4)
print("r =", r)

print(sep)

# Handles nested call, adding indent per-level
@here
def my_sqrt_bis(x):
    y =  here(pow(x, 0.5))
    return y

r = my_sqrt_bis(16)
print("r =", r)

print(sep)

# Same but with more context
@ctxt
def my_sqrt_ter(x):
    y =  ctxt(pow(x, 0.5))
    return y

r = my_sqrt_ter(25)
print("r =", r)
```

    [CALL: my_sqrt, FROM: <ipython-input-4-10cc6d34de9d>:6 in <module>]
    r = 2.0
    
    ======================================================================
    
    [CALL: my_sqrt_bis, FROM: <ipython-input-4-10cc6d34de9d>:17 in [...]
      [<ipython-input-4-10cc6d34de9d>:14] in my_sqrt_bis
    r = 4.0
    
    ======================================================================
    
    [CALL: my_sqrt_ter, FROM: <ipython-input-4-10cc6d34de9d>:28 in [...]
    <- in:
    > 25
      [<ipython-input-4-10cc6d34de9d>:25] in my_sqrt_ter:
      > 5.0
    -> out:
    > 5.0
    r = 5.0



```python
# If you still want to use the print function to add more context,
# you can wrap the print function using our wrapper

import builtins

@here
def print(*args, **kwargs):
    return builtins.print(*args)

# or
# print = here(builtins.print)

print("hello")

print(sep)  # Yes it will also be affected ;-)

def some_function():
    print("in some_function")
    

some_function()
    
# Reset old print function

print = builtins.print
```

    [CALL: print, FROM: <ipython-input-8-b7886cfc88db>:13 in <module>]
    hello
    [CALL: print, FROM: <ipython-input-8-b7886cfc88db>:15 in <module>]
    
    ======================================================================
    
    [CALL: print, FROM: <ipython-input-8-b7886cfc88db>:18 in [...]
    in some_function


# TODO List:

- allows more arguments to Context class
- allows block context with `with here as h:`
