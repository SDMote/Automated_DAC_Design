# ============================================================================
# Common functions for automated design
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import subprocess
import pdk
from utils import read_data
from spice import resistor_tb


def measure_resistance(Lr, Nr=1):
    resistor_tb(Lr, Nr)
    subprocess.run("ngspice -b sim/resistor_tb.spice -o sim/resistor.log > sim/temp.txt", shell=True, check=True)
    data_op_res = read_data("sim/resistor_op.txt")
    return  data_op_res[0][0]/data_op_res[1][0]


def layout_params(N=4, Wn=0.3, Wp=0.3, NG=1, Lr=pdk.RES_MIN_L, Nr=1, Winv=1925, Wg=pdk.MOS_MIN_L):
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
    fp.write("HALF_WIDTH  = "+str(Winv)+"\n")
    fp.write("\n")
    return