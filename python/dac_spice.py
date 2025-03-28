# ============================================================================
# DAC SPICE 
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import user
import pdk


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


def dac_tb(N: int, debug=False, type=0):
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
    fp = open("sim/dac_tb.spice", "w")
    fp.write("** "+str(N)+"-Bit DAC testbench **\n")
    fp.write("\n")
    fp.write(pdk.LIB_MOS_TT)
    fp.write(pdk.LIB_RES_T)
    fp.write(".include \"dac.spice\"\n")
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
        fp.write("wrdata "+user.SIM_PATH+"/dac_dc.txt vout"+nodes+"\n")
        fp.write("wrdata "+user.SIM_PATH+"/dac_ids.txt"+currents+"\n")
        fp.write("wrdata "+user.SIM_PATH+"/dac_vds.txt"+voltages+"\n")
    else:
        fp.write("wrdata "+user.SIM_PATH+"/dac_dc.txt vout\n")
    fp.write(".endc\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return


def dac_tb_tran(N: int, C, type):
    """Generates SPICE testbench to measure RDAC worst rise time.
    N: bits of resolution.
    C: load capacitance in picofarad.
    type: DAC topology to be tested.
    """
    if type == 0:
        lsb = pdk.LOW_VOLTAGE/2**N
        Vhigh = pdk.LOW_VOLTAGE - lsb
    else:
        Vhigh = pdk.LOW_VOLTAGE
    vin = " vin"
    fp = open("sim/dac_tb_tran.spice", "w")
    fp.write("** Resistive ladder DAC testbench **\n")
    fp.write("\n")
    fp.write(pdk.LIB_MOS_TT)
    fp.write(pdk.LIB_RES_T)
    fp.write(".include \"dac.spice\"\n")
    fp.write("\n")
    fp.write("x1 vss vdd" + vin*N + " vout dac\n")
    fp.write("C1 vout 0 " + str(C) + "p\n")
    fp.write("\n")
    fp.write("Vdd vdd 0 "+str(pdk.LOW_VOLTAGE)+"\n")
    fp.write("Vss vss 0 0\n")
    fp.write("Vin vin 0 PULSE(1.2 0 1u 1p 1p 1m 2m)\n")
    fp.write("\n")
    fp.write(".control\n")
    fp.write("save v(vin) v(vout)\n")
    fp.write("tran 0.001 1m\n")
    fp.write("meas tran t1 find time when v(vout)="+str(0.1*Vhigh)+" TD=0 RISE=1\n")
    fp.write("meas tran t2 find time when v(vout)="+str(0.9*Vhigh)+" TD=0 RISE=1\n")
    fp.write("wrdata "+user.SIM_PATH+"/dac_tran.txt t2-t1\n")
    fp.write(".endc\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return
