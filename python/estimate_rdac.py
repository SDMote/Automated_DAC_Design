# ============================================================================
# Resistor DAC estimation
# Alfonso Cortes - Inria AIO
# 
# ============================================================================


RESOLUTION = 4

# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import pdk
from utils import read_data
from rdac import estimate_rdac_nl, rdac_ideal_tb

R = 100
N = 2
M = 4

def ideal_rdac_sim(N: int, R, Rn, Rp):
    """Run ideal RDAC testbench for all codes.
    N: bits of resolution.
    R: Unit resistance value
    Rn: NMOS on resistance
    Rp: PMOS on resistance
    """
    Q = int(2**N)
    transfer_function = np.zeros(Q)
    for i in range(Q):
        rdac_ideal_tb(N, i, R, Rn, Rp)
        subprocess.run("ngspice -b sim/rdac_ideal_tb.spice -o sim/rdac.log > sim/temp.txt", shell=True, check=True)
        data_dc = read_data("sim/rdac_op.txt")
        transfer_function[i] = data_dc[1][0]
    return transfer_function

resolution = np.zeros(N, dtype=np.uint)
ratio = np.zeros(M)
for j in range(M):
    ratio[j] = 0.75**j
abs_inl = np.zeros((N,M))
abs_dnl = np.zeros((N,M))
abs_inl2 = np.zeros((N,M))
abs_dnl2 = np.zeros((N,M))
for i in range(N):
    resolution[i] = int(RESOLUTION + 4*i)
    Q = int(2**resolution[i])
    digital_input = np.arange(Q)
    lsb = pdk.LOW_VOLTAGE/Q
    transfer_function_ref = digital_input * pdk.LOW_VOLTAGE / Q
    vref = 2**np.arange(resolution[i])*lsb
    voltages = np.zeros((M, resolution[i]))
    inl = np.zeros((M, Q))
    dnl = np.zeros((M, Q-1))
    for j in range(M):
        # inl[j], dnl[j], voltages[j], _ = estimate_rdac_nl(resolution[i], 29885, ratio[j]*575, 666)
        transfer_function = ideal_rdac_sim(int(resolution[i]), 100*R, ratio[j]*R, R)
        inl[j] = (transfer_function - transfer_function_ref)/lsb
        dnl[j] = (transfer_function[1:] - transfer_function[:Q-1] - lsb)/lsb
        abs_inl[i][j] = max(abs(inl[j]))
        abs_dnl[i][j] = max(abs(dnl[j]))
        est_inl, est_dnl, _ = estimate_rdac_nl(int(resolution[i]), 100*R, ratio[j]*R, R)
        abs_inl2[i][j] = max(abs(est_inl))
        abs_dnl2[i][j] = max(abs(est_dnl))

for i in range(N):
    fig, axs = plt.subplots(2, 1, sharex=True)
    for j in range(M):
        axs[0].plot(digital_input, inl[j], '-o', label='simulated, ratio='+str(ratio[j]))
        axs[1].plot(digital_input[1:], dnl[j], '-o', label='simulated, ratio='+str(ratio[j]))
    axs[0].set_ylabel("INL (LSB)")
    axs[0].legend()
    axs[0].grid()
    axs[1].set_ylabel("DNL (LSB)")
    axs[1].legend()
    axs[1].grid()
    axs[0].set_title("Nonlinearity with "+str(resolution[i])+" bits of resolution")
    plt.show()

fig, axs = plt.subplots(N, 1, sharex=True)
for i in range(N):
    axs[i].plot(ratio, abs_inl[i], 'b-o', label='worst sim inl')
    axs[i].plot(ratio, abs_dnl[i], 'b--', label='worst sim dnl')
    axs[i].plot(ratio, abs_inl2[i], 'r-+', label='worst est inl')
    axs[i].plot(ratio, abs_dnl2[i], 'r--', label='worst est dnl')
    axs[i].set_ylabel("Worst nonlinearity (LSB)\nwith "+str(resolution[i])+" bits of resolution")
    axs[i].legend()
    axs[i].grid()
axs[0].set_title("Estimated worst nonlinearities over NMOS/PMOS on-resistance ratio")
plt.show()


# fig, axs = plt.subplots(2, 1, sharex=True)
# for j in range(M):
#     axs[0].plot(digital_input, inl[j], '-', label=str(ratio[j]))
#     axs[1].plot(digital_input[1:], dnl[j], '-', label=str(ratio[j]))
# axs[0].set_ylabel("INL (LSB)")
# axs[0].legend()
# axs[0].grid()
# axs[1].set_ylabel("DNL (LSB)")
# axs[1].legend()
# axs[1].grid()
# axs[0].set_title("Estimated nonlinearities with "+str(resolution[N-1])+" bits of resolution")
# plt.show()


# inl, dnl, _ = estimate_rdac_nl(RESOLUTION, R, 2*Rn, 2*Rp)

# fig, axs = plt.subplots(2, 1, sharex=True)
# axs[0].plot(digital_input, inl, '-', label='Rn=Rp=500')
# axs[0].plot(digital_input, inl2, '-', label='Rn=Rp=250')
# axs[0].set_ylabel("INL (LSB)")
# axs[0].legend()
# axs[0].grid()
# axs[1].plot(digital_input[1:], dnl, '-', label='Rn=Rp=500')
# axs[1].plot(digital_input[1:], dnl2, '-', label='Rn=Rp=250')
# axs[1].set_ylabel("DNL (LSB)")
# axs[1].legend()
# axs[1].grid()
# axs[1].set_xlabel("Code")
# axs[0].set_title("Nonlinearity estimations with "+str(RESOLUTION)+" bits of resolution")
# plt.show()