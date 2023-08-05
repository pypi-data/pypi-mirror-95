# QuickParse
Simple command line argument parser for Python

## Example

`list_things.py`:
```python
from quickparse import QuickParse

def list_things(a_list, quickparse):
    print(', '.join(map(str, a_list[:quickparse.numeric])))

commands_config = {
    'ls': list_things,
    '': lambda: print("Command is missing, use 'ls'"),
}

mylist = list(range(1, 12))

QuickParse(commands_config).execute(mylist)
```

Run it:
```sh
$ python list_things.py ls -5
1, 2, 3, 4, 5
```

The way it works:
- `commands_config` tells QuickParse to look for `ls` as a command and call `list_things` on it - when no commands show help
- QuickParse parses arguments as normal while `ls` is privileged as a command
- QuickParse finds `-5` so it adds as `quickparse.numeric = 5` (`quickparse` being the `QuickParse` instance that otherwise would come as `quickparse = QuickParse(commands_config)`)
- QuickParse sees `list_things` being associated to `ls`, so `quickparse.execute(mylist)` calls it, passing on the arguments of `execute(..)` - one positional argument in this case
- since `list_things` expects a named argument `quickparse`, QuickParse makes sure it passes on the reference to its own instance of `quickparse`

## GNU Argument Syntax implementation with extensions
GNU Argument Syntax: https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html

### Extensions
#### Numeric '-' values
```bash
$ my_cmd -12
```
#### Numeric '+' values
```bash
$ my_cmd +12
```
#### Long '-' options - only with explicit config
```bash
$ my_cmd -list
```
By default it becomes `-l -i -s -t`, but adding `QuickParse(options_config = [ ('-list', ) ])` will stop unpacking.
#### Long '+' options by default
```bash
$ my_cmd +list
```
#### Equivalent options - using options_config
```bash
$ my_cmd -l
```
is equivalent to
```bash
$ my_cmd --list
```
if adding `QuickParse(options_config = [ ('-l', '--list') ])`
#### Command-subcommand hierarchy and function bindings - using commands_config
Defining a random sample from `git` looks like this:
```python
commands_config = {
    '': do_show_help,
    'commit': do_commit,
    'log': do_log,
    'stash': {
        '': do_stash,
        'list': do_stash_list,
    }
}

options_config = [
    ('-a', '--all'),
]

QuickParse(commands_config, options_config).execute()
```
Commands are called according to commands_config.  
That is `$ git log -3` calls `do_log`  
`do_log` may look like this:
```python
def do_log(quickparse):
    print(get_log_entries()[:quickparse.numeric])
```
If there is a named argument in `do_log`'s signature called `quickparse`, the instance coming from `QuickParse(commands_config, options_config)` is passed down holding all the results of parsing.  
Parsing happens by using the defaults and applying what `options_config` adds to it.

## Argument Formats
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Argument&nbsp;Format&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Example&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Remarks |
| --- | --- | --- |
| `-<number>` | `$ my_cmd -12` | (default) |
| `+<number>` | `$ my_cmd +12` | (default) |
| `-<single_letter>` | `$ my_cmd -x` | (default) |
| `+<single_letter>` | `$ my_cmd +x` | (default) |
| `-<single_letter><value>` | `$ my_cmd -nFoo` | unpacking is the default: -n -F -o<br>`options_config` needs a type entry saying it expects a value (other than bool) |
| `+<single_letter><value>` | `$ my_cmd +nFoo` | unpacking is the default: +n +F +o<br>`options_config` needs a type entry saying it expects a value (other than bool) |
| `-<single_letter>=<value>` | `$ my_cmd -n=Foo` | (default) |
| `+<single_letter>=<value>` | `$ my_cmd +n=Foo` | (default) |
| `-<single_letter> <value>` | `$ my_cmd -n Foo` | `options_config` needs a type entry saying it expects a value (other than bool) |
| `+<single_letter> <value>` | `$ my_cmd +n Foo` | `options_config` needs a type entry saying it expects a value (other than bool) |
| `-<letters>` | `$ my_cmd -abc` | unpacking is the default: -a -b -c<br>if in `options_config` it's taken as `-abc` |
| `+<letters>` | `$ my_cmd +abc` | unpacking is the default: +a +b +c<br>if in `options_config` it's taken as `+abc` |
| `-<letters>=<value>` | `$ my_cmd -name=Foo` | (default) |
| `+<letters>=<value>` | `$ my_cmd +name=Foo` | (default) |
| `--<letters>` | `$ my_cmd --list` | (default) |
| `--<letters>=<value>` | `$ my_cmd --message=Bar` | (default) |
| `--<letters> <value>` | `$ my_cmd --message Bar` | `options_config` needs a type entry saying it expects a value (other than bool) |
| `--` | `$ my_cmd -- --param-anyway` | parameters delimiter<br>(default) |

