# ============================================================================
# Automated DAC design
# Alfonso Cortes - Inria AIO
# 
# ============================================================================


TYPE = 0
RESOLUTION = 10     # number of bits
# EQUAL_WIDTH = 0     # use equal widths for NMOS and PMOS, else consider a ratio between on-resistances
IDEAL_WIDTH = 1     # use ideal on-resistance ratio between NMOS and PMOS, else equall on-resistances
RES_NUMBER  = 2     # number of resistance instances that make the unit resistor R, changing the layout

MAX_NL = 0.50       # worst (max absolute) integral and differential nonlinearities (in LSB)
MAX_TIME = 2.5      # max transition time in us (rise or fall) from 10% to 90%
C_LOAD = 50         # load capacitance in picofarad


# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import user
from pdk import *
from utils import read_data, um, dbu, dbu2um
from design import measure_resistance, layout_params
from dac_spice import dac_tb, dac_tb_tran
from rdac_spice import rdac, estimate_r2rdac_nl, r2r_ladder
from rdac_design import set_ron_ratio

MIN_STEP = GRID/DBU
Q = 2**RESOLUTION # number of codes
LSB = LOW_VOLTAGE/Q
target_R_th = MAX_TIME * 1e-6 / (2.2 * C_LOAD * 1e-12)     # 10%-90%, rise_time = 2.2*tau = 2.2*R_th*C_load
print("Resolution: ", RESOLUTION, "\t\tNº of series resistors: ", RES_NUMBER, "\tTarget max NL:", MAX_NL)
print("Target max transition time:", MAX_TIME, "us, with load of", C_LOAD, "pF (Target output resistance:", target_R_th, ")")
POLY_W = 300 #dbu

