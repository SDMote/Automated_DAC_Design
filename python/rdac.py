# ============================================================================
# Resistor DAC SPICE
# Alfonso Cortés - Inria AIO
# 
# ============================================================================

import pdk
from utils import net
from inverter import inverter

def rdac(N, Wn, Wp, Lr=pdk.MIN_RES_L):
    """Generates SPICE of RDAC, including SPICE for the inverter.
    N: bits of resolution.
    Wn: width of inverter NMOS.
    Wp: width of inverter PMOS.
    Lr: lenght of RDAC unit resistor.
    return: string with RDAC ports.
    """
    inverter(Wn, Wp)
    fp = open("rdac.spice", "w")
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
    ports = "out0"
    for i in range(1,N):
        ports = ports + ", out" + str(i)
    fp = open("adc.va", "w")
    fp.write("`include \"constants.h\"\n")
    fp.write("`include \"discipline.h\"\n")
    fp.write("\n")
    fp.write("module adc_va(in, "+ports+") ;\n")
    fp.write("\tinput in ;\n")
    fp.write("\toutput "+ports+" ;\n")
    fp.write("\telectrical in, "+ports+" ;\n")
    fp.write("\tparameter real vlow = 0, vhigh = 1.2 ;\n")
    fp.write("\tinteger sample ;\n")
    fp.write("\n")
    fp.write("\tanalog begin\n")
    fp.write("\t\tsample = floor( "+str(2**N)+" * V(in) / vhigh ) ;\n")
    for i in range(N):
        fp.write("\t\tV(out"+str(i)+") <+ (sample & "+str(2**i)+")? vhigh : vlow ;\n")
    fp.write("\tend\n")
    fp.write("endmodule\n")
    fp.close()
    return


def rdac_tb(N: int, dut_spice="rdac.spice"):
    """Generates SPICE testbench for RDAC.
    N: bits of resolution.
    dut_spice: name of the SPICE file with the inverter to be tested.
    """
    ports = ""
    for i in range(N):
        ports = ports + " d" + str(i)
    fp = open("rdac_tb.spice", "w")
    fp.write("** Resistive ladder DAC testbench **\n")
    fp.write("\n")
    fp.write(pdk.LIB_MOS_TT)
    fp.write(pdk.LIB_RES_T)
    fp.write(".include \""+dut_spice+"\"\n")
    fp.write("\n")
    fp.write("x1 vss vdd" + ports + " vout rdac\n")
    fp.write("\n")
    fp.write("Vdd vdd 0 1.2\n")
    fp.write("Vss vss 0 0\n")
    signals = ""
    for i in range(N):
        t = 2**i * 10
        signals = signals + " v(d" + str(i) + ")"
        fp.write("Vd"+str(i)+" d"+str(i)+" 0 dc 0 PULSE(0 1.2 0 1n 1n "+str(t-1)+"n "+str(2*t)+"n)\n")
    fp.write("\n")
    fp.write(".control\n")
    fp.write("save" + signals + " v(vout)\n")
    fp.write("tran 0.001 "+str(2**N * 10)+"n\n")
    fp.write("wrdata /foss/designs/dac/python/rdac_tran.txt" + signals + " v(vout)\n")
    fp.write("\n")
    fp.write("setplot const\n")
    fp.write("let i = 0\n")
    fp.write("repeat "+str(2**N)+"\n")
    for i in range(N):
        fp.write(" alter Vd"+str(i)+" {$&i / "+str(2**i)+" % 2 * 1.2}\n")
    fp.write(" op\n")
    fp.write(" wrdata /foss/designs/dac/python/rdac_op.txt vout\n")
    fp.write(" set appendwrite\n")
    fp.write(" let i = i + 1\n")
    fp.write("end\n")
    fp.write("\n")
    fp.write(".endc\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return


def resistor_tb(L=pdk.MIN_RES_L):
    """Generates SPICE testbench for N mosfet.
    """
    fp = open("resistor_tb.spice", "w")
    fp.write("** Resistor testbench **\n")
    fp.write("\n")
    fp.write(pdk.LIB_RES_T)
    fp.write("\n")
    fp.write("XR1 vn vp rhigh w=0.5u l="+str(L)+"u m=1 b=0\n")
    fp.write("\n")
    fp.write("Vp vp 0 1.2\n")
    fp.write("Vn vn 0 0\n")
    fp.write("\n")
    fp.write(".control\n")
    fp.write("save v(vp) v(vn) @vn[i]\n")
    fp.write("op\n")
    fp.write("wrdata /foss/designs/dac/python/resistor_op.txt @vn[i]\n")
    fp.write(".endc\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return




