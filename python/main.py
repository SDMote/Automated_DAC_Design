# ============================================================================
# Automated DAC design
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

# DAC specifications 
RESOLUTION = 10     # number of bits
TOPOLOGY = 0        # DAC circuit type
MAX_NL = 0.50       # worst (max absolute) integral and differential nonlinearities (in LSB)
MAX_TIME = 5.0      # max transition time in us (rise or fall) from 10% to 90%
C_LOAD = 50         # load capacitance in picofarad

# R2R-ladder options
IDEAL_WIDTH = 1     # use ideal on-resistance ratio between NMOS and PMOS, else equall on-resistances


# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import pdk
from design.dac import load_specs, design_dac, simulate_dac
from layout.dac import layout_dac

# Set dictionary with user input specifications
POLY_W = 300 
RES_NUMBER = 2
options = {'ideal_width':IDEAL_WIDTH, 'res_number':RES_NUMBER}  # topology-dependent specifications for R2R-ladder DAC
input_specs = {'resolution':RESOLUTION, 'topology':TOPOLOGY, 'max_nl':MAX_NL, 'max_time':MAX_TIME, 'c_load':C_LOAD, 'poly_w':POLY_W, 'options':options}
# input_specs = load_specs()    # to use values from specs.py

# Design circuit
print('\nCircuit design:')
spice_params, layout_params = design_dac(**input_specs)


# Simulate full circuit
print('\nTop-level simulation:')
inl, dnl, rise_time = simulate_dac(RESOLUTION, TOPOLOGY, spice_params, C_LOAD)
Q = 2**RESOLUTION
lsb = pdk.LOW_VOLTAGE/Q
digital_input = np.arange(Q)


# # Layout generation
print('\nGenerating layout:')
layout_dac(RESOLUTION, TOPOLOGY, layout_params, drc=1)


# Plot nonlinearities
fig, axs = plt.subplots(2, 1, sharex=True)
axs[0].plot(digital_input, inl, label='estimated inl')
axs[0].set_ylabel("INL (LSB)")
axs[0].grid()
axs[1].plot(digital_input[1:], dnl, label='estimated dnl')
axs[1].set_ylabel("DNL (LSB)")
axs[1].set_xlabel("Input code")
axs[1].grid()
axs[0].set_title("Simulated nonlinearities")
plt.show()