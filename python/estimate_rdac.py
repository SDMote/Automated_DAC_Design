# ============================================================================
# Resistor DAC estimation
# Alfonso Cortes - Inria AIO
# 
# ============================================================================


RESOLUTION = 4

# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import pdk
from rdac import estimate_rdac_nl, rdac_ideal_tb

R = 100
N = 3
M = 4


resolution = np.zeros(N, dtype=np.uint)
ratio = np.zeros(M)
for j in range(M):
    ratio[j] = 0.75**j
abs_inl = np.zeros((N,M))
abs_dnl = np.zeros((N,M))
for i in range(N):
    resolution[i] = int(RESOLUTION + 4*i)
    Q = 2**resolution[i]
    digital_input = np.arange(Q)
    lsb = pdk.LOW_VOLTAGE/Q
    vref = 2**np.arange(resolution[i])*lsb
    voltages = np.zeros((M, resolution[i]))
    inl = np.zeros((M, Q))
    dnl = np.zeros((M, Q-1))
    fig, axs = plt.subplots(1, 1, sharex=True)
    for j in range(M):
        # inl[j], dnl[j], voltages[j], _ = estimate_rdac_nl(resolution[i], 100*R, ratio[j]*R, R)
        inl[j], dnl[j], voltages[j], _ = estimate_rdac_nl(resolution[i], 29885, ratio[j]*575, 666)
        abs_inl[i][j] = max(abs(inl[j]))
        abs_dnl[i][j] = max(abs(dnl[j]))
        axs.plot(np.arange(resolution[i]), voltages[j]-vref, '-', label=str(ratio[j]))
    # axs.plot(np.arange(RESOLUTION), vref, '--', label='calculated')
    axs.set_ylabel("Bit voltage error")
    axs.legend()
    axs.grid()
    axs.set_title("Estimated bit voltage errors with "+str(resolution[i])+" bits of resolution")
    plt.show()

fig, axs = plt.subplots(N, 1, sharex=True)
for i in range(N):
    axs[i].plot(ratio, abs_inl[i], 'b-o', label='worst inl')
    axs[i].plot(ratio, abs_dnl[i], 'r-o', label='worst dnl')
    axs[i].set_ylabel("Worst nonlinearity (LSB)\nwith "+str(resolution[i])+" bits of resolution")
    axs[i].legend()
    axs[i].grid()
axs[0].set_title("Estimated worst nonlinearities over NMOS/PMOS on-resistance ratio")
plt.show()


fig, axs = plt.subplots(2, 1, sharex=True)
for j in range(M):
    axs[0].plot(digital_input, inl[j], '-', label=str(ratio[j]))
    axs[1].plot(digital_input[1:], dnl[j], '-', label=str(ratio[j]))
axs[0].set_ylabel("INL (LSB)")
axs[0].legend()
axs[0].grid()
axs[1].set_ylabel("DNL (LSB)")
axs[1].legend()
axs[1].grid()
axs[0].set_title("Estimated nonlinearities with "+str(resolution[N-1])+" bits of resolution")
plt.show()


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