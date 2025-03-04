# ============================================================================
# Automated DAC design
# Alfonso Cortes - Inria AIO
# 
# ============================================================================


RESOLUTION = 10     # number of bits
MAX_INL = 1         # max absolute integral nonlinearity (in LSB)
MAX_DNL = 1         # max absolute differential nonlinearity (in LSB)

# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import pdk
import user
from utils import read_data
from rdac import rdac, rdac_tb, estimate_rdac_nl
from bit import inverter, inverter_tb, nmos_tb, pmos_tb, resistor_tb

NMOS_W = 0.2        # inverter nmos finger width
RES_L = 10.0        # rdac unit resistance lenght
PMOS_FACTOR = 2.5
PMOS_W = NMOS_W * PMOS_FACTOR
M = 2**RESOLUTION # number of codes
LSB = pdk.LOW_VOLTAGE/M


# Estimate minimum necessary ON resistances with expression
print('\nEstimating minimum on resistance')

resistor_tb(RES_L)
subprocess.run("ngspice -b sim/resistor_tb.spice -o sim/resistor.log > sim/temp.txt", shell=True, check=True)
data_op_res = read_data("sim/resistor_op.txt")
R = data_op_res[0][0]/data_op_res[1][0]

ready = False
mos_resistance = 16000
while not ready:
    inl, dnl = estimate_rdac_nl(RESOLUTION, R, mos_resistance, mos_resistance)
    if max(abs(inl))<1 and max(abs(dnl))<1:
        ready = True
    else:
        mos_resistance = mos_resistance / 2
print('Estimated\tINL=', max(abs(inl)), '\tDNL=', max(abs(dnl)))

# Estimate transistor width by simulating 2-bits DAC
print('\nEstimating required multiplicity')

ready = False
number_fingers = 1
digital_input = np.arange(4)
rdac(2, NMOS_W, PMOS_W, number_fingers, RES_L)
rdac_tb(2, debug=True)
subprocess.run("openvaf sim/adc_model.va -o sim/adc_model.osdi", shell=True, check=True) 

while not ready:
    subprocess.run("ngspice -b sim/rdac_tb.spice -o sim/rdac.log > sim/temp.txt", shell=True, check=True)
    data_ids = read_data("sim/rdac_ids.txt")
    data_vds = read_data("sim/rdac_vds.txt")
    resistance = data_vds[1:]/data_ids[1:]
    Rn = (resistance[0][1]+resistance[0][3]+resistance[2][2]+resistance[2][3])/4
    Rp = (resistance[1][0]+resistance[1][2]+resistance[3][0]+resistance[3][1])/4
    if Rn < mos_resistance and Rp < mos_resistance:
        ready = True
    else:
        number_fingers = number_fingers + 1
        inverter(NMOS_W*number_fingers, PMOS_W*number_fingers, NGn=number_fingers, NGp=number_fingers) # edit the inverter is enough

print('multiplicity=', number_fingers)
print('Rn=', Rn)
print('Rp=', Rp)


# Iterate 
print('\nSimulation')

rdac(RESOLUTION, NMOS_W, PMOS_W, number_fingers, RES_L)
rdac_tb(RESOLUTION)
subprocess.run("openvaf sim/adc_model.va -o sim/adc_model.osdi", shell=True, check=True) 
subprocess.run("ngspice -b sim/rdac_tb.spice -o sim/rdac.log > sim/temp.txt", shell=True, check=True) #!ngspice -b rdac.spice

data_dc = read_data("sim/rdac_dc.txt")
digital_input = np.arange(M)
transfer_function = np.flip(data_dc[1][0:M])
tfunction_ref = digital_input * pdk.LOW_VOLTAGE / M
inl = (transfer_function - tfunction_ref)/LSB
dnl = (transfer_function[1:] - transfer_function[:M-1] - LSB)/LSB

print('Simulated\tINL=', max(abs(inl)), '\tDNL=', max(abs(dnl)))
# while not ready:
#     inl, dnl = estimate_rdac_nl(RESOLUTION, R, mos_resistance, mos_resistance)
#     if max(abs(inl))<1 and max(abs(dnl))<1:
#         ready = True
#     else:
#         mos_resistance = mos_resistance / 2


## here set layout generator parameters to match simulated circuit

# # call layout generation with klayout
# subprocess.run("klayout -zz -r ../klayout/python/rdac_bit.py -j ../klayout/", shell=True, check=True) 


# NMOS_W = 2.0
# MOS_NG = 2
# PMOS_W = 2.5*NMOS_W
# inverter(NMOS_W, PMOS_W, NGn=MOS_NG, NGp=MOS_NG)

# # Extract spice netlist from GDS
# subprocess.run("magic -rcfile "+user.MAGICRC_PATH+" -noconsole -nowrapper ../magic/extract_rdac.tcl", shell=True, check=True)

# # Perform LVS
# subprocess.run("netgen -batch lvs \"../magic/TOP.spice TOP\" \"sim/inverter.spice inverter\" "+user.NETGEN_SETUP+" ../netgen/comp.out", shell=True, check=True)