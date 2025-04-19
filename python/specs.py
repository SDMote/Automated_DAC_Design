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
# EQUAL_WIDTH = 0     # use equal widths for NMOS and PMOS, else consider a ratio between on-resistances
IDEAL_WIDTH = 0     # use ideal on-resistance ratio between NMOS and PMOS, else equall on-resistances
RES_NUMBER  = 2     # number of resistance instances that make the unit resistor R, changing the layout
