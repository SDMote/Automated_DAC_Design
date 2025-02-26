# ============================================================================
# Inverter SPICE
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import user
import pdk

def inverter(Wn=pdk.MOS_MIN_W, Wp=pdk.MOS_MIN_W, Ln=pdk.MOS_MIN_L, Lp=pdk.MOS_MIN_L, Mn=1, Mp=1, NGn=1, NGp=1):
    """Generates SPICE testbench for inverter.
    Wn: NmOS width.
    Wp: PMOS width.
    Ln: NMOS lenght.
    Lp: PMOS lenght.
    """
    fp = open("sim/inverter.spice", "w")
    fp.write("** Inverter **\n")
    fp.write("\n")
    fp.write(".subckt inverter vss vdd vin vout\n")
    fp.write("XM1 vss vin vout vss sg13_lv_nmos w="+str(Wn)+"u l="+str(Ln)+"u ng="+str(NGn)+" m="+str(Mn)+"\n")
    fp.write("XM2 vout vin vdd vdd sg13_lv_pmos w="+str(Wp)+"u l="+str(Lp)+"u ng="+str(NGp)+" m="+str(Mp)+"\n")
    fp.write(".ends\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return


def inverter_tb(dut_spice="inverter.spice"):
    """Generates SPICE testbench for inverter.
    dut_spice: name of the SPICE file with the inverter to be tested.
    """
    fp = open("sim/inverter_tb.spice", "w")
    fp.write("** Inverter testbench **\n")
    fp.write("\n")
    fp.write(pdk.LIB_MOS_TT)
    fp.write(".include \""+dut_spice+"\"\n")
    fp.write("\n")
    fp.write("x1 vss vdd vin vout inverter\n")
    fp.write("*R1 vss vout 1k\n")
    fp.write("\n")
    fp.write("Vdd vdd 0 "+str(pdk.LOW_VOLTAGE)+"\n")
    fp.write("Vss vss 0 0\n")
    fp.write("Vin vin 0 dc 0 PULSE(0 "+str(pdk.LOW_VOLTAGE)+" 0 1n 1n 90n 200n)\n")
    fp.write("\n")
    fp.write(".control\n")
    fp.write("save v(vin) v(vout)\n")
    fp.write("tran 0.001 1000n\n")
    fp.write("wrdata "+user.SIM_PATH+"/inverter_tran.txt v(vin) v(vout)\n")
    fp.write(".endc\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return


def nmos_tb(W, NG=1, L=pdk.MOS_MIN_L, M=1, VDS=pdk.LOW_VOLTAGE):
    """Generates SPICE testbench for N mosfet.
    """
    fp = open("sim/nmos_tb.spice", "w")
    fp.write("** NMOS testbench **\n")
    fp.write("\n")
    fp.write(pdk.LIB_MOS_TT)
    fp.write("\n")
    fp.write("XM1 vs vg vd vs sg13_lv_nmos w="+str(W)+"u l="+str(L)+"u ng="+str(NG)+" m="+str(M)+"\n")
    fp.write("\n")
    fp.write("Vd vd 0 "+str(VDS)+"\n")
    fp.write("Vs vs 0 0\n")
    fp.write("Vg vg 0 "+str(pdk.LOW_VOLTAGE)+"\n")
    fp.write("\n")
    fp.write(".control\n")
    fp.write("save v(vg) v(vd) @n.xm1.nsg13_lv_nmos[ids]\n")
    fp.write("op\n")
    fp.write("wrdata "+user.SIM_PATH+"/nmos_op.txt @n.xm1.nsg13_lv_nmos[ids]\n")
    fp.write(".endc\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return


def pmos_tb(W, NG=1, L=pdk.MOS_MIN_L, M=1, VDS=pdk.LOW_VOLTAGE):
    """Generates SPICE testbench for P mosfet.
    """
    fp = open("sim/pmos_tb.spice", "w")
    fp.write("** PMOS testbench **\n")
    fp.write("\n")
    fp.write(pdk.LIB_MOS_TT)
    fp.write("\n")
    fp.write("XM1 vd vg vs vs sg13_lv_pmos w="+str(W)+"u l="+str(L)+"u ng="+str(NG)+" m="+str(M)+"\n")
    fp.write("\n")
    fp.write("Vd vd 0 "+str(pdk.LOW_VOLTAGE-VDS)+"\n")
    fp.write("Vs vs 0 "+str(pdk.LOW_VOLTAGE)+"\n")
    fp.write("Vg vg 0 0\n")
    fp.write("\n")
    fp.write(".control\n")
    fp.write("save v(vg) v(vd) @n.xm1.nsg13_lv_pmos[ids]\n")
    fp.write("op\n")
    fp.write("wrdata "+user.SIM_PATH+"/pmos_op.txt @n.xm1.nsg13_lv_pmos[ids]\n")
    fp.write(".endc\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    return