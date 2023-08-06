
***************************************
Raisin: To perform cluster work easily!
***************************************

.. Pour la syntaxe voir: https://deusyss.developpez.com/tutoriels/Python/SphinxDoc/

Project Philosophy
^^^^^^^^^^^^^^^^^^
| The main aim of project\ *raisin*\  is to \ **share physical resources**\  of your laptop with a community.
| In counterpart, you can \ **benefit from the community resources**\ .
| There are 2 sides in this project:

1. Resources usage
^^^^^^^^^^^^^^^^^^
| The \ *raisin*\  API wants to be as close as possible to the 'threading' and 'multiprocessing' python APIs.
| The advantage in using \ *raisin*\  rather than 'threading' or 'multiprocessing' is that the computing power is greatly increased (depending on the number of connected resources).
| Though \ *raisin*\  is based on 'multiprocessing' module - that splits tasks among the resources of a single computer - it also shares the load over the different machines in the network. Everything is automatically and intelligently orchestrated relying on code analysis and graph theory.

\ *raisin*\  wants to be \ **as simple as possible**\ . That’s why the code analysis and the resources management are automated. It also uses a bunch of classes and functions default parameters that are suitable for most usages.

| However, you can tune \ *raisin*\  behavior as you want since all these parameters are \ **fully customizable**\ .
| \ *raisin*\  is a multi-OS module 100% written in python in order to keep installation reliable and simple.
| Although \ *raisin*\  uses powerful modules such as 'sympy', 'numpy', 'giacpy', 'pycryptodomex', 'tkinter'... these modules are not required (they are sometimes not easy to install). This will just lead to less efficiency, but no failure!

In a future version, \ *raisin*\  will be able to perform automatic parallelization, a little like 'pydron'.

2. Resources sharing
^^^^^^^^^^^^^^^^^^^^

| To be able to use community resources, you must give in return!
| That’s why, when \ *raisin*\  is installed as a python package, you have to install the 'application' part.
| To do this, execute the ``python3 -m raisin install`` command.

| The \ **security**\  is a primordial aspect.
| You can join or create your own cluster (e.g. friends working on a same project, ...), one at a time. The different clusters are waterproof between them. The data are encrypted. Machines must identify one another within a given cluster.

Your comfort while you are offering resources is guaranteed. \ *raisin*\  is \ **not intrusive**\ , it uses your resources - RAM, CPU, fan noise and bandwidth - only if they are available. Naturally, you can control how you want to share your resources (timetable, rate, ...).

Resource sharing, including security, is graphically \ **configurable**\ . Simply run ``python3 -m raisin configure`` command.

Installation
------------

From PyPI using pip (stable):

.. code-block:: bash

    sudo pip3 install raisin && sudo python3 -m raisin install # Remove 'sudo' for a single user installation.
    sudo apt install graphviz, python3-tk && sudo pip3 install graphviz, matplotlib # Optional, allows better graphics.

Upgrade to development version from 'framagit' (unstable):

.. code-block:: bash

    sudo python3 -m raisin upgrade --unstable

Configuration:

.. code-block:: bash

    python3 -m raisin configure

Uninstallation
--------------

.. code-block:: bash

    sudo python3 -m raisin uninstall && sudo pip3 uninstall raisin

Main Functions
--------------

* `Cluster work <https://framagit.org/robinechuca/raisin/-/blob/master/raisin/raisin.py>`_, with automatic distribution recording, results and protocol resumption.

+----------------+---------------------------------------------------+---------+
| Package        | Basic Description                                 | Example |
+================+===================================================+=========+
| raisin.Map     | runs a function n times, one per each argument    | n°2     |
+----------------+---------------------------------------------------+---------+
| raisin.map     | same as python built-in 'map', but over a cluster | n°3     |
+----------------+---------------------------------------------------+---------+
| raisin.Process | executes the function in the background           | n°4     |
|                | (similar to & unix command)                       |         |
+----------------+---------------------------------------------------+---------+
| raisin.process | same as Process, but blocking                     | n°5     |
+----------------+---------------------------------------------------+---------+
| raisin.Scan    | executes a function of i parameters n0*n1*...*ni  | n°6     |
|                | times. 'nk' is the length of the k th iterable.   |         |
+----------------+---------------------------------------------------+         |
| raisin.scan    | same as 'Scan' but blocking                       |         |
+----------------+---------------------------------------------------+---------+

* `Serialization <https://framagit.org/robinechuca/raisin/-/blob/master/raisin/serialization/serialize.py>`_ / `Deserialization <https://framagit.org/robinechuca/raisin/-/blob/master/raisin/serialization/deserialize.py>`_, with intercompatibility, encryption, compression and RAM saving.

