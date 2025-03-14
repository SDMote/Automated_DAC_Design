# ============================================================================
# Functions for automated design
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import numpy as np
import subprocess
import pdk
import user
from utils import read_data, um
from bit import inverter, resistor_tb

def measure_resistance(Lr, Nr=1):
    resistor_tb(Lr, Nr)
    subprocess.run("ngspice -b sim/resistor_tb.spice -o sim/resistor.log > sim/temp.txt", shell=True, check=True)
    data_op_res = read_data("sim/resistor_op.txt")
    return  data_op_res[0][0]/data_op_res[1][0]


def sim2bits (Wn, Wp, NF=1):
    # requires running rdac() and rdac_tb() first for resolution 2
    inverter(Wn, Wp, NGn=NF, NGp=NF) # editing the inverter is enough to update transistor widths
    subprocess.run("ngspice -b sim/rdac_tb.spice -o sim/rdac.log > sim/temp.txt", shell=True, check=True)
    data_ids = read_data("sim/rdac_ids.txt")
    data_vds = read_data("sim/rdac_vds.txt")
    resistances = data_vds[1:]/data_ids[1:]
    Rn = (resistances[0][1]+resistances[0][3]+resistances[2][2]+resistances[2][3])/4
    Rp = (resistances[1][0]+resistances[1][2]+resistances[3][0]+resistances[3][1])/4
    return Rn, Rp


def set_ron_ratio(Wn, Wp, ratio, NF=1):
    # requires running rdac() and rdac_tb() first for resolution 2
    Rn, Rp = sim2bits (Wn, Wp)
    done = 0
    if Rn < ratio*Rp:   # edit PMOS width
        target  = Rn / ratio
        step = (Rp * Wp) / target - Wp  
        # print(" With Wn=", um(Wn), " and Wp=", um(Wp), ", Rn=", Rn, ", Rp=", Rp, " and distance=", um(step))
        while not done and abs(step) >= pdk.GRID:
            if abs(step) < 1.5*pdk.GRID:
                Wp = Wp + step            # move 1 database unit
                done = 1
            else:
                Wp = Wp + 0.5 * step      # move 50% of estimated distance
            Rn, Rp = sim2bits (Wn, Wp, NF)
            target  = Rn / ratio
            step = (Rp * Wp) / target - Wp 
            # print(" With Wn=", um(Wn), " and Wp=", um(Wp), ", Rn=", Rn, ", Rp=", Rp, " and distance=", um(step))
    else:               # edit NMOS width
        target  = Rp * ratio
        step = (Rn * Wn) / target - Wn 
        # print(" With Wn=", um(Wn), " and Wp=", um(Wp), ", Rn=", Rn, ", Rp=", Rp, " and distance=", um(step))
        while not done and abs(step) >= pdk.GRID:
            if abs(step) < 1.5*pdk.GRID:
                Wn = Wn + step            # move 1 database unit
                done = 1
            else:                    
                Wn = Wn + 0.5 * step      # move 50% of estimated distance
            Rn, Rp = sim2bits (Wn, Wp, NF)
            target  = Rp * ratio
            step = (Rn * Wn) / target - Wn  
            # print(" With Wn=", um(Wn), " and Wp=", um(Wp), ", Rn=", Rn, ", Rp=", Rp, " and distance=", um(step))
    return Wn, Wp, Rn, Rp