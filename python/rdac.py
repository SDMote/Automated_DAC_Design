# ============================================================================
# Resistor DAC SPICE
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import numpy as np
import user
import pdk
from utils import net
from inverter import inverter

def rdac(N, Wn, Wp, M=1, Lr=pdk.RES_MIN_L):
    """Generates SPICE of RDAC, including SPICE for the inverter.
    N: bits of resolution.
    Wn: width of inverter NMOS.
    Wp: width of inverter PMOS.
    Lr: lenght of RDAC unit resistor.
    return: string with RDAC ports.
    """
    inverter(Wn, Wp, Mn=M, Mp=M)
    fp = open("sim/rdac.spice", "w")
    fp.write("** Resistive ladder DAC **\n")
    fp.write("\n")
    fp.write(".include \"inverter.spice\"\n")
    fp.write("\n")
    ports = "vss vdd"
    for i in range(N):
        ports = ports + " d" + str(i)
    ports = ports + " vout"
    fp.write(".subckt rdac "+ports+"\n")
    fp.write("XR1 vss net1 rhigh w=0.5u l="+str(2*Lr)+"u m=1 b=0\n")
    for i in range(N-2):
        fp.write("XR"+str(i+2)+net(i+1)+net(i+2)+" rhigh w=0.5u l="+str(Lr)+"u m=1 b=0\n")
    fp.write("XR"+str(N)+" net"+str(N-1)+" vout rhigh w=0.5u l="+str(Lr)+"u m=1 b=0\n")
    for i in range(N-1):
        fp.write("x"+str(i+1)+" vss vdd d"+str(i)+net(N+i)+" inverter\n")
        fp.write("XR"+str(N+i+1)+net(i+1)+net(N+i)+" rhigh w=0.5u l="+str(2*Lr)+"u m=1 b=0\n")
    fp.write("x"+str(N)+" vss vdd d"+str(N-1)+net(2*N-1)+" inverter\n")
    fp.write("XR"+str(2*N)+" vout"+net(2*N-1)+" rhigh w=0.5u l="+str(2*Lr)+"u m=1 b=0\n")
    fp.write("\n")
    fp.write(".ends\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return ports


def adc_va(N: int):
    """Generates Verilog-A module for N bit ADC.
    N: bits of resolution.
    """
    # Verilog-A model
    ports = "out0"
    for i in range(1,N):
        ports = ports + ", out" + str(i)
    fp = open("sim/adc_model.va", "w")
    fp.write("`include \"constants.h\"\n")
    fp.write("`include \"discipline.h\"\n")
    fp.write("\n")
    fp.write("module adc_va(in, "+ports+") ;\n")
    fp.write("\tinput in ;\n")
    fp.write("\toutput "+ports+" ;\n")
    fp.write("\telectrical in, "+ports+" ;\n")
    fp.write("\tparameter real vlow = 0, vhigh = "+str(pdk.LOW_VOLTAGE)+" ;\n")
    fp.write("\tinteger sample ;\n")
    fp.write("\n")
    fp.write("\tanalog begin\n")
    fp.write("\t\tsample = floor( "+str(2**N)+" * V(in) / vhigh ) ;\n")
    for i in range(N):
        fp.write("\t\tV(out"+str(i)+") <+ (sample & "+str(2**i)+")? vhigh : vlow ;\n")
    fp.write("\tend\n")
    fp.write("endmodule\n")
    fp.close()
    # Spice subcircuit
    ports = "" 
    for i in range(N):
        ports = ports + " out" + str(i)
    fp = open("sim/adc_model.spice", "w")
    fp.write("** Verilog-A modeled ADC **\n")
    fp.write("\n")
    fp.write(".model adc_model adc_va ;\n")
    fp.write("\n")
    fp.write(".subckt adc in"+ports+"\n")
    fp.write("\tnadc in"+ports+" adc_model\n")
    fp.write(".ends\n")
    fp.write("\n")
    fp.write(".control\n")
    fp.write("\tpre_osdi adc_model.osdi\n")
    fp.write(".endc\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return


def rdac_tb(N: int, dut_spice="rdac.spice", debug=False):
    """Generates SPICE testbench for RDAC.
    N: bits of resolution.
    dut_spice: name of the SPICE file with the inverter to be tested.
    debug: when True, testbench saves internal voltages and currents.
    """
    adc_va(N)
    lsb = pdk.LOW_VOLTAGE/2**N
    ports = ""
    for i in range(N):
        ports = ports + " d" + str(i)
    fp = open("sim/rdac_tb.spice", "w")
    fp.write("** Resistive ladder DAC testbench **\n")
    fp.write("\n")
    fp.write(pdk.LIB_MOS_TT)
    fp.write(pdk.LIB_RES_T)
    fp.write(".include \""+dut_spice+"\"\n")
    fp.write(".include \"adc_model.spice\"\n")
    fp.write("\n")
    fp.write("x1 vss vdd" + ports + " vout rdac\n")
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
        for i in range(N):
            nodes = nodes + " x1.net" + str(i+1)
            currents = currents + " @n.x1.x"+str(i+1)+".xm1.nsg13_lv_nmos[ids] @n.x1.x"+str(i+1)+".xm2.nsg13_lv_pmos[ids]"
            voltages = voltages + " @n.x1.x"+str(i+1)+".xm1.nsg13_lv_nmos[vds] @n.x1.x"+str(i+1)+".xm2.nsg13_lv_pmos[vds]"
        fp.write("save" + nodes + "\n")
        fp.write("save" + currents + "\n")
        fp.write("save" + voltages + "\n")
    fp.write("dc Vin "+str(lsb/2)+" "+str(pdk.LOW_VOLTAGE)+" "+str(lsb)+"\n")
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


def resistor_tb(L=pdk.RES_MIN_L):
    """Generates SPICE testbench for N mosfet.
    L: resistor lenght.
    """
    fp = open("sim/resistor_tb.spice", "w")
    fp.write("** Resistor testbench **\n")
    fp.write("\n")
    fp.write(pdk.LIB_RES_T)
    fp.write("\n")
    fp.write("XR1 vn vp rhigh w=0.5u l="+str(L)+"u m=1 b=0\n")
    fp.write("\n")
    fp.write("Vp vp 0 "+str(pdk.LOW_VOLTAGE)+"\n")
    fp.write("Vn vn 0 0\n")
    fp.write("\n")
    fp.write(".control\n")
    fp.write("save v(vp) v(vn) @vn[i]\n")
    fp.write("op\n")
    fp.write("wrdata "+user.SIM_PATH+"/resistor_op.txt @vn[i]\n")
    fp.write(".endc\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return


def estimate_rdac_nl(N: int, R, Rn, Rp):
    """Estimate RDAC nonlinearities.
    N: bits of resolution.
    R: RDAC unit resistance.
    Rn: NMOS on resistance.
    Rp: PMOS on resistance.
    return: INL, DNL arrays of size 2^N and 2^N-1 (normalized to LSB).
    """
    digital_input = np.arange(2**N)
    lsb = pdk.LOW_VOLTAGE/(2**N)
    transfer_function_ref = digital_input * pdk.LOW_VOLTAGE / 2**N

    r_1 = 2*R + Rp
    r_2 = np.zeros(N)
    r_3 = np.zeros(N)
    r_4 = np.zeros(N)
    k = np.zeros(N)
    temp = 2*R + Rn

    r_3[N-1] = float('inf')
    r_3[N-2] = 3*R + Rn
    k[N-1] = 1
    k[N-2] = temp / (temp + R)
    voltages = np.zeros(N)
    for i in range(N-3, -1, -1):
        temp2 = temp*r_3[i+1]/(temp + r_3[i+1])
        r_3[i] = R + temp2
        k[i] = k[i+1] * temp2/r_3[i]
    for i in range(N):
        if i == 0:
            r_2[0] = 2*R
        else:
            r_2[i] = R + temp*r_2[i-1]/(temp + r_2[i-1])
        if i == N-1:
            r_4[i] = r_2[i]
        else:
            r_4[i] = r_2[i]*r_3[i]/(r_2[i] + r_3[i])
        voltages[i] = pdk.LOW_VOLTAGE * k[i] * r_4[i]/(r_4[i] + r_1)

    transfer_function = np.zeros(2**N)
    for i in range(2**N):
        for j in range(N):
            transfer_function[i] = transfer_function[i] + ((i//2**j)%2)*voltages[j]

    inl = (transfer_function - transfer_function_ref)/lsb
    dnl = (transfer_function[1:] - transfer_function[:2**N-1] - lsb)/lsb
    return inl, dnl

