# ============================================================================
# Resistor DAC estimation
# Alfonso Cortés - Inria AIO
# 
# ============================================================================


RESOLUTION = 10
RES_L = 10.0
NMOS_W = 0.2
MOS_M = 6

# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import pdk
import user
from utils import read_data, net
from inverter import nmos_tb, pmos_tb
from rdac import resistor_tb, estimate_rdac_nl

# W_PMOS = 2.5*W_NMOS
# resistor_tb(L_RES)
# subprocess.run("ngspice -b sim/resistor_tb.spice -o sim/resistor.log > sim/temp.txt", shell=True, check=True)
# data_op_res = read_data("sim/resistor_op.txt")
# R = data_op_res[0][0]/data_op_res[1][0]

# nmos_tb(W_NMOS, M=M_MOS)
# pmos_tb(W_PMOS, M=M_MOS)
# subprocess.run("ngspice -b sim/nmos_tb.spice -o sim/nmos.log > sim/temp.txt", shell=True, check=True)
# subprocess.run("ngspice -b sim/pmos_tb.spice -o sim/pmos.log > sim/temp.txt", shell=True, check=True)
# data_op_nmos = read_data("sim/nmos_op.txt")
# data_op_pmos = read_data("sim/pmos_op.txt")
# Rn = data_op_nmos[0][0]/data_op_nmos[1][0]
# Rp = (pdk.LOW_VOLTAGE-data_op_pmos[0][0])/data_op_pmos[1][0]

R = 3020*RES_L
Rn = 520.9 #2730/(W_NMOS*M_MOS)
Rp = 613.4 #5851/(W_PMOS*M_MOS)

N = 2**RESOLUTION
digital_input = np.arange(N)
lsb = pdk.LOW_VOLTAGE/N
transfer_function_ref = digital_input * pdk.LOW_VOLTAGE / N

