# ============================================================================
# Automated DAC design
# Alfonso Cortes - Inria AIO
# 
# ============================================================================


RESOLUTION = 10     # number of bits
TOPOLOGY = 0        # DAC type
MAX_NL = 0.50       # worst (max absolute) integral and differential nonlinearities (in LSB)
MAX_TIME = 2.5      # max transition time in us (rise or fall) from 10% to 90%
C_LOAD = 50         # load capacitance in picofarad

# R2R-ladder options
# EQUAL_WIDTH = 0     # use equal widths for NMOS and PMOS, else consider a ratio between on-resistances
IDEAL_WIDTH = 1     # use ideal on-resistance ratio between NMOS and PMOS, else equall on-resistances
RES_NUMBER  = 2     # number of resistance instances that make the unit resistor R, changing the layout


# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import user
import pdk
from design.dac import design_dac, simulate_dac
from layout.dac import layout_dac


target_R_th = MAX_TIME * 1e-6 / (2.2 * C_LOAD * 1e-12)     # 10%-90%, rise_time = 2.2*tau = 2.2*R_th*C_load
POLY_W = 300    # Not the gate width/lenght but the width of the inverter input


# Set topology-dependant options
match TOPOLOGY:
    case 0:     # R2R-ladder RDAC
        print("R2R-ladder RDAC with", RESOLUTION, "bits of resolution and ", RES_NUMBER, "series resistors per unit")
        options = {'IDEAL_WIDTH':IDEAL_WIDTH, 'RES_NUMBER':RES_NUMBER}
    case 1:     # Binary-weighted RDAC
        print("Binary-weighted RDAC with", RESOLUTION, "bits of resolution")
        options = {}
    case 2:     # Series RDAC
        print("Series-resistor RDAC with", RESOLUTION, "bits of resolution")
    case 3:     # Capacitive DAC
        print("Capacitive DAC with", RESOLUTION, "bits of resolution")
    case _:
        print("Error")
print("Target max NL:", MAX_NL, "\tTarget max transition time:", MAX_TIME, "us, with load of", C_LOAD, "pF (Target output resistance:", target_R_th, ")")


# Design circuit
print('\nCircuit design:')
spice_params, layout_params = design_dac(RESOLUTION, TOPOLOGY, MAX_NL, target_R_th, options, POLY_W)


# Simulate full circuit
print('\nTop-level simulation:')
inl, dnl, rise_time = simulate_dac(RESOLUTION, TOPOLOGY, spice_params, C_LOAD)


# # Layout generation
# print('\nGenerating layout:')
# layout_dac(RESOLUTION, TOPOLOGY, layout_params)

