# ============================================================================
# Functions for automated design of RDAC
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import numpy as np
import subprocess
from pdk import *
from utils import read_data, dbu, um
from spice.common import inverter
from design.common import measure_resistance
from spice.dac import dac_tb, dac_tb_tran
from spice.rdac import rdac, r2r_ladder


def estimate_r2rdac_nl(N: int, R, Rn, Rp):
    """Estimate RDAC nonlinearities.
    N: bits of resolution.
    R: RDAC unit resistance.
    Rn: NMOS on resistance.
    Rp: PMOS on resistance.
    return: INL, DNL arrays of size 2^N and 2^N-1 (normalized to LSB).
    """
    Q = int(2**N)
    digital_input = np.arange(Q)
    lsb = LOW_VOLTAGE/Q
    transfer_function_ref = digital_input * LOW_VOLTAGE / Q

    temp = [2*R + Rn, 2*R + Rp]
    r_1 = temp[1]
    r_2 = np.zeros((N, Q//2))
    r_3 = np.zeros((N, Q//2))
    r_4 = np.zeros(N)
    # r_th = np.zeros(Q)
    k = np.zeros((N, Q//2))

    r_2[0][0] = 2*R
    for j in range(N-1):
        for i in range(2**j):
            r_2[j+1][i] = R + temp[0]*r_2[j][i]/(temp[0] + r_2[j][i])
            r_2[j+1][2**j+i] = R + temp[1]*r_2[j][i]/(temp[1] + r_2[j][i])
    r_th = r_2[N-1][Q//2-1] * temp[1] / (r_2[N-1][Q//2-1] + temp[1])
    # for i in range(Q//2):
    #     r_th[2*i] = r_2[N-1][i] * temp[0] / (r_2[N-1][i] + temp[0])
    #     r_th[2*i+1] = r_2[N-1][i] * temp[1] / (r_2[N-1][i] + temp[1])

    r_3[N-1][0] = float('inf')
    r_3[N-2][0] = R + temp[0]
    r_3[N-2][1] = R + temp[1]
    k[N-1][0] = 1
    k[N-2][0] = temp[0] / (temp[0] + R)
    k[N-2][1] = temp[1] / (temp[1] + R)
    for j in range(N-3, -1, -1):
        for i in range(2**(N-1-j)):
            temp2 = temp[i%2]*r_3[j+1][i//2]/(temp[i%2] + r_3[j+1][i//2])
            r_3[j][i] = R + temp2
            k[j][i] = k[j+1][i//2] * temp2/r_3[j][i]

    transfer_function = np.zeros(Q)
    for i in range(Q):
        for j in range(N):
            if (i//2**j)%2:
                if j == N-1:
                    r_4 = r_2[N-1][i%(2**j)]
                else:
                    r_4 = r_2[j][i%(2**j)]*r_3[j][i//2**(j+1)]/(r_2[j][i%(2**j)]+r_3[j][i//2**(j+1)])
                transfer_function[i] = transfer_function[i] + LOW_VOLTAGE * k[j][i//2**(j+1)] * r_4 / (r_4 + r_1)
    inl = (transfer_function - transfer_function_ref)/lsb
    dnl = (transfer_function[1:] - transfer_function[:Q-1] - lsb)/lsb
    return inl, dnl, transfer_function, r_th


def sim2bits (Wn, Wp, NF=1):
    # requires running dac() and dac_tb() first for resolution 2
    # works for both rdac topologies
    Wn, Wp = inverter(Wn, Wp, NGn=NF, NGp=NF) # editing the inverter is enough to update transistor widths
    subprocess.run("ngspice -b sim/dac_tb.spice -o sim/dac.log > sim/temp.txt", shell=True, check=True)
    data_ids = read_data("sim/dac_ids.txt")
    data_vds = read_data("sim/dac_vds.txt")
    resistances = data_vds[1:]/data_ids[1:]
    Rn = (resistances[0][1]+resistances[0][3]+resistances[2][2]+resistances[2][3])/4
    Rp = (resistances[1][0]+resistances[1][2]+resistances[3][0]+resistances[3][1])/4
    return Rn, Rp, Wn, Wp


def set_ron_ratio(Wn, Wp, ratio, NF=1):
    # requires running dac() and dac_tb() first for resolution 2
    # works for R2R-ladder rdac
    Wn = dbu(Wn)
    Wp = dbu(Wp)
    MIN = int(GRID / DBU)
    Rn, Rp, _, _ = sim2bits (Wn, Wp, NF)
    done = 0
    if Rn < ratio*Rp:   # edit PMOS width
        target  = Rn / ratio
        step = dbu(((Rp * Wp) / target - Wp) / NF)  # round to minimum possible width change
        # print(" With Wn=", um(Wn), " and Wp=", um(Wp), ", Rn=", Rn, ", Rp=", Rp, " and distance=", step)
        while not done and step != 0:
            if abs(step) <= MIN:
                done = 1
            Wp = Wp + NF * step
            Rn, Rp, _, _ = sim2bits (Wn, Wp, NF)
            target  = Rn / ratio
            step = dbu(((Rp * Wp) / target - Wp)/NF)
            if done == 1 and step > MIN:
                done = 0
            # print(" With Wn=", um(Wn), " and Wp=", um(Wp), ", Rn=", Rn, ", Rp=", Rp, " and distance=", step)
    else:               # edit NMOS width
        target  = Rp * ratio
        step = dbu(((Rn * Wn) / target - Wn) / NF)  # round to minimum possible width change
        # print(" With Wn=", um(Wn), " and Wp=", um(Wp), ", Rn=", Rn, ", Rp=", Rp, " and distance=", step)
        while not done and step != 0:
            if abs(step) <= MIN:
                done = 1
            Wn = Wn + NF * step
            Rn, Rp, _, _ = sim2bits (Wn, Wp, NF)
            target  = Rp * ratio
            step = dbu(((Rn * Wn) / target - Wn)/NF) 
            if done == 1 and step > MIN:
                done = 0
            # print(" With Wn=", um(Wn), " and Wp=", um(Wp), ", Rn=", Rn, ", Rp=", Rp, " and distance=", step)
    # print("Ratio=", Rn/Rp)
    return Rn, Rp, Wn, Wp


def design_r2r_rdac(N, ideal_width, Nr, max_nl, target_R_th, POLY_W):
    MIN_STEP = GRID/DBU
    # Estimate on-resistances ratio
    print("\nResistance estimation:")
    R = 1
    Rp = R/10
    if ideal_width: # on resistance ratio that minimizes both nonlinearities
        inl, dnl, _, _ = estimate_r2rdac_nl(N, R, 0.2*Rp, Rp)
        worst_inl_1 = max(abs(inl))
        worst_dnl_1 = max(abs(dnl))
        inl, dnl, _, _ = estimate_r2rdac_nl(N, R, Rp, Rp)
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
    inl, dnl, _ , _ = estimate_r2rdac_nl(N, R, ratio*Rp, Rp)
    # print(" With R=", R, "Rn=", ratio*Rp, "and Rp=", Rp)
    # print(" Estimate => INL: ", max(abs(inl)), " DNL: ", max(abs(dnl)))
    worst_nl = max(max(abs(inl)), max(abs(dnl)))
    R = R * worst_nl / max_nl       # first approximation
    inl, dnl, _ , _ = estimate_r2rdac_nl(N, R, ratio*Rp, Rp)
    worst_nl = max(max(abs(inl)), max(abs(dnl)))
    R = R * worst_nl / max_nl       # second approximation
    k = 1/(R // Rp)
    inl, dnl, _ , R_th = estimate_r2rdac_nl(N, R, ratio*k*R, k*R)
    target_R = R * target_R_th / R_th
    target_Rp = k*target_R
    target_Rn = ratio*k*target_R
    inl, dnl, _ , R_th = estimate_r2rdac_nl(N, target_R, target_Rn, target_Rp)
    print(" With R=", target_R, "Rn=", target_Rn, "and Rp=", target_Rp)
    print(" Estimate => INL: ", max(abs(inl)), " DNL: ", max(abs(dnl)), " R_th=", R_th)

    # Simulate required resistance lenght fot target R (iteratively)
    print("\nResistor size simulation:")
    Lr = RES_MIN_L * Nr  # default unit resistor lenght (total for all series devices)
    R = measure_resistance(Lr, Nr)
    # r_resistivity = R / RES_L
    # print("R min: ", R, " resistivity: ", r_resistivity)
    step = dbu((Lr * target_R / R - Lr) / Nr)
    done = 0
    while not done and step != 0:
        if abs(step) <= MIN_STEP:
            done = 1
        Lr = Lr + Nr * step
        R = measure_resistance(Lr, Nr)
        step = dbu((Lr * target_R / R - Lr) / Nr)
    r2r_ladder(Lr, Nr)       # editing the ladder is enough to update unit resistor lenght
    print(" With Lr=", um(Lr), "R=", R)

    # Simulate required Wn, Wp for target Rn, Rp mantaining ratio (iteratively)
    print("\nInverter size simulation:")
    Wn = Wp = MOS_MIN_W
    rdac(2, Wn, Wp, 1, Lr, 0, Nr)
    dac_tb(2, debug=True, type=0)
    subprocess.run("openvaf sim/adc_model.va -o sim/adc_model.osdi", shell=True, check=True) 
    Rn, Rp, Wn, Wp = set_ron_ratio(Wn, Wp, ratio)   # first approximation
    equivalent_inverter_width = 2 * max(Wp * Rp / target_Rp, Wn * Rn / target_Rn)
    INVERTER_CONST_WIDTH = 2 * ( max(RHIa/2 + M1b, GATd+POLY_W/2, (NWc+NWd)/2, (300+PSDb+PSDc1)/2) + max(M1b, GATd + CNTd) + CNTd + CNTa + GATb/2 )
    if Nr == 2:     # fixed width ladder layout 2
        BIT_WIDTH = 3960   
    else:                   # variable width ladder layout 1
        BIT_WIDTH = Lr + 1000 # check constant from layout
    MAX_INVERTER_WIDTH = BIT_WIDTH - INVERTER_CONST_WIDTH  
    fingers = int(equivalent_inverter_width // MAX_INVERTER_WIDTH + 1)   # Estimate inverter equivalent width to determine NF
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
        fingers_next = int(equivalent_inverter_width // MAX_INVERTER_WIDTH + 1)
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
            
    inl, dnl, _, R_th = estimate_r2rdac_nl(N, R, Rn, Rp)
    print(" With Wn=", um(Wn), " Wp=", um(Wp), " and NG=", fingers, ", then Rn=", Rn, "Rp=", Rp)
    print(" Estimate => INL: ", max(abs(inl)), " DNL: ", max(abs(dnl)), " R_th", R_th)
    params = {'Wn':Wn, 'Wp':Wp, 'Ng':fingers, 'Lr':Lr, 'Nr':Nr}
    return params, BIT_WIDTH


def design_weighted_rdac(N, max_nl, target_R_th, POLY_W):
    MIN_STEP = GRID/DBU
    ratio = 1

    target_R = 1000
    # Simulate required resistance lenght fot target R (iteratively)
    print("\nResistor size simulation:")
    Lr = RES_MIN_L  # default unit resistor lenght (total for all series devices)
    R = measure_resistance(Lr)
    # r_resistivity = R / RES_L
    # print("R min: ", R, " resistivity: ", r_resistivity)
    step = dbu(Lr * target_R / R - Lr)
    done = 0
    while not done and step != 0:
        if abs(step) <= MIN_STEP:
            done = 1
        Lr = Lr + step
        R = measure_resistance(Lr)
        step = dbu(Lr * target_R / R - Lr)
    r2r_ladder(Lr)       # editing the ladder is enough to update unit resistor lenght
    print(" With Lr=", um(Lr), "R=", R)

    params = {'Wn':500, 'Wp':1000, 'Ng':2, 'Lr':Lr}
    return params