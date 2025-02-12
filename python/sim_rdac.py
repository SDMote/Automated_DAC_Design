# ============================================================================
# Resistor DAC simulation
# Alfonso Cortés - Inria AIO
# 
# ============================================================================


RESOLUTION = 8
L_RES = 5.0
W_NMOS = 6.0

# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import pdk

R = 3020*L_RES
Rn = 2745/W_NMOS
Rp = 5868/(2*W_NMOS)

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
voltages = np.zeros(RESOLUTION)
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
    voltages[i] = pdk.LOW_VOLTAGE * k[i] * r_4[i]/(r_4[i] + r_1)

transfer_function = np.zeros(2**RESOLUTION)
for i in range(2**RESOLUTION):
    for j in range(RESOLUTION):
        transfer_function[i] = transfer_function[i] + ((i//2**j)%2)*voltages[j]

digital_input = np.arange(2**RESOLUTION)
lsb = pdk.LOW_VOLTAGE/(2**RESOLUTION)
tfunction_ref = digital_input * pdk.LOW_VOLTAGE / 2**RESOLUTION
inl = (transfer_function - tfunction_ref)/lsb
dnl = (transfer_function[1:] - transfer_function[:2**RESOLUTION-1] - lsb)/lsb

fig, axs = plt.subplots(2, 1, sharex=True)
axs[0].plot(digital_input, transfer_function, '-o', label='transfer function')
axs[0].plot(digital_input, tfunction_ref, '-', label='reference')
axs[0].set_ylabel("Operating point\nVout (V)")
axs[0].legend()
axs[0].grid()
axs[1].plot(digital_input, inl, '-', label='INL')
axs[1].plot(digital_input[1:], dnl, '-', label='DNL')
axs[1].set_ylabel("INL and DNL\nDeviation (LSB)")
axs[1].legend()
axs[1].grid()
axs[0].set_title("Resistive DAC with "+str(RESOLUTION)+" bits of resolution")
plt.show(block=False)

