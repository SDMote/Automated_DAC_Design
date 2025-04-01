# ============================================================================
# Common circuits SPICE generation
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import user
import pdk
from utils import net, um, dbu


def inverter(Wn=pdk.MOS_MIN_W, Wp=pdk.MOS_MIN_W, Ln=pdk.MOS_MIN_L, Lp=pdk.MOS_MIN_L, NGn=1, NGp=1):
    """Generates SPICE testbench for inverter.
    Wn: total NMOS width (equivalent).
    Wp: total PMOS width (equivalent).
    Ln: NMOS lenght.
    Lp: PMOS lenght.
    NGn: number of NMOS fingers.
    NGn: number of PMOS fingers.
    """
    fwn = dbu(Wn/NGn) #if Wn%NGn == 0 else Wn//NGn + 1
    fwp = dbu(Wp/NGp) #if Wp%NGp == 0 else Wp//NGp + 1
    fp = open("sim/inverter.spice", "w")
    fp.write("** Inverter **\n")
    fp.write("\n")
    fp.write(".subckt inverter vss vdd vin vout\n")
    fp.write("XM1 vss vin vout vss sg13_lv_nmos w="+um(NGn*fwn)+"u l="+um(Ln)+"u ng="+str(NGn)+" m=1\n")
    fp.write("XM2 vout vin vdd vdd sg13_lv_pmos w="+um(NGp*fwp)+"u l="+um(Lp)+"u ng="+str(NGp)+" m=1\n")
    if NGn%2 == 0:
        fp.write("XM3 vss vss vss vss sg13_lv_nmos w="+um(4*fwn)+"u l="+um(Ln)+"u ng=4 m=1\n")
    else:
        fp.write("XM3 vss vss vss vss sg13_lv_nmos w="+um(3*fwn)+"u l="+um(Ln)+"u ng=3 m=1\n")
        fp.write("XM5 vss vss vout vss sg13_lv_nmos w="+um(fwn)+"u l="+um(Ln)+"u ng=1 m=1\n")
    if NGp%2 == 0:
        fp.write("XM4 vdd vdd vdd vdd sg13_lv_pmos w="+um(4*fwp)+"u l="+um(Lp)+"u ng=4 m=1\n")
    else:
        fp.write("XM4 vdd vdd vdd vdd sg13_lv_pmos w="+um(3*fwp)+"u l="+um(Lp)+"u ng=3 m=1\n")
        fp.write("XM6 vout vdd vdd vdd sg13_lv_pmos w="+um(fwp)+"u l="+um(Lp)+"u ng=1 m=1\n")
    fp.write(".ends\n")
    fp.write("\n")
    fp.write(".end\n")
    fp.close()
    Wn = NGn*fwn
    Wp = NGp*fwp
    return Wn, Wp



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
    fp.write("XM1 vs vg vd vs sg13_lv_nmos w="+um(W)+"u l="+um(L)+"u ng="+str(NG)+" m="+str(M)+"\n")
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
    fp.write("XM1 vd vg vs vs sg13_lv_pmos w="+um(W)+"u l="+um(L)+"u ng="+str(NG)+" m="+str(M)+"\n")
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


def resistor_tb(L=pdk.RES_MIN_L, N=1):
    """Generates SPICE testbench for N mosfet.
    L: Total lenght of unit resistor R.
    N: Number of resistances in series that make the unit resistor.
    """
    il = L//N if N > 1 else L
    fp = open("sim/resistor_tb.spice", "w")
    fp.write("** Resistor testbench **\n")
    fp.write("\n")
    fp.write(pdk.LIB_RES_T)
    fp.write("\n")
    if N<=1:
        fp.write("XR1 vn vp rhigh w=0.5u l="+um(il)+"u m=1 b=0\n")
    elif N==2:
        fp.write("XR1 vn net0 rhigh w=0.5u l="+um(il)+"u m=1 b=0\n")
        fp.write("XR2 net0 vp rhigh w=0.5u l="+um(il)+"u m=1 b=0\n")
    else:
        fp.write("XR1 vn net0 rhigh w=0.5u l="+um(il)+"u m=1 b=0\n")
        for i in range(1,N-1):
            fp.write("XR"+str(i+1)+net(i-1)+net(i)+" rhigh w=0.5u l="+um(il)+"u m=1 b=0\n")
        fp.write("XR"+str(N)+net(N-2)+" vp rhigh w=0.5u l="+um(il)+"u m=1 b=0\n")
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
