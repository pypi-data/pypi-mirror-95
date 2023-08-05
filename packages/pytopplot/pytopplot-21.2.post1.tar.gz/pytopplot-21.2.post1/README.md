# Description

GUI for **A**zimuthal **B**eam **C**avity **I**nteraction (ABCI) program. ABCI binaries could be obtained from [http://abci.kek.jp/abci.htm](http://abci.kek.jp/abci.htm).

# Installation

## Get python and pip

Download and install python and pip.

You may use a package manager for this. For example, in Debian installation command looks like this:

`sudo apt-get install python3 python3-pip`

If you don't have a package manager, download installer from the [python web site](https://www.python.org/downloads/).

## Install *pytopplot*

From the terminal issue the command

`pip3 install pytopplot`

for system-wide installation, or

`pip3 install --user pytopplot`

for the local installation.

## Download *ABCI* binary [optional]

Package provides *ABCI* binaries, but they may be outdated.

Download the newest *ABCI* binaries form the [*ABCI* web site](http://abci.kek.jp/abci.htm).
When program starts, in *Settings* tab choose the location of the *ABCI* binary, you want to use.

# Run

In order to run the program, from the terminal issue the command

`pytopplot`

If it's not found, you have to modify the `PATH` environment variable to include the python scripts folder ([unix guide](https://stackoverflow.com/a/3402176/5745120),[windows guide](https://superuser.com/a/143121/736971)) or supply the full path to the program.

# Other

## Update *pytopplot*

To update program, from the terminal issue the command

`pip3 install --upgrade pytopplot`

for system-wide installation, or

`pip3 install --upgrade --user pytopplot`

for the local installation.

## Issue submission

In case of a problem with the program, create an issue in the [issue tracker](https://bitbucket.org/seregaxvm/pytopplot/issues?status=new&status=open).