# Estimate on-resistances ratio
print("\nResistance estimation:")
R = 1
Rp = R/10
if IDEAL_WIDTH: # on resistance ratio that minimizes both nonlinearities
    inl, dnl, _, _ = estimate_r2rdac_nl(RESOLUTION, R, 0.2*Rp, Rp)
    worst_inl_1 = max(abs(inl))
    worst_dnl_1 = max(abs(dnl))
    inl, dnl, _, _ = estimate_r2rdac_nl(RESOLUTION, R, Rp, Rp)
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
inl, dnl, _ , _ = estimate_r2rdac_nl(RESOLUTION, R, ratio*Rp, Rp)
# print(" With R=", R, "Rn=", ratio*Rp, "and Rp=", Rp)
# print(" Estimate => INL: ", max(abs(inl)), " DNL: ", max(abs(dnl)))
worst_nl = max(max(abs(inl)), max(abs(dnl)))
R = R * worst_nl / MAX_NL       # first approximation
inl, dnl, _ , _ = estimate_r2rdac_nl(RESOLUTION, R, ratio*Rp, Rp)
worst_nl = max(max(abs(inl)), max(abs(dnl)))
R = R * worst_nl / MAX_NL       # second approximation
k = 1/(R // Rp)
inl, dnl, _ , R_th = estimate_r2rdac_nl(RESOLUTION, R, ratio*k*R, k*R)
target_R = R * target_R_th / R_th
target_Rp = k*target_R
target_Rn = ratio*k*target_R
inl, dnl, _ , R_th = estimate_r2rdac_nl(RESOLUTION, target_R, target_Rn, target_Rp)
print(" With R=", target_R, "Rn=", target_Rn, "and Rp=", target_Rp)
print(" Estimate => INL: ", max(abs(inl)), " DNL: ", max(abs(dnl)), " R_th=", R_th)


# Simulate required resistance lenght fot target R (iteratively)
print("\nResistor size simulation:")
RES_L = RES_MIN_L * RES_NUMBER  # default unit resistor lenght (total for all series devices)
R = measure_resistance(RES_L, RES_NUMBER)
# r_resistivity = R / RES_L
# print("R min: ", R, " resistivity: ", r_resistivity)
step = dbu((RES_L * target_R / R - RES_L) / RES_NUMBER)
done = 0
while not done and step != 0:
    if abs(step) <= MIN_STEP:
        done = 1
    RES_L = RES_L + RES_NUMBER * step
    R = measure_resistance(RES_L, RES_NUMBER)
    step = dbu((RES_L * target_R / R - RES_L) / RES_NUMBER)
r2r_ladder(RES_L, RES_NUMBER)       # editing the ladder is enough to update unit resistor lenght
print(" With Lr=", um(RES_L), "R=", R)


# Simulate required Wn, Wp for target Rn, Rp mantaining ratio (iteratively)
print("\nInverter size simulation:")
Wn = Wp = MOS_MIN_W
rdac(2, Wn, Wp, 1, RES_L, 0, RES_NUMBER)
dac_tb(2, debug=True, type=TYPE)
subprocess.run("openvaf sim/adc_model.va -o sim/adc_model.osdi", shell=True, check=True) 
Rn, Rp, Wn, Wp = set_ron_ratio(Wn, Wp, ratio)   # first approximation
equivalent_inverter_width = 2 * max(Wp * Rp / target_Rp, Wn * Rn / target_Rn)
inverter_const_width = max(RHIa/2 + M1b, GATd+POLY_W/2, (NWc+NWd)/2, (300+PSDb+PSDc1)/2) + max(M1b, GATd + CNTd) + CNTd + CNTa + GATb/2
if RES_NUMBER == 2:     # fixed width ladder layout 2
    HALF_WIDTH = 3960/2   
else:                   # variable width ladder layout 1
    HALF_WIDTH = (RES_L + 1000)/2 # check constant from layout
max_inverter_width = 2*(HALF_WIDTH - inverter_const_width)  
fingers = int(equivalent_inverter_width // max_inverter_width + 1)   # Estimate inverter equivalent width to determine NF
if fingers > 1:
    Wn = Wp = MOS_MIN_W * fingers
    Rn, Rp, Wn, Wp = set_ron_ratio(Wn, Wp, ratio, fingers)
step = dbu(((Rn * Wn) / target_Rn - Wn) / fingers)
done = 0
while not done: #Rn > target_Rn or Rp > target_Rp:
    if step == MIN_STEP:
        Wn = Wn + fingers * MIN_STEP
        Wp = Wp + fingers * dbu(MIN_STEP / ratio)
    else:
        Wn = Wn + fingers * dbu(0.5 * step)
        Wp = Wp + fingers * dbu(0.5 * step / ratio)
    Rn, Rp, Wn, Wp = set_ron_ratio(Wn, Wp, ratio, fingers)
    equivalent_inverter_width = 2 * max(Wp * Rp / target_Rp, Wn * Rn / target_Rn)
    fingers_next = int(equivalent_inverter_width // max_inverter_width + 1)
    if fingers != fingers_next:
        fingers = fingers_next
        if Wn < MOS_MIN_W * fingers or Wp < MOS_MIN_W * fingers:
            Wn = Wp = MOS_MIN_W * fingers
        else:
            Wn = fingers * dbu(Wn / fingers)
            Wp = fingers * dbu(Wp / fingers)
        Rn, Rp, Wn, Wp = set_ron_ratio(Wn, Wp, ratio, fingers)
    step = dbu(((Rn * Wn) / target_Rn - Wn) / fingers)
    if step == 0 or step == -MIN_STEP:
        done = 1
        
inl, dnl, _, R_th = estimate_r2rdac_nl(RESOLUTION, R, Rn, Rp)
print(" With Wn=", um(Wn), " Wp=", um(Wp), " and NG=", fingers, ", then Rn=", Rn, "Rp=", Rp)
print(" Estimate => INL: ", max(abs(inl)), " DNL: ", max(abs(dnl)), " R_th", R_th)


# Simulate full circuit
print('\nTop-level simulation:')
rdac(RESOLUTION, Wn, Wp, fingers, RES_L, TYPE, RES_NUMBER)
dac_tb(RESOLUTION)
subprocess.run("openvaf sim/adc_model.va -o sim/adc_model.osdi", shell=True, check=True) 
subprocess.run("ngspice -b sim/dac_tb.spice -o sim/dac.log > sim/temp.txt", shell=True, check=True) #!ngspice -b rdac.spice
data_dc = read_data("sim/dac_dc.txt")
digital_input = np.arange(Q)
transfer_function = np.flip(data_dc[1][0:Q])
tfunction_ref = digital_input * LSB
inl = (transfer_function - tfunction_ref)/LSB
dnl = (transfer_function[1:] - transfer_function[:Q-1] - LSB)/LSB

dac_tb_tran(RESOLUTION, C_LOAD, TYPE)
subprocess.run("ngspice -b sim/dac_tb_tran.spice -o sim/dac.log > sim/temp.txt", shell=True, check=True) #!ngspice -b rdac.spice
data = read_data("sim/dac_tran.txt")
rise_time = data[1][0]
R_th = rise_time / (2.2 * C_LOAD * 1e-12)
print(' Simulate => INL:', max(abs(inl)), ' DNL:', max(abs(dnl)), " Worst transition time:", rise_time)


# ============================================================================

# Layout generation
print('\nGenerating layout:')
layout_params(RESOLUTION, Wn, Wp, fingers, RES_L, RES_NUMBER, HALF_WIDTH, POLY_W)   # set layout generator parameters to match simulated circuit
subprocess.run("klayout -zz -r ../klayout/python/rdac.py -j ../klayout/", shell=True, check=True) # call layout generation with klayout

print("\nVerification:")
# Run DRC
print(" Running DRC")
subprocess.run("klayout -zz -r "+user.KLAYOUT_DRC+" -rd in_gds=\"../klayout/rdac.gds\" -rd report_file=\"../klayout/drc/sg13g2_maximal.lyrdb\" >../klayout/drc/drc.log", shell=True, check=True)

# Extract spice netlist from GDS
subprocess.run("magic -rcfile "+user.MAGICRC_PATH+" -noconsole -nowrapper ../magic/extract_dac.tcl > sim/temp.txt", shell=True, check=True)

# Perform LVS
print(" Running LVS")
subprocess.run("netgen -batch lvs \"../magic/dac.spice dac\" \"sim/dac.spice dac\" "+user.NETGEN_SETUP+" ../netgen/comp.out > sim/temp.txt", shell=True, check=True)