voltages = np.zeros(RESOLUTION)
for j in range(RESOLUTION):
    fp = open("sim/rdac_tb.spice", "w")
    fp.write("** Resistive ladder DAC **\n")
    fp.write("\n")
    fp.write(pdk.LIB_RES_T)
    fp.write("\n")
    fp.write("XR1 0 net1 rhigh w=0.5u l="+str(2*RES_L)+"u m=1 b=0\n")
    for i in range(RESOLUTION-2):
        fp.write("XR"+str(i+2)+net(i+1)+net(i+2)+" rhigh w=0.5u l="+str(RES_L)+"u m=1 b=0\n")
    fp.write("XR"+str(RESOLUTION)+" net"+str(RESOLUTION-1)+" vout rhigh w=0.5u l="+str(RES_L)+"u m=1 b=0\n")
    for i in range(RESOLUTION-1):
        fp.write("XR"+str(RESOLUTION+i+1)+net(i+1)+net(RESOLUTION+i)+" rhigh w=0.5u l="+str(2*RES_L)+"u m=1 b=0\n")
        if i == j:
            fp.write("R"+str(i)+" d"+str(i)+net(RESOLUTION+i)+" "+str(Rp)+"\n")
            fp.write("Vd"+str(i)+" d"+str(i)+" 0 "+str(pdk.LOW_VOLTAGE)+"\n")
        else:
            fp.write("R"+str(i)+" d"+str(i)+net(RESOLUTION+i)+" "+str(Rn)+"\n")
            fp.write("Vd"+str(i)+" d"+str(i)+" 0 0\n")
    fp.write("XR"+str(2*RESOLUTION)+" vout"+net(2*RESOLUTION-1)+" rhigh w=0.5u l="+str(2*RES_L)+"u m=1 b=0\n")
    if j == RESOLUTION-1:
        fp.write("R"+str(RESOLUTION-1)+" d"+str(RESOLUTION-1)+net(2*RESOLUTION-1)+" "+str(Rp)+"\n")
        fp.write("Vd"+str(RESOLUTION-1)+" d"+str(RESOLUTION-1)+" 0 "+str(pdk.LOW_VOLTAGE)+"\n")
    else:
        fp.write("R"+str(RESOLUTION-1)+" d"+str(RESOLUTION-1)+net(2*RESOLUTION-1)+" "+str(Rn)+"\n")
        fp.write("Vd"+str(RESOLUTION-1)+" d"+str(RESOLUTION-1)+" 0 0\n")
    fp.write("\n")
    fp.write(".control\n")
    fp.write("save v(vout)\n")
    fp.write("op\n")
    fp.write("wrdata "+user.SIM_PATH+"/rdac_op.txt vout\n")
    fp.write(".endc\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    
    subprocess.run("ngspice -b sim/rdac_tb.spice -o sim/rdac.log > sim/temp.txt", shell=True, check=True) #!ngspice -b rdac.spice
    data_dc = read_data("sim/rdac_op.txt")
    voltages[j] = data_dc[1][0]

print(voltages)

transfer_function = np.zeros(N)
for i in range(N):
    for j in range(RESOLUTION):
        transfer_function[i] = transfer_function[i] + ((i//2**j)%2)*voltages[j]

inl = (transfer_function - transfer_function_ref)/lsb
dnl = (transfer_function[1:] - transfer_function[:N-1] - lsb)/lsb

r_1 = 2*R + Rp
r_2 = np.zeros(RESOLUTION)
r_3 = np.zeros(RESOLUTION)
r_4 = np.zeros(RESOLUTION)
k = np.zeros(RESOLUTION)
temp = 2*R + Rn

r_3[RESOLUTION-1] = float('inf')
r_3[RESOLUTION-2] = 3*R + Rn
k[RESOLUTION-1] = 1
k[RESOLUTION-2] = temp / (temp + R)
voltages2 = np.zeros(RESOLUTION)
for i in range(RESOLUTION-3, -1, -1):
    temp2 = temp*r_3[i+1]/(temp + r_3[i+1])
    r_3[i] = R + temp2
    k[i] = k[i+1] * temp2/r_3[i]
for i in range(RESOLUTION):
    if i == 0:
        r_2[0] = 2*R
    else:
        r_2[i] = R + temp*r_2[i-1]/(temp + r_2[i-1])
    if i == RESOLUTION-1:
        r_4[i] = r_2[i]
    else:
        r_4[i] = r_2[i]*r_3[i]/(r_2[i] + r_3[i])
    voltages2[i] = pdk.LOW_VOLTAGE * k[i] * r_4[i]/(r_4[i] + r_1)

transfer_function2 = np.zeros(N)
for i in range(N):
    for j in range(RESOLUTION):
        transfer_function2[i] = transfer_function2[i] + ((i//2**j)%2)*voltages2[j]

inl2 = (transfer_function2 - transfer_function_ref)/lsb
dnl2 = (transfer_function2[1:] - transfer_function2[:N-1] - lsb)/lsb

print("R:\t\t", R, "Ohm")
print("Rn:\t\t", Rn, "Ohm")
print("Rp:\t\t", Rp, "Ohm")

# fig, axs = plt.subplots(2, 1, sharex=True)
# axs[0].plot(digital_input, transfer_function, '-o', label='transfer function')
# axs[0].plot(digital_input, transfer_function2, '-o', label='transfer function 2')
# axs[0].plot(digital_input, transfer_function_ref, '-', label='reference')
# axs[0].set_ylabel("Operating point\nVout (V)")
# axs[0].legend()
# axs[0].grid()
# axs[1].plot(digital_input, inl, '-', label='INL')
# axs[1].plot(digital_input[1:], dnl, '-', label='DNL')
# axs[1].plot(digital_input, inl2, '-', label='INL 2')
# axs[1].plot(digital_input[1:], dnl2, '-', label='DNL 2')
# axs[1].set_ylabel("INL and DNL\nDeviation (LSB)")
# axs[1].legend()
# axs[1].grid()
# axs[0].set_title("Resistive DAC with "+str(RESOLUTION)+" bits of resolution")
# plt.show()

R1 = 500
R2 = 250
inl, dnl = estimate_rdac_nl(RESOLUTION, R, R1, R1)
inl2, dnl2 = estimate_rdac_nl(RESOLUTION, R, R2, R2)


fig, axs = plt.subplots(2, 1, sharex=True)
axs[0].plot(digital_input, inl, '-', label='Rn=Rp=500')
axs[0].plot(digital_input, inl2, '-', label='Rn=Rp=250')
axs[0].set_ylabel("INL (LSB)")
axs[0].legend()
axs[0].grid()
axs[1].plot(digital_input[1:], dnl, '-', label='Rn=Rp=500')
axs[1].plot(digital_input[1:], dnl2, '-', label='Rn=Rp=250')
axs[1].set_ylabel("DNL (LSB)")
axs[1].legend()
axs[1].grid()
axs[1].set_xlabel("Code")
axs[0].set_title("Nonlinearity estimations with "+str(RESOLUTION)+" bits of resolution")
plt.show()