Mysbox
======

It is a set of tools to iniate MySensor's sketches (nodes and gateways) which can be compiled out of box. You also can
compile, upload (you need to download Arduino IDE, it uses its tools to compile and upload) your sketches and connect to
your MySensor's network and get some status of it.

Dependencies
------------

You may see all the dependeciens inside **requirements.txt**

or can use:

    $ pip install -r requirements.txt

Install
-------

    $ sudo python setup.py install

Usage
-----

This tool has, currently, three commands (create, compile and upload). You can use `-h` option in all commands to see
their usage.

Creating sketches
~~~~~~~~~~~~~~~~~

You can create sketches using simple commands.

Creating a node sketch with default name (node)

    $ mysbox create node

Creating a node sketch with a different name, internal sketch name and version

    $ mysbox create node my_light -n "My Light" -v 1.1

Creating a gateway sketch with default name (gw_node)

    $ mysbox create gw

Compiling
~~~~~~~~~

You also can compile your sketches using this tool. After you've executed any command of mysbox, it should create an
settings file in your home folder (`~/.mysboxrc`). In that file, all settings are required.

You must install MySensors library in any folder that you put into `.mysboxrc`

Listing all available boards

    $ mysbox compile -l

Compiling a simple node to Arduino Uno

    $ mysbox compile -b uno node/node.ino

Uploading
~~~~~~~~~

You also can upload your sketches using this tool. After you've executed any command of mysbox, it should create an
settings file in your home folder (`~/.mysboxrc`). In that file, all settings are required. However for this command,
only `arduino_tools` is required.

Listing all available boards

    $ mysbox upload -l

Compiling a simple node to Arduino Uno

    $ mysbox compile -b uno node/build_mys/node.ino.hex /dev/ttyUSB0

Support
-------

It was only tested on Linux envrionment. However, it should work on Windows and OS X systems.
Operating System:
- Linux

It was only tested with Python 3.4, but it should work with any Python 3.x.
Python Version:
- 3.4

What's news
-----------

- Support to create node and modify some arguments
- Support to create serial
- Support to compile sketch using arduino ide tools
- Support to upload hex file using arduino ide tools(avrdude)
