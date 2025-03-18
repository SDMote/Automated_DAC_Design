# ============================================================================
# Automated DAC design
# Alfonso Cortes - Inria AIO
# 
# ============================================================================


RESOLUTION = 8     # number of bits
# EQUAL_WIDTH = 0     # use equal widths for NMOS and PMOS, else consider a ratio between on-resistances
IDEAL_WIDTH = 1     # use ideal on-resistance ratio between NMOS and PMOS, else equall on-resistances
RES_NUMBER  = 2     # number of resistance instances that make the unit resistor R, changing the layout

MAX_NL = 0.5        # worst (max absolute) integral and differential nonlinearities (in LSB)
MAX_TIME = 2.5      # max transition time in us (rise or fall) from 10% to 90%
C_LOAD = 50         # load capacitance in picofarad


# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import pdk
import user
from utils import read_data, um
from design import set_ron_ratio, measure_resistance, layout_params
from rdac import rdac, rdac_tb, estimate_rdac_nl, r2r_ladder, rdac_tb_tran


Q = 2**RESOLUTION # number of codes
LSB = pdk.LOW_VOLTAGE/Q
target_R_th = MAX_TIME * 1e-6 / (2.2 * C_LOAD * 1e-12)     # 10%-90%, rise_time = 2.2*tau = 2.2*R_th*C_load
print("Resolution: ", RESOLUTION, "\tNº of series resistors: ", RES_NUMBER)
print("TARGET: Max NL:", MAX_NL, "\tOutput resistance:", target_R_th)


# Estimate on-resistances ratio
print("\nResistance estimation:")
R = 1
Rp = R/10
if IDEAL_WIDTH: # on resistance ratio that minimizes both nonlinearities
    inl, dnl, _, _ = estimate_rdac_nl(RESOLUTION, R, 0.2*Rp, Rp)
    worst_inl_1 = max(abs(inl))
    worst_dnl_1 = max(abs(dnl))
    inl, dnl, _, _ = estimate_rdac_nl(RESOLUTION, R, Rp, Rp)
    worst_inl_2 = max(abs(inl))
    worst_dnl_2 = max(abs(dnl))
    worst_inl_a = (worst_inl_1 - worst_inl_2)/(-0.8)
    worst_inl_b = worst_inl_2 - worst_inl_a
    worst_dnl_a = (worst_dnl_1 - worst_dnl_2)/(-0.8)
    worst_dnl_b = worst_dnl_2 - worst_dnl_a
    ratio = (worst_dnl_b - worst_inl_b)/(worst_inl_a - worst_dnl_a) # ratio in the crossing of worst INL and DNL
    print(" Ideal ratio: ", ratio)
else:           # equal on-resistances
    ratio = 1


