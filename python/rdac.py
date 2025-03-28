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
from dac import adc_va

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
    fp = open("sim/rdac.spice", "w")
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


def rdac_tb(N: int, debug=False):
    """Generates SPICE testbench for RDAC.
    N: bits of resolution.
    type: DAC topology to be tested.
    debug: when True, testbench saves internal voltages and currents.
    """
    adc_va(N)
    lsb = pdk.LOW_VOLTAGE/2**N  # this is only to use the adc
    ports = ""
    for i in range(N):
        ports = ports + " d" + str(i)
    fp = open("sim/rdac_tb.spice", "w")
    fp.write("** "+str(N)+"-Bit DAC testbench **\n")
    fp.write("\n")
    fp.write(pdk.LIB_MOS_TT)
    fp.write(pdk.LIB_RES_T)
    fp.write(".include \"rdac.spice\"\n")
    fp.write(".include \"adc_model.spice\"\n")
    fp.write("\n")
    fp.write("x1 vss vdd" + ports + " vout dac\n")
    fp.write("x2 vin" + ports + " adc\n")
    fp.write("\n")
    fp.write("Vdd vdd 0 "+str(pdk.LOW_VOLTAGE)+"\n")
    fp.write("Vss vss 0 0\n")
    fp.write("Vin vin 0 0\n")
    signals = ""
    for i in range(N):
        #t = 2**i * 10
        signals = signals + " v(d" + str(i) + ")"
        #fp.write("Vd"+str(i)+" d"+str(i)+" 0 dc 0 PULSE(0 1.2 0 1n 1n "+str(t-1)+"n "+str(2*t)+"n)\n")
    fp.write("\n")
    fp.write(".control\n")
    fp.write("save v(vin)" + signals + " v(vout)\n")
    if debug:
        nodes = ""
        currents = ""
        voltages = ""
        if type == 0:
            for i in range(N):
                if i < N-1:
                    nodes = nodes + " x1.net" + str(2*i)
                currents = currents + " @n.x1.x"+str(2*i+2)+".xm1.nsg13_lv_nmos[ids] @n.x1.x"+str(2*i+2)+".xm2.nsg13_lv_pmos[ids]"
                voltages = voltages + " @n.x1.x"+str(2*i+2)+".xm1.nsg13_lv_nmos[vds] @n.x1.x"+str(2*i+2)+".xm2.nsg13_lv_pmos[vds]"
            fp.write("save" + nodes + "\n")
        else:
            for i in range(N):
                currents = currents + " @n.x1.x"+str(2**i)+".xm1.nsg13_lv_nmos[ids] @n.x1.x"+str(2**i)+".xm2.nsg13_lv_pmos[ids]"
                voltages = voltages + " @n.x1.x"+str(2**i)+".xm1.nsg13_lv_nmos[vds] @n.x1.x"+str(2**i)+".xm2.nsg13_lv_pmos[vds]"
        fp.write("save" + currents + "\n")
        fp.write("save" + voltages + "\n")
    fp.write("dc Vin "+str(lsb/2)+" "+str(lsb*2**N)+" "+str(lsb)+"\n")
    if debug:
        fp.write("wrdata "+user.SIM_PATH+"/rdac_dc.txt vout"+nodes+"\n")
        fp.write("wrdata "+user.SIM_PATH+"/rdac_ids.txt"+currents+"\n")
        fp.write("wrdata "+user.SIM_PATH+"/rdac_vds.txt"+voltages+"\n")
    else:
        fp.write("wrdata "+user.SIM_PATH+"/rdac_dc.txt vout\n")
    fp.write(".endc\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return


def rdac_tb_tran(N: int, C, type=0):
    """Generates SPICE testbench to measure RDAC worst rise time.
    N: bits of resolution.
    C: load capacitance in picofarad.
    type: DAC topology to be tested.
    """
    dut_spice="rdac.spice"
    if type == 0:
        lsb = pdk.LOW_VOLTAGE/2**N
    else:
        lsb = pdk.LOW_VOLTAGE/(2**N-1)
    vin = " vin"
    fp = open("sim/rdac_tb_tran.spice", "w")
    fp.write("** Resistive ladder DAC testbench **\n")
    fp.write("\n")
    fp.write(pdk.LIB_MOS_TT)
    fp.write(pdk.LIB_RES_T)
    fp.write(".include \""+dut_spice+"\"\n")
    fp.write("\n")
    fp.write("x1 vss vdd" + vin*N + " vout rdac\n")
    fp.write("C1 vout 0 " + str(C) + "p\n")
    fp.write("\n")
    fp.write("Vdd vdd 0 "+str(pdk.LOW_VOLTAGE)+"\n")
    fp.write("Vss vss 0 0\n")
    fp.write("Vin vin 0 PULSE(1.2 0 1u 1p 1p 1m 2m)\n")
    fp.write("\n")
    fp.write(".control\n")
    fp.write("save v(vin) v(vout)\n")
    fp.write("tran 0.001 1m\n")
    Vhigh = pdk.LOW_VOLTAGE - lsb
    fp.write("meas tran t1 find time when v(vout)="+str(0.1*Vhigh)+" TD=0 RISE=1\n")
    fp.write("meas tran t2 find time when v(vout)="+str(0.9*Vhigh)+" TD=0 RISE=1\n")
    fp.write("wrdata "+user.SIM_PATH+"/rdac_tran.txt t2-t1\n")
    fp.write(".endc\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return


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
