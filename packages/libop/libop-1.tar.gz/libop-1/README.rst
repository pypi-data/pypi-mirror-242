**L  I  B  O  P**


!!


**NAME**

|
| OP - original programmer
|

**DESCRIPTION**

|
| OP (original programmer) is a package that provides basic programming
| tools, such as disk perisistence for configuration files, event handler
| to handle the client/server connections, code to introspect modules for
| commands, deferred exception handling to not crash on an error, a parser
| to parse commandline options and values, etc.
|
| LIBOP is a contribution back to society and is Public Domain.
|

**SYNOPSIS**

::

    >>> from op import Object, read, write
    >>> o = op.Object()
    >>> o.a = "b"
    >>> write(o, "demo")
    >>> oo = op.Object()
    >>> read(oo, "demo")
    >>> oo
    {"a": "b"}


**INSTALL**

|
| pipx install libop
|


**AUTHOR**

|
| Bart Thate <libbotx@gmail.com>
|

**COPYRIGHT**

|
| LIBOP is a contribution back to society and is Public Domain.