# Estimate target R for target R_th
inl, dnl, _ , _ = estimate_rdac_nl(RESOLUTION, R, ratio*Rp, Rp)
# print(" With R=", R, "Rn=", ratio*Rp, "and Rp=", Rp)
# print(" Estimate => INL: ", max(abs(inl)), " DNL: ", max(abs(dnl)))
worst_nl = max(max(abs(inl)), max(abs(dnl)))
R = R * worst_nl / MAX_NL       # first approximation
inl, dnl, _ , _ = estimate_rdac_nl(RESOLUTION, R, ratio*Rp, Rp)
worst_nl = max(max(abs(inl)), max(abs(dnl)))
R = R * worst_nl / MAX_NL       # second approximation
k = 1/(R // Rp)
inl, dnl, _ , R_th = estimate_rdac_nl(RESOLUTION, R, ratio*k*R, k*R)
target_R = R * target_R_th / R_th
target_Rp = k*target_R
target_Rn = ratio*k*target_R
inl, dnl, _ , R_th = estimate_rdac_nl(RESOLUTION, target_R, target_Rn, target_Rp)
print(" With R=", target_R, "Rn=", target_Rn, "and Rp=", target_Rp)
print(" Estimate => INL: ", max(abs(inl)), " DNL: ", max(abs(dnl)), " R_th=", R_th)


# Simulate required resistance lenght fot target R (iteratively)
print("\nResistor size simulation:")
RES_L = pdk.RES_MIN_L * RES_NUMBER  # default unit resistor lenght (total for all series devices)
R = measure_resistance(RES_L, RES_NUMBER)
# r_resistivity = R / RES_L
# print("R min: ", R, " resistivity: ", r_resistivity)
l_step = RES_L * target_R / R - RES_L
while abs(l_step) >= pdk.GRID:
    RES_L = RES_L + l_step
    R = measure_resistance(RES_L, RES_NUMBER)
    l_step = RES_L * target_R / R - RES_L
r2r_ladder(RES_L, RES_NUMBER)       # editing the ladder is enough to update unit resistor lenght
print(" With Lr=", um(RES_L), "R=", R)


# Estimate inverter equivalent width to determine NF
Wn = Wp = pdk.MOS_MIN_W
rdac(2, Wn, Wp, 1, RES_L, RES_NUMBER)
rdac_tb(2, debug=True)
subprocess.run("openvaf sim/adc_model.va -o sim/adc_model.osdi", shell=True, check=True) 
Wn, Wp, Rn, Rp = set_ron_ratio(Wn, Wp, ratio)
equivalent_width = (Wp + Wn) * Rp / target_Rp
if RES_NUMBER == 2:     # fixed width ladder layout 2
    max_inverter_width = 3.85 - 0.7        # write as function of PDK or constant
else:                   # variable width ladder layout 1
    max_inverter_width = RES_L + 1.0  # check constant from layout
fingers = int(equivalent_width // max_inverter_width + 1)
if fingers > 1:
    Wn = Wp = pdk.MOS_MIN_W*fingers
    Wn, Wp, Rn, Rp = set_ron_ratio(Wn, Wp, ratio, fingers)
print(" Estimated inverter width:", equivalent_width, " Number of fingers: ", fingers)


# Simulate required Wn, Wp for target Rn, Rp mantaining ratio (iteratively)
print("\nInverter size simulation:")
step = (Rp * Wp) / target_Rp - Wp
while Rn > target_Rn or Rp > target_Rp:
    if abs(step) < fingers*pdk.GRID:
        Wn = Wn + fingers*pdk.GRID
        Wp = Wp + 2*fingers*pdk.GRID
    else:
        Wn = Wn + ratio * step
        Wp = Wp + step 
    Wn, Wp, Rn, Rp = set_ron_ratio(Wn, Wp, ratio, fingers)
    equivalent_width = (Wp + Wn) * Rp / target_Rp
    if equivalent_width // (fingers-1) > max_inverter_width:
        fingers = fingers + 1
        # Wn, Wp, Rn, Rp = set_ron_ratio(Wn, Wp, ratio, fingers)
    step = (Rp * Wp) / target_Rp - Wp
        
inl, dnl, _, R_th = estimate_rdac_nl(RESOLUTION, R, Rn, Rp)
print(" With Wn=", um(Wn), " Wp=", um(Wp), " and NG=", fingers, ", then Rn=", Rn, "Rp=", Rp)
print(" Estimate => INL: ", max(abs(inl)), " DNL: ", max(abs(dnl)), " R_th", R_th)


# Simulate full circuit
print('\nTop-level simulation:')
rdac(RESOLUTION, Wn, Wp, fingers, RES_L, RES_NUMBER)
rdac_tb(RESOLUTION)
subprocess.run("openvaf sim/adc_model.va -o sim/adc_model.osdi", shell=True, check=True) 
subprocess.run("ngspice -b sim/rdac_tb.spice -o sim/rdac.log > sim/temp.txt", shell=True, check=True) #!ngspice -b rdac.spice
data_dc = read_data("sim/rdac_dc.txt")
digital_input = np.arange(Q)
transfer_function = np.flip(data_dc[1][0:Q])
tfunction_ref = digital_input * pdk.LOW_VOLTAGE / Q
inl = (transfer_function - tfunction_ref)/LSB
dnl = (transfer_function[1:] - transfer_function[:Q-1] - LSB)/LSB

rdac_tb_tran(RESOLUTION, C_LOAD)
subprocess.run("ngspice -b sim/rdac_tb_tran.spice -o sim/rdac.log > sim/temp.txt", shell=True, check=True) #!ngspice -b rdac.spice
data = read_data("sim/rdac_tran.txt")
rise_time = data[1][0]
R_th = rise_time / (2.2 * C_LOAD * 1e-12)
print(' Simulate => INL:', max(abs(inl)), ' DNL:', max(abs(dnl)), " Worst transition time:", rise_time)
print("resistance", R_th)


# ============================================================================

# Layout generation
print('\nGenerating layout:')
layout_params(RESOLUTION, Wn, Wp, fingers, RES_L, RES_NUMBER)   # set layout generator parameters to match simulated circuit
subprocess.run("klayout -zz -r ../klayout/python/rdac.py -j ../klayout/", shell=True, check=True) # call layout generation with klayout

# # Extract spice netlist from GDS
# subprocess.run("magic -rcfile "+user.MAGICRC_PATH+" -noconsole -nowrapper ../magic/extract_rdac.tcl", shell=True, check=True)

# # Perform LVS
# subprocess.run("netgen -batch lvs \"../magic/TOP.spice TOP\" \"sim/rdac.spice rdac\" "+user.NETGEN_SETUP+" ../netgen/comp.out", shell=True, check=True)