Argtools
==========

Description
-------------------
A collection of decorators wrapping argparse module for building command-line tools with *minimal effort*.

Quick start
-------------------

### Installation
```sh
$ pip install argtools
```

### Building a simple command-line tool

```python
# examples/test.py
from argtools import command, argument

@command
@argument('foo', help='a positional arugment')
@argument('--bar', default=3, help='an optional argument')
def main(args):
    """ One line description here

    Write details here (printed with --help|-h)
    """
    print args.bar
    print args.foo
    return 1  # return code


if __name__ == '__main__':
    command.run()
```

```sh
$ python test.py
$ python test.py -v   # Increasing the verbosity of logging module
```

The `argument` decorator has the same api as argparse.ArgumentParser.add_argument.
See http://docs.python.org/dev/library/argparse.html for details.


### Building subcommands

```python
# examples/subtest.py
from argtools import command, argument

@command.add_sub
def foo(args):
    """ This is foo
    """
    print 'foo'


@command.add_sub
def bar(args):
    """ This is bar
    """
    print 'bar'


@command.add_sub(name=baz)  # set different name
def bar(args):
    """ This is baz
    """
    print 'baz'

if __name__ == '__main__':
    command.run()
```

```sh
$ python test.py foo      # print foo
$ python test.py bar      # print bar
$ python test.py bar -h   # print help text of bar subcommand
```


Other features
-------------------

- In `command.run()`, the logging module is setup. You can control the verbosity with options: -v, -vv, ..
- In `command.run()`, SIGPIPE occured inside of wrapped function will be ignored to ease piping.
- To use `group` or `exclusive` functionality of argparse, give `argument` objects (e.g. arg1, arg2, arg3) as `@argument.group(arg1, arg2, arg3)` or `@argument.exclusive(arg1, arg2, arg3)`, respectively (documentation is #TODO).
- Builtin options: -v, --verbose and --debug can be turned off by setting `command.add_verbose = False` or `command.add_debug = False`
