# ============================================================================
# Tests that shows on-resistances depend weakly on the input code
# Alfonso Cortes - Inria AIO
# 
# ============================================================================


RESOLUTION = 8
RES_L = 10000
NMOS_W = 6*200
NG = 1

# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import pdk
from utils import read_data
from dac import dac_tb
from rdac import rdac, estimate_r2rdac_nl
from bit import resistor_tb

PMOS_W = 2.5*NMOS_W
N = 2**RESOLUTION
LSB = pdk.LOW_VOLTAGE/N
digital_input = np.arange(N)

resistor_tb(RES_L)
subprocess.run("ngspice -b sim/resistor_tb.spice -o sim/resistor.log > sim/temp.txt", shell=True, check=True)
data_op_res = read_data("sim/resistor_op.txt")
R = data_op_res[0][0]/data_op_res[1][0]

dac_tb(RESOLUTION, debug=True)
subprocess.run("openvaf sim/adc_model.va -o sim/adc_model.osdi", shell=True, check=True)
rdac(RESOLUTION, NMOS_W, PMOS_W, NG, RES_L, 1)
print("Running SPICE")
subprocess.run("ngspice -b sim/rdac_tb.spice -o sim/rdac.log > sim/temp.txt", shell=True, check=True)

data_dc = read_data("sim/rdac_dc.txt")
transfer_function = np.flip(data_dc[1][0:N])
tfunction_ref = digital_input * pdk.LOW_VOLTAGE / N
inl = (transfer_function - tfunction_ref)/LSB
dnl = (transfer_function[1:] - transfer_function[:N-1] - LSB)/LSB
print("INL: ",max(abs(inl)))
print("DNL: ",max(abs(dnl)))

data_ids = read_data("sim/rdac_ids.txt")
data_vds = read_data("sim/rdac_vds.txt")
resistance = data_vds[1:]/data_ids[1:]

Rn = np.zeros((RESOLUTION, N//2))
Rp = np.zeros((RESOLUTION, N//2))
for i in range(RESOLUTION):
    condition = ((digital_input//2**i)%2)
    Rn[i] = resistance[2*i][condition==1]
    Rp[i] = resistance[2*i+1][condition==0]

Rn_mean = np.mean(Rn)
Rp_mean = np.mean(Rp)
# Rn_max = np.max(Rn)
# Rp_max = np.max(Rp)
# Rn_min = np.min(Rn)
# Rp_min = np.min(Rp)
print("R :", R)
print("Rn :", Rn_mean)
print("Rp :", Rp_mean)
inl2, dnl2, _, _ = estimate_r2rdac_nl(RESOLUTION, R, Rn_mean, Rp_mean)
# inl3, dnl3, _, _ = estimate_rdac_nl(RESOLUTION, R, Rn_min, Rp_max)
# inl4, dnl4, _, _ = estimate_rdac_nl(RESOLUTION, R, Rn_max, Rp_min)
print("INL: ",max(abs(inl2)))
print("DNL: ",max(abs(dnl2)))

fig, axs = plt.subplots(2, 1, sharex=True)
axs[0].boxplot(Rn.T)
axs[0].grid()
axs[0].set_ylabel("NMOS on resistance (Ohm)")
axs[1].boxplot(Rp.T)
axs[1].grid()
axs[1].set_ylabel("PMOS on resistance (Ohm)")
axs[0].set_title("On resistance distributions for different bit positions")
plt.show()

fig, axs = plt.subplots(2, 1, sharex=True)
axs[0].plot(digital_input, inl, '-', label='inl simulation')
axs[0].plot(digital_input, inl2, '-', label='inl estimation')
# axs[0].plot(digital_input, inl3, '-', label='inl estimation with min N/P ratio')
# axs[0].plot(digital_input, inl4, '-', label='inl estimation with max N/P ratio')
axs[0].legend()
axs[0].grid()
axs[0].set_ylabel("INL (LSB)")
axs[1].plot(digital_input[1:], dnl, '-', label='dnl simulation')
axs[1].plot(digital_input[1:], dnl2, '-', label='dnl estimation')
# axs[1].plot(digital_input[1:], dnl3, '-', label='dnl estimation with min N/P ratio')
# axs[1].plot(digital_input[1:], dnl4, '-', label='dnl estimation with max N/P ratio')
axs[1].legend()
axs[1].grid()
axs[1].set_ylabel("DNL (LSB)")
axs[0].set_title("Nonlinearities with "+str(RESOLUTION)+" bits of resolution")
plt.show()

## Internal voltages
# net0 = data_dc[2]
# net1 = data_dc[3]
# net2 = data_dc[4]
# vout = data_dc[1]
# transfer_function = np.flip(data_dc[1][0:2**RESOLUTION])

# fig, axs = plt.subplots(1, 1, sharex=True)
# axs.plot(digital_input, net0, '-', label='net0')
# axs.plot(digital_input, net1, '-', label='net1')
# axs.plot(digital_input, net2, '-', label='net2')
# axs.plot(digital_input, vout, '-', label='voit')
# axs.set_ylabel("Voltage (V)")
# axs.legend()
# axs.grid()
# axs.set_title("RDAC internal node voltages")
# plt.show()

## transistors voltage and current
# data_ids = read_data("sim/rdac_ids.txt")
# data_vds = read_data("sim/rdac_vds.txt")

# fig, axs = plt.subplots(2, 1, sharex=True)
# for i in range(RESOLUTION):
#     axs[0].plot(digital_input, data_vds[2*i+1], '-', label='vds n'+str(i))
# axs[0].set_ylabel("Voltage (V)")
# axs[0].legend()
# axs[0].grid()
# for i in range(RESOLUTION):
#     axs[1].plot(digital_input, data_vds[2*i+2], '-', label='vds p'+str(i))
# axs[1].set_ylabel("Voltage (V)")
# axs[1].legend()
# axs[1].grid()
# axs[0].set_title("RDAC transistors voltages")
# plt.show()

# fig, axs = plt.subplots(2, 1, sharex=True)
# for i in range(RESOLUTION):
#     axs[0].plot(digital_input, data_ids[2*i+1], '-', label='ids n'+str(i))
# axs[0].set_ylabel("Current (A)")
# axs[0].legend()
# axs[0].grid()
# for i in range(RESOLUTION):
#     axs[1].plot(digital_input, data_ids[2*i+2], '-', label='ids p'+str(i))
# axs[1].set_ylabel("Current (A)")
# axs[1].legend()
# axs[1].grid()
# axs[0].set_title("RDAC transistors currents")
# plt.show()


## check superposition error
# data_dc = read_data("sim/rdac_dc.txt")
# transfer_function = np.flip(data_dc[1][0:2**RESOLUTION])
# voltages = np.zeros(RESOLUTION)
# for i in range(RESOLUTION):
#     voltages[i] = data_dc[1][N-1-2**i]
# transfer_function2 = np.zeros(2**RESOLUTION)
# for i in range(2**RESOLUTION):
#     for j in range(RESOLUTION):
#         transfer_function2[i] = transfer_function2[i] + ((i//2**j)%2)*voltages[j]
# error = 100*(transfer_function[1:]-transfer_function2[1:])/transfer_function[1:]

# fig, axs = plt.subplots(1, 1, sharex=True)
# axs.plot(digital_input[1:], error, '-', label='superposition error')
# axs.set_ylabel("%")
# axs.legend()
# axs.grid()
# axs.set_title("transfer function superposition error")
# plt.show()