`<letters>` means [a-zA-Z] and '-'s not in the first place

### An argument like '-a*' gets unpacked if...
- '-a' is not defined to expect a value
- the '*' part has only letters, not '-' or '='

### How to change the interpretation of `-swing`
It can mean (default):  
`-s -w -i -n -g`  
or  
`-s wing` / `-s=wing`  
To acheve the latter make the parser aware that '-s' expects a `str` value:
```python
options_config = [
    ('-s', str),
]
```

### Make the parser aware that an option expects a value after a space
Add type explicitly in `options_config`.  
For just getting as it is add `str`.

### How to define option types
Use build-in types like `int` or `float`, or create a callable that raises exceptions.  
Using `bool` is a special case: parser will not expect a value but explicitly adds an error if one provided.

### How to add empty value to an option
`-option=`
Some commands support '-' as empty value: `curl -C - -O http://domanin.com/`  
In this case '-' couldn't be provided as a literal so the syntax with '=' is supported here.

## Error handling
If the parser parameters 'commands_config' or 'options_config' are not valid, ValueError is rased from the underlying AssertionError.  
If the arguments are not compliant with the config (e.g. no value provided for an option that requires one) then no exceptions are raised but an `errors` list is populated on the `QuickParse` object.

## How to define options
`options_test.py`:
```python
from quickparse import QuickParse

options_config = [
    ('-u', '--utc', '--universal'),
    ('-l', '--long'),
    ('-n', '--name', str),
]

parsed = QuickParse(options_config=options_config)

print(parsed.options)
```

Run it:
```
$ python options_test.py
{}

$ python options_test.py -u
{'-u': True, '--utc': True, '--universal': True}

$ python options_test.py -ul
{'-u': True, '--utc': True, '--universal': True, '-l': True, '--long': True}

$ python options_test.py -uln
{'-uln': True}

$ python options_test.py -ul -nthe_name
{'-u': True, '--utc': True, '--universal': True, '-l': True, '--long': True, '-n': 'the_name', '--name': 'the_name'}

$ python options_test.py -ul -n the_name
{'-u': True, '--utc': True, '--universal': True, '-l': True, '--long': True, '-n': 'the_name', '--name': 'the_name'}

$ python options_test.py -ul -n=the_name
{'-u': True, '--utc': True, '--universal': True, '-l': True, '--long': True, '-n': 'the_name', '--name': 'the_name'}

$ python options_test.py -ul --name the_name
{'-u': True, '--utc': True, '--universal': True, '-l': True, '--long': True, '--name': 'the_name', '-n': 'the_name'}

$ python options_test.py -ul --name=the_name
{'-u': True, '--utc': True, '--universal': True, '-l': True, '--long': True, '--name': 'the_name', '-n': 'the_name'}
```
`-uln` stopped the parser from unpacking because `-n` expected an input value

## Test your command line arguments
`quickparse_test_args.py` (committed in the repo):
```python
from pprint import pformat

from quickparse import QuickParse


def do_show_help():
    print("Executing 'do_show_help'...")

def do_commit():
    print("Executing 'do_commit'...")

def do_log(quickparse):
    print("Executing 'do_log'...")

def do_stash():
    print("Executing 'do_stash'...")

def do_stash_list():
    print("Executing 'do_stash_list'...")

commands_config = {
    '': do_show_help,
    'commit': do_commit,
    'log': do_log,
    'stash': {
        '': do_stash,
        'list': do_stash_list,
    }
}

options_config = [
    ('-m', '--message', str),
    ('-p', '--patch'),
]


parsed = QuickParse(commands_config, options_config)


print(f'Commands:\n{pformat(parsed.commands)}')
print(f'Parameters:\n{pformat(parsed.parameters)}')
print(f'Options:\n{pformat(parsed.options)}')
print(f'\'-\' numeric argument:\n{pformat(parsed.numeric)}')
print(f'\'+\' numeric argument:\n{pformat(parsed.plusnumeric)}')
print(f'Functions to call:\n{pformat(parsed.to_execute)}')

parsed.execute()
```

## Validation
Well, I still need to elaborate the docs on this but here is a quick example snippet.  
```python
quickparse.validate({
    'parameters': { 'mincount': 1, },
    'options': {
        'mandatory': '--branch',
        'optional': '--stage',
    },
    'numeric': { 'maxcount': 0 },
    'plusnumeric': { 'maxcount': 0 },
})
assert 'parameters.mincount' not in quickparse.errors, f'Add a target'
assert not quickparse.has_errors, '\n'.join(quickparse.error_messages)
```
