# ============================================================================
# Resistor DAC SPICE
# Alfonso Cortés - Inria AIO
# 
# ============================================================================

import user
import pdk
from utils import net
from inverter import inverter

def rdac(N, Wn, Wp, M=1, Lr=pdk.MIN_RES_L):
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


def rdac_tb(N: int, dut_spice="rdac.spice"):
    """Generates SPICE testbench for RDAC.
    N: bits of resolution.
    dut_spice: name of the SPICE file with the inverter to be tested.
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
    fp.write("dc Vin "+str(lsb/2)+" "+str(pdk.LOW_VOLTAGE)+" "+str(lsb)+"\n")
    fp.write("wrdata "+user.SIM_PATH+"rdac_dc.txt vout\n")
    fp.write(".endc\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return


def resistor_tb(L=pdk.MIN_RES_L):
    """Generates SPICE testbench for N mosfet.
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
    fp.write("wrdata "+user.SIM_PATH+"resistor_op.txt @vn[i]\n")
    fp.write(".endc\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return




