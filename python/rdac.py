# ============================================================================
# Resistor DAC SPICE generation and estimation
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import numpy as np
import user
import pdk
from utils import um, net
from bit import inverter, r2r_ladder


def rdac(N, Wn, Wp, NG=1, Lr=pdk.RES_MIN_L, type=0, Nr=1):
    """Generates SPICE of RDAC, including SPICE for the inverter.
    N: bits of resolution.
    Wn: width of inverter NMOS.
    Wp: width of inverter PMOS.
    NG: number of gates of the transistors.
    Lr: lenght of each resistor instance.
    Nr: number of series resistors in each unit resistor R.
    return: string with RDAC ports.
    """
    fp = open("sim/dac.spice", "w")
    inverter(Wn, Wp, NGn=NG, NGp=NG)
    if type == 0:   # R2R-ladder RDAC
        r2r_ladder(L=Lr, N=Nr)
        fp.write("** Resistive ladder DAC **\n")
        fp.write("\n")
        fp.write(".include \"r2r_bit_0.spice\"\n")
        fp.write(".include \"r2r_bit_i.spice\"\n")
    else:           # 
        fp.write("** Binary-weighted resistor DAC **\n")
        fp.write("\n")
    fp.write(".include \"inverter.spice\"\n")
    fp.write("\n")
    ports = "vss vdd"
    for i in range(N):
        ports = ports + " d" + str(i)
    ports = ports + " vout"
    fp.write(".subckt dac "+ports+"\n")
    if type == 0:
        fp.write("X1 vss net0 net1 r2r_bit_0\n")
        fp.write("X2 vss vdd d0 net1 inverter\n")
        for i in range(N-2):
            fp.write("X"+str(2*i+3)+net(2*i)+net(2*i+2)+net(2*i+3)+" r2r_bit_i\n")
            fp.write("X"+str(2*i+4)+" vss vdd d"+str(i+1)+net(2*i+3)+" inverter\n")
        fp.write("X"+str(2*N-1)+net(2*N-4)+" vout"+net(2*N-2)+" r2r_bit_i\n")
        fp.write("X"+str(2*N)+" vss vdd d"+str(N-1)+net(2*N-2)+" inverter\n")
    else:
        index = 1
        for i in range(N):
            for j in range(2**i):
                fp.write("X"+str(index)+" vss vdd d"+str(i)+net(index)+" inverter\n")
                fp.write("XR"+str(index)+net(index)+" vout rhigh w=0.5u l="+um(Lr)+"u m=1 b=0\n")
                index = index + 1
    fp.write(".ends\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return ports


def rdac_ideal_tb(N: int, i: int, R, Rn, Rp):
    """Generates SPICE testbench for ideal R2R-ladder RDAC.
    N: bits of resolution.
    i: input code.
    R: Unit resistance value
    Rn: NMOS on resistance
    Rp: PMOS on resistance
    """
    fp = open("sim/rdac_ideal_tb.spice", "w")
    fp.write("** Ideal Resistive ladder DAC testbench **\n")
    fp.write("\n")
    fp.write("R1 0 net1 "+str(2*R)+"\n")
    for j in range(N-2):
        fp.write("R"+str(j+2)+net(j+1)+net(j+2)+" "+str(R)+"\n")
    fp.write("R"+str(N)+" net"+str(N-1)+" vout "+str(R)+"\n")
    for j in range(N-1):
        fp.write("R"+str(N+j+1)+net(j+1)+net(N+j)+" "+str(2*R)+"\n")
    fp.write("R"+str(2*N)+" vout"+net(2*N-1)+" "+str(2*R)+"\n")
    for j in range(N):
        if (i//2**j)%2:
            fp.write("R"+str(2*N+j+1)+" d"+str(j)+net(N+j)+" "+str(Rp)+"\n")
        else:
                fp.write("R"+str(2*N+j+1)+" d"+str(j)+net(N+j)+" "+str(Rn)+"\n")
    for j in range(N):
        if (i//2**j)%2:
            fp.write("Vd"+str(j)+" d"+str(j)+" 0 "+str(pdk.LOW_VOLTAGE)+"\n")
        else:
            fp.write("Vd"+str(j)+" d"+str(j)+" 0 0\n")
    fp.write("\n")
    fp.write(".control\n")
    fp.write("save v(vout)\n")
    fp.write("op\n")
    fp.write("wrdata "+user.SIM_PATH+"/rdac_op.txt vout\n")
    fp.write(".endc\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return


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
    lsb = pdk.LOW_VOLTAGE/Q
    transfer_function_ref = digital_input * pdk.LOW_VOLTAGE / Q

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
                transfer_function[i] = transfer_function[i] + pdk.LOW_VOLTAGE * k[j][i//2**(j+1)] * r_4 / (r_4 + r_1)
    inl = (transfer_function - transfer_function_ref)/lsb
    dnl = (transfer_function[1:] - transfer_function[:Q-1] - lsb)/lsb
    return inl, dnl, transfer_function, r_th
