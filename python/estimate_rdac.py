# ============================================================================
# Resistor DAC estimation
# Alfonso Cortes - Inria AIO
# 
# ============================================================================


RESOLUTION = 4  # initial resolution
N = 5           # number of resolutions
M = 17          # number of ratios
STEP = 2        # resolution step

# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import pdk
from utils import read_data
from spice.rdac import rdac_ideal_tb
from design.rdac import estimate_r2rdac_nl

R = 1500

def ideal_rdac_sim(N: int, R, Rn, Rp):
    """Run ideal RDAC testbench for all codes.
    N: bits of resolution.
    R: Unit resistance value
    Rn: NMOS on resistance
    Rp: PMOS on resistance
    """
    Q = int(2**N)
    digital_input = np.arange(Q)
    lsb = pdk.LOW_VOLTAGE/Q
    transfer_function_ref = digital_input * pdk.LOW_VOLTAGE / Q
    transfer_function = np.zeros(Q)
    for i in range(Q):
        rdac_ideal_tb(N, i, R, Rn, Rp)
        subprocess.run("ngspice -b sim/rdac_ideal_tb.spice -o sim/rdac.log > sim/temp.txt", shell=True, check=True)
        data_dc = read_data("sim/rdac_op.txt")
        transfer_function[i] = data_dc[1][0]
        inl = (transfer_function - transfer_function_ref)/lsb
        dnl = (transfer_function[1:] - transfer_function[:Q-1] - lsb)/lsb
    return inl, dnl, transfer_function

resolution = np.zeros(N, dtype=np.uint)
ratio = np.zeros(M)
for j in range(M):
    ratio[j] = 0.9**j
abs_inl = np.zeros((N,M))
abs_dnl = np.zeros((N,M))
abs_inl2 = np.zeros((N,M))
abs_dnl2 = np.zeros((N,M))
for i in range(N):
    resolution[i] = int(RESOLUTION + STEP*i)
    print("Resolution: ", resolution[i])
    Q = int(2**resolution[i])
    inl = np.zeros((M, Q))
    dnl = np.zeros((M, Q-1))
    for j in range(M):
        # inl[j], dnl[j], _ = estimate_rdac_nl(resolution[i], 29885, ratio[j]*575, 666)
        # inl[j], dnl[j], _ = ideal_rdac_sim(int(resolution[i]), 2*R*2**(STEP*i), ratio[j]*R, R)
        # abs_inl[i][j] = max(abs(inl[j]))
        # abs_dnl[i][j] = max(abs(dnl[j]))
        est_inl, est_dnl, _ = estimate_r2rdac_nl(int(resolution[i]), 2*R*2**(STEP*i), ratio[j]*R, R)
        abs_inl2[i][j] = max(abs(est_inl))
        abs_dnl2[i][j] = max(abs(est_dnl))

# for i in range(N):
#     digital_input = np.arange(Q)
#     fig, axs = plt.subplots(2, 1, sharex=True)
#     for j in range(M):
#         axs[0].plot(digital_input, inl[j], '-o', label='simulated, ratio='+str(ratio[j]))
#         axs[1].plot(digital_input[1:], dnl[j], '-o', label='simulated, ratio='+str(ratio[j]))
#     axs[0].set_ylabel("INL (LSB)")
#     axs[0].legend()
#     axs[0].grid()
#     axs[1].set_ylabel("DNL (LSB)")
#     axs[1].legend()
#     axs[1].grid()
#     axs[0].set_title("Nonlinearity with "+str(resolution[i])+" bits of resolution")
#     plt.show()

fig, axs = plt.subplots(N, 1, sharex=True)
for i in range(N):
    # axs[i].plot(ratio, abs_inl[i], 'b-o', label='worst sim inl')
    # axs[i].plot(ratio, abs_dnl[i], 'b--', label='worst sim dnl')
    axs[i].plot(ratio, abs_inl2[i], 'r-+', label='estimated inl')
    axs[i].plot(ratio, abs_dnl2[i], 'r--', label='estimated dnl')
    axs[i].set_ylabel("Worst nonlinearity (LSB)\nwith "+str(resolution[i])+" bits of resolution")
    axs[i].legend()
    axs[i].grid()
axs[N-1].set_xlabel("NMOS on-resistance / PMOS on-resistance ratio")
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