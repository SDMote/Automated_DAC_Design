# ============================================================================
# DAC design specifications
# 
# ============================================================================

RESOLUTION = 10     # number of bits
TOPOLOGY = 0        # DAC type
MAX_NL = 0.50       # worst (max absolute) integral and differential nonlinearities (in LSB)
MAX_TIME = 5.0      # max transition time in us (rise or fall) from 10% to 90%
C_LOAD = 50         # load capacitance in picofarad

# R2R-ladder options
IDEAL_WIDTH = 0     # use ideal on-resistance ratio between NMOS and PMOS, else equall on-resistances
