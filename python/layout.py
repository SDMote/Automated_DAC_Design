# ============================================================================
# DAC layout scripts
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

from pdk import *

def params(N=4, Wn=0.3, Wp=0.3, NG=1, Lr=RES_MIN_L, Layout=1):
    """Generates python file with parameters for layout generation.
    N: bits of resolution.
    Wn: width of inverter NMOS.
    Wp: width of inverter PMOS.
    Lr: lenght of RDAC unit resistor.
    return: string with RDAC ports.
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
    fp.write("MOS_LENGHT  = "+str(MOS_MIN_L)+"\n")
    fp.write("POLY_WIDTH  = "+str(MOS_MIN_L)+"\n")
    fp.write("RES_LENGHT  = "+str(Lr)+"\n")
    fp.write("RES_LAYOUT  = "+str(Layout)+"\n")
    fp.write("\n")
    return