\pypack_metager\
================

A `BuildNN <https://www.buildnn.com>`_ Open Source project.

Installing
----------

.. code-block:: text

  $ pip install pymetager

or from source

.. code-block:: text

  $ git clone https://github.com/buildnn/pymetager
  $ cd pymetager
  $ pip install -e .

Quickstart
----------

.. code-block:: text

  $ pymetager --help
  Usage: pymetager [OPTIONS] COMMAND [ARGS]...
  
  Options:
    -q, --quiet       Flag for minimal output.
    --config_fp FILE  Custom path for setup.cfg.  [default: ./setup.cfg]
    --help            Show this message and exit.
  
  Commands:
    echo-meta-elm
    increment


let's use info print function

.. code-block:: text

  $ pymetager echo-meta-elm --help
  --- PYPACK-METAGER ---
  A BuildNN Open Source project.
  Reading/Writing from/to ./setup.cfg
  Usage: pymetager echo-meta-elm [OPTIONS] [NAME]
  
  Options:
    -s, --section TEXT
    --help              Show this message and exit


.. code-block:: text

  $ pymetager echo-meta-elm version
  --- PYPACK-METAGER ---
  A BuildNN Open Source project.
  Reading/Writing from/to ./setup.cfg
  0.0.1

Or, concisely

.. code-block:: text

  $ pymetager -q echo-meta-elm version
  0.0.1
