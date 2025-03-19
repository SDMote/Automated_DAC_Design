# ============================================================================
# Resistor DAC estimation
# Alfonso Cortes - Inria AIO
# 
# ============================================================================


RESOLUTION = 4  # initial resolution
N = 3           # number of resolutions
M = 17          # number of ratios
STEP = 2        # resolution step

# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import pdk
from rdac import rdac_tb, rdac, estimate_rdac_nl, rdac_ideal_tb
from bit import resistor_tb, inverter
from utils import read_data

RES_L = 1000
NMOS_W = 500
PMOS_W = 3*NMOS_W
NG = 1

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
    ratio[j] = 1.1**j
abs_inl = np.zeros(M)
abs_dnl = np.zeros(M)
abs_inl2 = np.zeros(M)
abs_dnl2 = np.zeros(M)
abs_inl3 = np.zeros(M)
abs_dnl3 = np.zeros(M)
fig, axs = plt.subplots(N, 1, sharex=True)
for i in range(N):
    resolution[i] = int(RESOLUTION + STEP*i)
    print("\nResolution: ", resolution[i])
    Q = 2**resolution[i]
    lsb = pdk.LOW_VOLTAGE/Q
    vref = 2**np.arange(resolution[i])*lsb
    digital_input = np.arange(Q)
    tfunction_ref = digital_input * pdk.LOW_VOLTAGE / Q
    rdac(resolution[i], NMOS_W, PMOS_W, NG, RES_L*2**(STEP*i), 1)
    rdac_tb(resolution[i], debug=True)
    subprocess.run("openvaf sim/adc_model.va -o sim/adc_model.osdi", shell=True, check=True) 
    # measure R
    resistor_tb(RES_L*2**(2*i))
    subprocess.run("ngspice -b sim/resistor_tb.spice -o sim/resistor.log > sim/temp.txt", shell=True, check=True)
    data_op_res = read_data("sim/resistor_op.txt")
    R = data_op_res[0][0]/data_op_res[1][0]
    print("Unit resistor: ", R)
    r_ratio = np.zeros(M)
    Rn = np.zeros((resolution[i], Q//2))
    Rp = np.zeros((resolution[i], Q//2))
    for j in range(M):
        inverter(ratio[j]*NMOS_W, PMOS_W, NGn=1, NGp=1)
        subprocess.run("ngspice -b sim/rdac_tb.spice -o sim/rdac.log > sim/temp.txt", shell=True, check=True)
        # measure out voltages (transfer function) to get nonlinearities
        data_dc = read_data("sim/rdac_dc.txt")
        transfer_function = np.flip(data_dc[1][0:Q])
        inl = (transfer_function - tfunction_ref)/lsb
        dnl = (transfer_function[1:] - transfer_function[:Q-1] - lsb)/lsb
        abs_inl[j] = max(abs(inl))
        abs_dnl[j] = max(abs(dnl))
        # measure on-resistances
        data_ids = read_data("sim/rdac_ids.txt")
        data_vds = read_data("sim/rdac_vds.txt")
        resistance = data_vds[1:]/data_ids[1:]
        for k in range(resolution[i]):
            condition = ((digital_input//2**k)%2)
            Rn[k] = resistance[2*k][condition==1]
            Rp[k] = resistance[2*k+1][condition==0]
        Rn_mean = np.mean(Rn)
        Rp_mean = np.mean(Rp)
        r_ratio[j] = Rn_mean / Rp_mean
        print("  NMOS/PMOS on-resistance ratio: ", Rn_mean, "/", Rp_mean, " = ", r_ratio[j])
        # estimate nonlinearities with ideal simulation
        inl2, dnl2, _ = ideal_rdac_sim(resolution[i], R, Rn_mean, Rp_mean)
        abs_inl2[j] = max(abs(inl2))
        abs_dnl2[j] = max(abs(dnl2))
        # estimate nonlinearities with calculation
        inl3, dnl3, _ = estimate_rdac_nl(resolution[i], R, Rn_mean, Rp_mean)
        abs_inl3[j] = max(abs(inl3))
        abs_dnl3[j] = max(abs(dnl3))
    axs[i].plot(r_ratio, abs_inl, 'b-o', label='simulated inl')
    axs[i].plot(r_ratio, abs_dnl, 'b--', label='simulated dnl')
    axs[i].plot(r_ratio, abs_inl2, 'r-o', label='ideal sim inl')
    axs[i].plot(r_ratio, abs_dnl2, 'r--', label='ideal sim dnl')
    axs[i].plot(r_ratio, abs_inl3, 'g-o', label='estimated inl')
    axs[i].plot(r_ratio, abs_dnl3, 'g--', label='estimated dnl')
    axs[i].set_ylabel("worst nonlinearity (LSB)\nwith "+str(resolution[i])+" bits of resolution")
    axs[i].legend()
    axs[i].grid()
axs[N-1].set_xlabel("NMOS on-resistance / PMOS on-resistance ratio")
axs[0].set_title("Simulated worst nonlinearity over NMOS/PMOS on-resistance ratio")
plt.show()

