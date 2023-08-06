# [copy_environment]

## Short Description
A package to copy environment requirements from one venv to another.

## Long Description
**copy_env** is a Python package allowing the user to copy requirements
from one venv to another. Users may interact with this package by importing
the copy_environment function or from the command line as a script.

## Examples
### Command Line
C:\example\path\lib\site-packages> python __init__.py --source C:\example\path\python.exe --destination C:\other\example\python.exe
C:\example\path\lib\site-packages> python __init__.py -s C:\example\path\python.exe -d C:\other\example\python.exe

### Importing
    from copy_environment import copy_environment

    source: str = C:\example\path
    destination: str = C:\other\example

    copy_environment(source, destination)
