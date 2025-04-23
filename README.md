# Automated_DAC_Design

Python script for automated DAC design and implementation using open-source tools.

Go to `python` directory before running anything.
Set specifications directly in `main.py`. Alternatively, set specifications in `specs.py` and use function `load_specs()`. More information about the supported topologies and specifications in `help.txt`.


## Repository organization

Automated_DAC_Design
|-background		: theoretical background
|-klayout		: gds files
|  |-drc		: directory with drc output (markers)
|  |...
|-magic			: extracted spice
|  |-extract_dac.tcl	: script to extract circuit for lvs
|-netgen		: directory with lvs output
|-python		: working directory
|  |-design		: python modules for design choices
|  |  |...
|  |-layout		: python modules for gds generation
|  |  |...
|  |-sim		: generated spice files and simulation outputs
|  |-spice		: python modules for spice generation
|  |  |...
|  |-user.py		: python file with user paths
|  |-main.py		: main python file
|  |...
|-xschem		: directory with examples for xschem
   |...



## Authorship

Alfonso Cortés and Filip Maksimovic, AIO team, Inria.

Licensed under Apache License Version 2.0
