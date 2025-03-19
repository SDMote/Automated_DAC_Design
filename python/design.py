# ============================================================================
# Functions for automated design
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import numpy as np
import subprocess
import pdk
import user
from utils import read_data, um, dbu
from bit import inverter, resistor_tb


def measure_resistance(Lr, Nr=1):
    resistor_tb(Lr, Nr)
    subprocess.run("ngspice -b sim/resistor_tb.spice -o sim/resistor.log > sim/temp.txt", shell=True, check=True)
    data_op_res = read_data("sim/resistor_op.txt")
    return  data_op_res[0][0]/data_op_res[1][0]


def sim2bits (Wn, Wp, NF=1):
    # requires running rdac() and rdac_tb() first for resolution 2
    Wn, Wp = inverter(Wn, Wp, NGn=NF, NGp=NF) # editing the inverter is enough to update transistor widths
    subprocess.run("ngspice -b sim/rdac_tb.spice -o sim/rdac.log > sim/temp.txt", shell=True, check=True)
    data_ids = read_data("sim/rdac_ids.txt")
    data_vds = read_data("sim/rdac_vds.txt")
    resistances = data_vds[1:]/data_ids[1:]
    Rn = (resistances[0][1]+resistances[0][3]+resistances[2][2]+resistances[2][3])/4
    Rp = (resistances[1][0]+resistances[1][2]+resistances[3][0]+resistances[3][1])/4
    return Rn, Rp, Wn, Wp


def set_ron_ratio(Wn, Wp, ratio, NF=1):
    # requires running rdac() and rdac_tb() first for resolution 2
    Wn = dbu(Wn)
    Wp = dbu(Wp)
    MIN = int(pdk.GRID / pdk.DBU)
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


def layout_params(N=4, Wn=0.3, Wp=0.3, NG=1, Lr=pdk.RES_MIN_L, Nr=1, Wg=pdk.MOS_MIN_L):
    """Generates python file with parameters for layout generation.
    N: bits of resolution.
    Wn: width of inverter NMOS.
    Wp: width of inverter PMOS.
    Lr: lenght of RDAC unit resistor.
    """
    fp = open("../klayout/python/params.py", "w")
    fp.write("# ============================================================================\n")
    fp.write("# DAC layout parameters\n")
    fp.write("#\n")
    fp.write("# ============================================================================\n")
    fp.write("\n")
    fp.write("RESOLUTION  = "+str(N)+"\n")
    fp.write("NMOS_W      = "+str(Wn)+"\n")
    fp.write("PMOS_W      = "+str(Wp)+"\n")
    fp.write("N_GATES     = "+str(NG)+"\n")
    fp.write("MOS_LENGHT  = "+str(pdk.MOS_MIN_L)+"\n")
    fp.write("POLY_WIDTH  = "+str(Wg)+"\n")
    fp.write("RES_LENGHT  = "+str(Lr)+"\n")
    fp.write("N_RES       = "+str(Nr)+"\n")
    fp.write("\n")
    return