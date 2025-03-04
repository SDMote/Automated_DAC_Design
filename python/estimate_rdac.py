# ============================================================================
# Resistor DAC estimation
# Alfonso Cortes - Inria AIO
# 
# ============================================================================


RESOLUTION = 8

# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import pdk
from rdac import estimate_rdac_nl, rdac_ideal_tb

R = 100
M = 5

N = 2**RESOLUTION
digital_input = np.arange(N)
lsb = pdk.LOW_VOLTAGE/N
vref = 2**np.arange(RESOLUTION)*lsb

ratio = np.zeros(M)
max_inl = np.zeros(M)
max_dnl = np.zeros(M)
min_inl = np.zeros(M)
min_dnl = np.zeros(M)
voltages = np.zeros((M, RESOLUTION))
voltages2 = np.zeros((M, RESOLUTION))
fig, axs = plt.subplots(1, 1, sharex=True)
for i in range(M):
    ratio[i] = 10**i
    # inl, dnl, voltages[i] = rdac_ideal_tb(RESOLUTION, ratio[i]*R, R, R)
    inl, dnl, voltages[i] = estimate_rdac_nl(RESOLUTION, ratio[i]*R, R, R)
    inl2, dnl2, voltages2[i] = estimate_rdac_nl(RESOLUTION, ratio[i]*R, R, 0.75*R)
    max_inl[i] = max(inl2)
    max_dnl[i] = max(dnl2)
    min_inl[i] = min(inl2)
    min_dnl[i] = min(dnl2)
    axs.plot(np.arange(RESOLUTION), voltages[i]-vref, '-o', label='ideal sim '+str(ratio[i]))
    axs.plot(np.arange(RESOLUTION), voltages2[i]-vref, '-', label='calculated '+str(ratio[i]))
# axs.plot(np.arange(RESOLUTION), vref, '--', label='calculated')
axs.set_ylabel("INL (LSB)")
axs.legend()
axs.grid()
axs.set_title("Nonlinearity estimations with "+str(RESOLUTION)+" bits of resolution")
plt.show()

# fig, axs = plt.subplots(2, 1, sharex=True)
# axs[0].plot(digital_input, inl, '-', label='ideal sim')
# axs[0].plot(digital_input, inl2, '-', label='calculated')
# axs[0].set_ylabel("INL (LSB)")
# axs[0].legend()
# axs[0].grid()
# axs[1].plot(digital_input[1:], dnl, '-', label='ideal sim')
# axs[1].plot(digital_input[1:], dnl2, '-', label='calculated')
# axs[1].set_ylabel("DNL (LSB)")
# axs[1].legend()
# axs[1].grid()
# axs[0].set_title("Nonlinearity estimations with "+str(RESOLUTION)+" bits of resolution")
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