Unlike \ *pickle*\ , \ *raisin*\  is also able to serialize filepath, generators, io.buffer, classes, functions and modules.

+--------------------+-------------------------------+---------+
| Package            | Basic Description             | Example |
+====================+===============================+=========+
| raisin.dumps       | serialisation (to str)        | n°7     |
+--------------------+-------------------------------+         |
| raisin.loads       | deserialisation (from str)    |         |
+--------------------+-------------------------------+---------+
| raisin.dump        | serialisation (to file)       | n°8     |
+--------------------+-------------------------------+         |
| raisin.load        | deserialisation (from file)   |         |
+--------------------+-------------------------------+---------+
| raisin.serialize   | serialisation (to bytes)      | n°9     |
+--------------------+-------------------------------+         |
| raisin.deserialize | deserialisation (from bytes)  |         |
+--------------------+-------------------------------+---------+
| raisin.copy        | real copy using serialization |         |
+--------------------+-------------------------------+---------+

* `More tools <https://framagit.org/robinechuca/raisin/-/blob/master/raisin/tools.py>`_.

+--------------------------------+------------------------------------------+
| Package                        | Basic Description                        |
+================================+==========================================+
| raisin.tools.MergeGenerators   | asynchronous merge iterator              |
+--------------------------------+------------------------------------------+
| raisin.tools.id                | retrieves lots of contextual information |
+--------------------------------+------------------------------------------+
| raisin.tools.Lock              | locks with possibility of mondial reach  |
+--------------------------------+------------------------------------------+
| raisin.tools.Printer           | friendly display                         |
+--------------------------------+------------------------------------------+
| raisin.tools.timeout_decorator | adds a timeout on any function           |
+--------------------------------+------------------------------------------+
| raisin.tools.get_temperature   | gets CPU temperature                     |
+--------------------------------+------------------------------------------+

Basic examples
--------------

.. code:: python

    In [1]: import raisin
       ...:
       ...: def foo(x):
       ...:     """Function long at execution."""
       ...:     ...
       ...:     return x**2
       ...:
       ...: def substraction(x, y):
       ...:     return x - y
       ...:
       ...: def localfail(): # A function that fails on this machine.
       ...:     import giacpy # Considering giacpy is not installed on the machine.
       ...:     return "OK"

Examples for 'Map', 'map', 'Process', 'process' and 'Scan'
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code:: python

    In [2]: m = raisin.Map(foo, range(3)) # More options.
       ...: m.start() # Hand back, parallel execution.
       ...: list(m.get_all()) # Yields the results as they arrive.
    Out[2]: [{'res': 0}, {'res': 1}, {'res': 4}] # More statistics fields.

    In [3]: list(raisin.map(foo, range(5))) # Sames options as 'Map'.
    Out[3]: [0, 1, 4, 9, 16] # Waits for the results to be ready and returns all.

    In [4]: p = raisin.Process(foo, args=(5,)) # More options.
       ...: p.start() # Hand back, parallel execution.
       ...: p.get() # Wait and return result.
    Out[4]: 25

    In [5]: raisin.process(localfail) # Look for a machine where it does not fail.
    Out[5]: 'OK'

    In [6]: s = raisin.Scan(substraction, [0, 1, 2], [1, 2]) # More options.
       ...: s.start()
       ...: s.get()
    Out[6]: [[-1, -2], [0, -1], [1, 0]] # The array dimension is the number of parameters.

Examples for 'dumps/loads', 'dump/load' and 'serialize/deserialize'
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code:: python

    In [7]: d = raisin.dumps(123456789) # More options.
       ...: print(d)    # Printable ascii characters.
       ...: print(raisin.loads(d))
    Out[7]: 'f2Y@c30Mc3MLfz4OcPgRdzsUej0M..'
       ...: 123456789

    In [8]: with open("filename.rsn", "wb") as f:
       ...:     raisin.dump(123456789, f) # Like pickle.dump
       ...: with open("filename.rsn", "rb") as f:
       ...:     print(raisin.load(f))
    Out[8]: 123456789

    In [9]: def gen(obj):
       ...:     for pack in raisin.serialize(obj): # Saves memory for large objects like files.
       ...:         print(pack)
       ...:         yield pack
       ...: print(raisin.deserialize(gen(123456789))) # Compatible with 'dumps' and 'dump'.
    Out[9]: b'</>small int</>123456789'
       ...: 123456789

* See the `integrated documentation <https://framagit.org/robinechuca/raisin/-/blob/master/raisin/__init__.py>`_ for more details and examples.
